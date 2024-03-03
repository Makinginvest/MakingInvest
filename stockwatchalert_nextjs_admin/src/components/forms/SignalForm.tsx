import { Box, Button, NativeSelect, Text, Textarea, TextInput } from '@mantine/core';
import { DatePicker, TimeInput } from '@mantine/dates';
import { useForm, yupResolver } from '@mantine/form';
import { showNotification } from '@mantine/notifications';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { Send } from 'tabler-icons-react';
import * as Yup from 'yup';
import { SignalModel } from '../../models/model.signal';

import { Dropzone, IMAGE_MIME_TYPE } from '@mantine/dropzone';
import { useModals } from '@mantine/modals';
import { getFirebaseStorageDownloadUrl } from '../../models_services/firebase_image_service';
import { apiCreateSignal, apiGetSignal, apiUpdateSignal } from '../../models_services/firestore_signals_service';
import { getSignalFormErrorStopLoss, getSignalFormErrorTakeProfit } from '../../utils/calculate_signal_form_error';
import { calculateForexPct } from '../../utils/calulate_forex_pct';
import { calculateForexPips } from '../../utils/calulate_forex_pips';
import { calculatePctPips } from '../../utils/calulate_pct_pips';
import { combineDateAndTime } from '../../utils/datetime';
import { FormError } from './_FormError';
import FormSkelenton from './_FormSkelenton';
import { getBoolFromString, getStringFromBool } from '../../utils/get_bool_string';
import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

type markets = 'forex' | 'crypto' | 'stocks' | 'commodity';

interface IProps {
  id?: string;
  market: markets;
  signal?: SignalModel | null;
  dbPath: string;
}

export default function SignalForm({ id, market, dbPath }: IProps) {
  const [isInitLoading, setIsInitLoading] = useState(id != null ? true : false);
  const [signal, setSignal] = useState<SignalModel | null>(null);

  async function getInitData() {
    if (id) setSignal(await apiGetSignal({ id: id!, dbPath: dbPath }));
    setIsInitLoading(false);
  }

  useEffect(() => {
    getInitData();
  }, []);

  if (isInitLoading) return <FormSkelenton />;
  if (!signal && id) return <FormError />;

  return <Form id={id} signal={signal} market={market} dbPath={dbPath} />;
}

const schema = Yup.object({
  entryType: Yup.string().required('Required'),
  symbol: Yup.string().required('Required'),
  comment: Yup.string(),
  isFree: Yup.string().required('Required'),
  analysisImage: Yup.string(),
  analysisText: Yup.string(),
  //
  entryPrice: Yup.number().required('Required'),
  entryDate: Yup.date().required('Required'),
  entryTime: Yup.date().required('Required'),
  //
  stopLoss: Yup.number().required('Required'),
  stopLossPips: Yup.string().nullable(),
  stopLossHit: Yup.string().required('Required'),
  stopLossDate: Yup.date().nullable(),
  stopLossTime: Yup.date().nullable(),
  //
  takeProfit1: Yup.number().required('Required'),
  takeProfit1Pips: Yup.string().nullable(),
  takeProfit1Hit: Yup.string().required('Required'),
  takeProfit1Date: Yup.date().nullable(),
  takeProfit1Time: Yup.date().nullable(),
  //
  takeProfit2: Yup.string().nullable(),
  takeProfit2Pips: Yup.string().nullable(),
  takeProfit2Hit: Yup.string().required('Required'),
  takeProfit2Date: Yup.date().nullable(),
  takeProfit2Time: Yup.date().nullable(),
  //
  takeProfit3: Yup.string().nullable(),
  takeProfit3Pips: Yup.string().nullable(),
  takeProfit3Hit: Yup.string().required('Required'),
  takeProfit3Date: Yup.date().nullable(),
  takeProfit3Time: Yup.date().nullable()
  //
});

function Form({ id, signal, market, dbPath }: IProps) {
  const router = useRouter();
  const modals = useModals();
  const isAuto = (router.query.isAuto as string) || '';
  const currentSignalIsAuto = signal?.isAuto ?? false;

  const [isLoading, setIsLoading] = useState(false);
  const [file, setFile] = useState<CustomFile | null>(null);

  const symbolAggr = useFirestoreStoreAdmin((state) => state.symbolAggr);

  function getSymbols() {
    if (market === 'forex') return symbolAggr.forex;
    if (market === 'crypto') return symbolAggr.crypto;
    if (market === 'stocks') return symbolAggr.stocks;
    return [];
  }

  const form = useForm({
    validate: yupResolver(schema),
    initialValues: {
      entryType: signal?.entryType ?? 'Long',
      symbol: signal?.symbol ?? '',
      comment: signal?.comment ?? '',
      analysisImage: signal?.analysisImage ?? '',
      analysisText: signal?.analysisText ?? '',

      entryPrice: signal?.entryPrice ?? '',
      entryDate: signal?.getEntryDate ?? new Date(),
      entryTime: signal?.getEntryTime ?? new Date(),
      isFree: getStringFromBool(signal?.isFree ?? false),

      stopLoss: signal?.stopLoss ?? '',
      stopLossPips: signal?.stopLossPips ?? '',
      stopLossHit: getStringFromBool(signal?.stopLossHit ?? false),
      stopLossDate: signal?.getStopLossDate ?? null,
      stopLossTime: signal?.getStopLossTime ?? null,

      takeProfit1: signal?.takeProfit1 == 0 ? '' : signal?.takeProfit1 ?? '',
      takeProfit1Pips: signal?.takeProfit1Pips ?? '',
      takeProfit1Hit: getStringFromBool(signal?.takeProfit1Hit ?? false),
      takeProfit1Date: signal?.getTakeProfit1Date ?? null,
      takeProfit1Time: signal?.getTakeProfit1Time ?? null,

      takeProfit2: signal?.takeProfit2 == 0 ? '' : signal?.takeProfit2 ?? '',
      takeProfit2Pips: signal?.takeProfit2Pips ?? '',
      takeProfit2Hit: getStringFromBool(signal?.takeProfit2Hit ?? false),
      takeProfit2Date: signal?.getTakeProfit2Date ?? null,
      takeProfit2Time: signal?.getTakeProfit2Time ?? null,

      takeProfit3: signal?.takeProfit3 == 0 ? '' : signal?.takeProfit3 ?? '',
      takeProfit3Pips: signal?.takeProfit3Pips ?? '',
      takeProfit3Hit: getStringFromBool(signal?.takeProfit3Hit ?? false),
      takeProfit3Date: signal?.getTakeProfit3Date ?? null,
      takeProfit3Time: signal?.getTakeProfit3Time ?? null
    }
  });

  type HandleSubmitProps = {
    sendNotification: boolean;
    isClosed?: boolean;
  };

  function handleSubmitClose() {
    if (form.validate().hasErrors) return;
    openCloseModal();
  }

  const handleSubmit = async ({ sendNotification, isClosed }: HandleSubmitProps) => {
    console.log('form.values', form.values);
    console.log('form.errors', form.errors);

    if (form.validate().hasErrors) return;

    try {
      setIsLoading(true);
      let s = new SignalModel();
      // spread the signal object
      if (signal) s = { ...s, ...SignalModel.toJson(signal) };

      if (!id) s.isAuto = isAuto == 'true' ? true : false;
      s.market = market;
      s.entryType = form.values.entryType;
      s.symbol = form.values.symbol;
      s.comment = form.values.comment;
      s.analysisImage = form.values.analysisImage;
      s.analysisText = form.values.analysisText;
      //
      s.entryPrice = Number(form.values.entryPrice);
      s.entryDateTime = combineDateAndTime(form.values.entryDate, form.values.entryTime);
      s.isFree = getBoolFromString(form.values.isFree);

      s.stopLoss = Number(form.values.stopLoss);
      s.stopLossPct = calculateForexPct(s.entryPrice, s.stopLoss);
      s.stopLossPips = calculateForexPips(s.entryPrice, s.stopLoss);
      s.stopLossHit = getBoolFromString(form.values.stopLossHit);
      s.stopLossDateTime = combineDateAndTime(form.values.stopLossDate, form.values.stopLossTime);

      s.takeProfit1 = Number(form.values.takeProfit1);
      s.takeProfit1Pct = calculateForexPct(s.entryPrice, s.takeProfit1);
      s.takeProfit1Pips = calculateForexPips(s.entryPrice, s.takeProfit1);
      s.takeProfit1Hit = getBoolFromString(form.values.takeProfit1Hit);
      s.takeProfit1DateTime = combineDateAndTime(form.values.takeProfit1Date, form.values.takeProfit1Time);

      s.takeProfit2 = Number(form.values.takeProfit2);
      s.takeProfit2Pct = calculateForexPct(s.entryPrice, s.takeProfit2);
      s.takeProfit2Pips = calculateForexPips(s.entryPrice, s.takeProfit2);
      s.takeProfit2Hit = getBoolFromString(form.values.takeProfit2Hit);
      s.takeProfit2DateTime = combineDateAndTime(form.values.takeProfit2Date, form.values.takeProfit2Time);

      s.takeProfit3 = Number(form.values.takeProfit3);
      s.takeProfit3Pct = calculateForexPct(s.entryPrice, s.takeProfit3);
      s.takeProfit3Pips = calculateForexPips(s.entryPrice, s.takeProfit3);
      s.takeProfit3Hit = getBoolFromString(form.values.takeProfit3Hit);
      s.takeProfit3DateTime = combineDateAndTime(form.values.takeProfit3Date, form.values.takeProfit3Time);

      s.timestampCreated = signal?.timestampCreated ?? new Date();
      s.timestampUpdated = new Date();

      if (file) s.analysisImage = await getFirebaseStorageDownloadUrl({ file: file! });

      if (!signal) await apiCreateSignal({ signal: s, sendNotification, dbPath });
      if (signal && id) await apiUpdateSignal({ signal: s, sendNotification, dbPath, id, isClosed });

      setIsLoading(false);

      if (market == 'commodity') router.push('/signals-commodities');
      if (market == 'crypto') router.push('/signals-crypto');
      if (market == 'forex') router.push('/signals-forex');
      if (market == 'stocks') router.push('/signals-stocks');

      showNotification({ title: 'Success', message: 'Signal was created', autoClose: 6000 });
    } catch (error: any) {
      console.log('error', error);
      setIsLoading(false);
      showNotification({ color: 'red', title: 'Error', message: 'There was an error creating the signals', autoClose: 6000 });
    }
  };

  const openCloseModal = () => {
    const modalId = modals.openModal({
      title: 'Are you sure you want to proceed?',
      centered: true,
      children: (
        <>
          <Text size='sm'>Manually close signal? This action cannot be undone.</Text>
          <Box className='flex justify-end mt-6'>
            <Button
              variant='outline'
              className='mx-2 border w-min border-light-800 text-dark-400'
              fullWidth
              onClick={() => modals.closeModal(modalId)}
              mt='md'>
              No don't close it
            </Button>

            <Button
              className='mx-2 w-min btn-delete'
              fullWidth
              onClick={() => {
                modals.closeModal(modalId);
                handleSubmit({ sendNotification: false, isClosed: true });
              }}
              mt='md'>
              close signal
            </Button>
          </Box>
        </>
      )
    });
  };

  const handleDropFiles = (files: File[]) => {
    if (files.length > 0) {
      const file = files[0];
      setFile(Object.assign(file, { preview: URL.createObjectURL(file) }));
    }
  };

  const DropzoneRemoveImage = () => {
    const removeFile = () => {
      form.setFieldValue('analysisImage', '');
      setFile(null);
    };
    if (file || form.values.analysisImage) {
      return (
        <Button className='absolute z-40 btn right-2 top-2' onClick={removeFile}>
          Remove
        </Button>
      );
    }
    return null;
  };

  const DropzoneChildren = () => {
    if (form.values.analysisImage != '') {
      return (
        <Box className='relative flex justify-center'>
          <img className='h-[300px]' src={form.values.analysisImage} alt='Preview' />
        </Box>
      );
    }
    if (file)
      return (
        <Box className='relative flex justify-center'>
          <img className='h-[300px]' src={file.preview} alt='Preview' />{' '}
        </Box>
      );
    return (
      <Box className='min-h-[300px] pointer-events-none flex justify-center items-center text-center'>
        <div>
          <Text size='xl' inline>
            Drag analysis image here
          </Text>
          <Text size='sm' color='dimmed' inline mt={7}>
            Attach a single file not larger than 5MB
          </Text>
        </div>
      </Box>
    );
  };

  return (
    <Box className=''>
      {isAuto == 'true' && (
        <Text className='mb-5 text-xl font-bold text-red-500'>
          You are creating an auto signal, once created values cant be change the api service will handle it
        </Text>
      )}
      {currentSignalIsAuto && <Text className='mb-5 text-xl font-bold text-red-500'>This is an auto signal most fields have been disabled</Text>}

      <div className='grid xs:grid-cols-2 md:grid-cols-3 gap-x-3'>
        {isAuto != 'true' && (
          <TextInput className='w-full' placeholder='Symbol' label='Symbol' {...form.getInputProps('symbol')} disabled={currentSignalIsAuto} />
        )}

        {isAuto == 'true' && (
          <NativeSelect
            className='w-full'
            disabled={currentSignalIsAuto}
            placeholder='----'
            label='Symbol'
            data={['', ...getSymbols().map((s) => s.symbol)]}
            onChange={(e: any) => form.setFieldValue('symbol', e.target.value)}
            value={form.values.symbol}
            error={form.errors.symbol}
          />
        )}

        <NativeSelect
          className='w-full'
          disabled={currentSignalIsAuto}
          placeholder='Long'
          label='Long/Short'
          data={['Long', 'Short']}
          onChange={(e: any) => form.setFieldValue('entryType', e.target.value)}
          value={form.values.entryType}
          error={form.errors.entryType}
        />

        <NativeSelect
          className='w-full'
          placeholder='Free'
          label='Free'
          data={['Yes', 'No']}
          onChange={(e: any) => form.setFieldValue('isFree', e.target.value)}
          value={form.values.isFree}
          error={form.errors.isFree}
        />
      </div>

      <div className='grid mt-6 xs:grid-cols-2 md:grid-cols-3 gap-x-3'>
        <TextInput
          label='Entry'
          placeholder='Entry'
          className='w-full'
          {...form.getInputProps('entryPrice')}
          type={'number'}
          disabled={currentSignalIsAuto}
        />
        <DatePicker label='Entry day' className='w-full' {...form.getInputProps('entryDate')} disabled={currentSignalIsAuto} />
        <TimeInput label='Entry time' className='w-full' format='12' {...form.getInputProps('entryTime')} disabled={currentSignalIsAuto} />
      </div>

      {/* stop loss */}
      <div className='grid mt-6 xs:grid-cols-2 md:grid-cols-5 gap-x-3'>
        <TextInput
          label='Stop loss'
          placeholder='Stop loss'
          disabled={currentSignalIsAuto}
          type={'number'}
          className='w-full'
          {...form.getInputProps('stopLoss')}
          error={getSignalFormErrorStopLoss(form.values.entryType, form.values.entryPrice, form.values.stopLoss) || form.errors.stopLoss}
        />

        <TextInput
          label='Stop loss pct(%) pips'
          placeholder='Stop pct loss pips'
          className='w-full'
          value={calculatePctPips(form.values.entryPrice, form.values.stopLoss)}
          disabled
        />

        <DatePicker label='Stop loss day' className='w-full' {...form.getInputProps('stopLossDate')} disabled={!id || currentSignalIsAuto} />
        <TimeInput
          label='Stop loss time'
          className='w-full'
          format='12'
          {...form.getInputProps('stopLossTime')}
          disabled={!id || currentSignalIsAuto}
          clearable
        />
        <NativeSelect
          className='w-full'
          placeholder=''
          disabled={!id || currentSignalIsAuto}
          label='Stop loss hit'
          data={['Yes', 'No']}
          onChange={(e: any) => form.setFieldValue('stopLossHit', e.target.value)}
          value={form.values.stopLossHit}
          error={form.errors.stopLossHit}
        />
      </div>

      <div className='grid mt-6 xs:grid-cols-2 md:grid-cols-5 gap-x-3'>
        <TextInput
          disabled={currentSignalIsAuto}
          label='Take profit 1'
          placeholder='Take profit 1'
          type={'number'}
          className='w-full'
          {...form.getInputProps('takeProfit1')}
          error={getSignalFormErrorTakeProfit(form.values.entryType, form.values.entryPrice, form.values.takeProfit1) || form.errors.takeProfit1}
        />

        <TextInput
          label='Take profit 1 pct(%) pips'
          placeholder='No update'
          value={calculatePctPips(form.values.entryPrice, form.values.takeProfit1)}
          className='w-full'
          disabled
        />
        <DatePicker
          label='Take profit 1 day'
          className='w-full'
          {...form.getInputProps('takeProfit1Date')}
          disabled={!id || currentSignalIsAuto}
        />
        <TimeInput
          label='Take profit 1 time'
          className='w-full'
          format='12'
          {...form.getInputProps('takeProfit1Time')}
          clearable
          disabled={!id || currentSignalIsAuto}
        />
        <NativeSelect
          className='w-full'
          disabled={!id || currentSignalIsAuto}
          placeholder=''
          label='Take profit 1 hit'
          data={['Yes', 'No']}
          onChange={(e: any) => form.setFieldValue('takeProfit1Hit', e.target.value)}
          value={form.values.takeProfit1Hit}
          error={form.errors.takeProfit1Hit}
        />
      </div>

      <div className='grid mt-6 xs:grid-cols-2 md:grid-cols-5 gap-x-3'>
        <TextInput
          disabled={currentSignalIsAuto}
          label='Take profit 2'
          placeholder='Take profit 2'
          className='w-full'
          onChange={(e: any) => {
            form.setFieldValue('takeProfit2', e.target.value == '' ? null : e.target.value);
            console.log(form.values.takeProfit2);
          }}
          value={form.values.takeProfit2}
          error={getSignalFormErrorTakeProfit(form.values.entryType, form.values.entryPrice, form.values.takeProfit2) || form.errors.takeProfit2}
        />

        <TextInput
          label='Take profit 2 pct(%) pips'
          className='w-full'
          value={calculatePctPips(form.values.entryPrice, form.values.takeProfit2)}
          disabled
        />
        <DatePicker
          label='Take profit 2 day'
          className='w-full'
          {...form.getInputProps('takeProfit2Date')}
          disabled={!id || currentSignalIsAuto}
        />
        <TimeInput
          label='Take profit 2 time'
          className='w-full'
          format='12'
          {...form.getInputProps('takeProfit2Time')}
          clearable
          disabled={!id || currentSignalIsAuto}
        />

        <NativeSelect
          className='w-full'
          placeholder=''
          disabled={!id || currentSignalIsAuto}
          label='Take profit 2 hit'
          data={['Yes', 'No']}
          onChange={(e: any) => form.setFieldValue('takeProfit2Hit', e.target.value)}
          value={form.values.takeProfit2Hit}
          error={form.errors.takeProfit2Hit}
        />
      </div>

      <div className='grid mt-6 xs:grid-cols-2 md:grid-cols-5 gap-x-3'>
        <TextInput
          disabled={currentSignalIsAuto}
          label='Take profit 3'
          placeholder='Take profit 3'
          className='w-full'
          onChange={(e: any) => {
            form.setFieldValue('takeProfit3', e.target.value == '' ? null : e.target.value);
          }}
          error={getSignalFormErrorTakeProfit(form.values.entryType, form.values.entryPrice, form.values.takeProfit3) || form.errors.takeProfit3}
          value={form.values.takeProfit3}
        />
        <TextInput
          label='Take profit 3 pct(%) pips'
          className='w-full'
          value={calculatePctPips(form.values.entryPrice, form.values.takeProfit3)}
          disabled
        />

        <DatePicker
          label='Take profit 3 day'
          className='w-full'
          {...form.getInputProps('takeProfit3Date')}
          disabled={!id || currentSignalIsAuto}
        />
        <TimeInput
          label='Take profit 3 time'
          className='w-full'
          format='12'
          {...form.getInputProps('takeProfit3Time')}
          clearable
          disabled={!id || currentSignalIsAuto}
        />

        <NativeSelect
          className='w-full'
          placeholder=''
          disabled={!id || currentSignalIsAuto}
          label='Take profit 3 hit'
          data={['Yes', 'No']}
          onChange={(e: any) => form.setFieldValue('takeProfit3Hit', e.target.value)}
          value={form.values.takeProfit3Hit}
          error={form.errors.takeProfit3Hit}
        />
      </div>

      <Box className='relative'>
        <DropzoneRemoveImage />
        <Dropzone
          className='z-0 p-2 mt-8'
          multiple={false}
          disabled={file != null || form.values.analysisImage != ''}
          onDrop={handleDropFiles}
          onReject={(files) => console.log('rejected files', files)}
          maxSize={3 * 1024 ** 2}
          accept={IMAGE_MIME_TYPE}>
          <DropzoneChildren />
        </Dropzone>
      </Box>

      <div className='mb-5'>
        <Textarea label='Analysis' placeholder='Analysis' minRows={4} maxLength={140} className='mt-4' {...form.getInputProps('analysisText')} />
        <Textarea label='Comment' placeholder='Result' minRows={4} maxLength={140} className='mt-4' {...form.getInputProps('comment')} />
      </div>

      <div className='mb-20 md:flex gap-x-5'>
        {(!id || signal?.isClosed == false) && (
          <Button
            loading={isLoading}
            onClick={() => handleSubmit({ sendNotification: true })}
            leftIcon={<Send size={14} />}
            variant='filled'
            className='w-full mt-10 text-black transition border-0 bg-app-yellow hover:bg-opacity-90'>
            {id ? 'Update with notification' : 'Submit with notification'}
          </Button>
        )}

        <Button
          loading={isLoading}
          onClick={() => handleSubmit({ sendNotification: false })}
          leftIcon={<Send size={14} />}
          variant='filled'
          className='w-full mt-5 text-white transition bg-gray-500 border-0 md:mt-10 bg-opacity-60 hover:bg-opacity-90'>
          {id ? 'Update quietly' : 'Submit quietly'}
        </Button>

        {id && signal?.isClosed == false && (
          <Button
            onClick={handleSubmitClose}
            leftIcon={<Send size={14} />}
            variant='filled'
            className='w-full mt-5 text-white transition bg-red-500 border-0 md:mt-10 hover:bg-opacity-90'>
            Close signal
          </Button>
        )}
      </div>
    </Box>
  );
}

export interface CustomFile extends File {
  path?: string;
  preview?: string;
}
