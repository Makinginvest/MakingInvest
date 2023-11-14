import { Box, Button, Divider, Grid, NativeSelect, Text, TextInput } from '@mantine/core';
import { Dropzone, IMAGE_MIME_TYPE } from '@mantine/dropzone';
import { useForm, yupResolver } from '@mantine/form';
import { showNotification } from '@mantine/notifications';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { Send } from 'tabler-icons-react';
import * as Yup from 'yup';
import { AppControlsPublicModel } from '../../models/model.app_controls';

import { getFirebaseStorageDownloadUrl } from '../../models_services/firebase_image_service';
import { apiGetAppControlsPublic, apiUpdateAppControlsPublic } from '../../models_services/firestore_appcontrols_service';
import { getBoolFromString, getStringFromBool } from '../../utils/get_bool_string';
import FormSkelenton from './_FormSkelenton';

interface IProps {
  appInfo?: AppControlsPublicModel | null;
}

export default function AppControlForm() {
  const [isInitLoading, setIsInitLoading] = useState(true);
  const [appInfo, setAppInfo] = useState<AppControlsPublicModel | null>(null);

  async function getInitData() {
    setAppInfo(await apiGetAppControlsPublic());
    setIsInitLoading(false);
  }

  useEffect(() => {
    getInitData();
  }, []);

  if (isInitLoading) return <FormSkelenton />;

  return <Form appInfo={appInfo} />;
}

function Form({ appInfo }: IProps) {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [file, setFile] = useState<CustomFile | null>(null);

  const handleDropFiles = (files: File[]) => {
    if (files.length > 0) {
      const file = files[0];
      setFile(Object.assign(file, { preview: URL.createObjectURL(file) }));
    }
  };

  const urlWithWebSocketRegex = new RegExp(/^(https?|wss?|ws?):\/\/([\da-z.-]+)\.([a-z.]{2,6})([\/\w .-]*)*\/?$/);

  const schema = Yup.object({
    name: Yup.string().required('Required'),
    logoImage: Yup.string(),
    adminUrl: Yup.string().url().required('Required'),
    frontendUrl: Yup.string().url().required('Required'),
    apiUrl: Yup.string().url().required('Required'),
    apiWebSocketUrl: Yup.string().matches(urlWithWebSocketRegex, 'Invalid URL').required('Required'),
    isEnableForexSignals: Yup.string().required('Required'),
    isEnableCryptoSignals: Yup.string().required('Required'),
    isEnableStocksSignals: Yup.string().required('Required'),
    isEnableForexNews: Yup.string().required('Required'),
    isEnableCryptoNews: Yup.string().required('Required'),
    isEnableStocksNews: Yup.string().required('Required'),
    sortOrderForexSignals: Yup.number().required('Required'),
    sortOrderCryptoSignals: Yup.number().required('Required'),
    sortOrderStocksSignals: Yup.number().required('Required'),
    headingNameCrypto: Yup.string().required('Required'),
    headingNameForex: Yup.string().required('Required'),
    headingNameStocks: Yup.string().required('Required')
  });

  const form = useForm({
    validate: yupResolver(schema),
    initialValues: {
      name: appInfo?.name ?? 'MakingInvest',
      logoImage: appInfo?.logoImage ?? '',
      frontendUrl: appInfo?.frontendUrl ?? '',
      adminUrl: appInfo?.adminUrl ?? '',
      apiUrl: appInfo?.apiUrl ?? '',
      apiWebSocketUrl: appInfo?.apiWebSocketUrl ?? '',
      isEnableForexSignals: getStringFromBool(appInfo?.isEnabledForexSignals ?? false),
      isEnableCryptoSignals: getStringFromBool(appInfo?.isEnabledCryptoSignals ?? false),
      isEnableStocksSignals: getStringFromBool(appInfo?.isEnabledStocksSignals ?? false),
      isEnableForexNews: getStringFromBool(appInfo?.isEnabledForexNews ?? false),
      isEnableCryptoNews: getStringFromBool(appInfo?.isEnabledCryptoNews ?? false),
      isEnableStocksNews: getStringFromBool(appInfo?.isEnabledStocksNews ?? false),
      sortOrderForexSignals: appInfo?.sortOrderForexSignals ?? 0,
      sortOrderCryptoSignals: appInfo?.sortOrderCryptoSignals ?? 0,
      sortOrderStocksSignals: appInfo?.sortOrderStocksSignals ?? 0,
      headingNameCrypto: appInfo?.headingNameCrypto ?? 'Crypto',
      headingNameForex: appInfo?.headingNameForex ?? 'Forex',
      headingNameStocks: appInfo?.headingNameStocks ?? 'Stocks'
    }
  });

  const handleSubmit = async () => {
    console.log('form.errors', form.errors);
    if (form.validate().hasErrors) return;

    try {
      setIsLoading(true);
      let s = new AppControlsPublicModel();
      s = { ...s, ...appInfo };
      s.name = form.values.name;
      s.frontendUrl = form.values.frontendUrl;
      s.adminUrl = form.values.adminUrl;
      s.apiUrl = form.values.apiUrl;
      s.apiWebSocketUrl = form.values.apiWebSocketUrl;
      s.logoImage = appInfo?.logoImage ?? '';
      s.isEnabledForexSignals = getBoolFromString(form.values.isEnableForexSignals);
      s.isEnabledCryptoSignals = getBoolFromString(form.values.isEnableCryptoSignals);
      s.isEnabledStocksSignals = getBoolFromString(form.values.isEnableStocksSignals);
      s.isEnabledForexNews = getBoolFromString(form.values.isEnableForexNews);
      s.isEnabledCryptoNews = getBoolFromString(form.values.isEnableCryptoNews);
      s.isEnabledStocksNews = getBoolFromString(form.values.isEnableStocksNews);
      s.sortOrderForexSignals = Number(form.values.sortOrderForexSignals);
      s.sortOrderCryptoSignals = Number(form.values.sortOrderCryptoSignals);
      s.sortOrderStocksSignals = Number(form.values.sortOrderStocksSignals);
      s.headingNameCrypto = form.values.headingNameCrypto;
      s.headingNameForex = form.values.headingNameForex;
      s.headingNameStocks = form.values.headingNameStocks;

      if (file) s.logoImage = await getFirebaseStorageDownloadUrl({ file: file! });

      await apiUpdateAppControlsPublic(s);

      setIsLoading(false);

      showNotification({ title: 'Success', message: 'App info updated', autoClose: 6000 });
    } catch (error) {
      console.log(error);
      setIsLoading(false);
      showNotification({ color: 'red', title: 'Error', message: 'There was an error updating', autoClose: 6000 });
    }
  };

  const DropzoneRemoveImage = () => {
    const removeFile = () => {
      form.setFieldValue('image', '');
      setFile(null);
    };
    if (file || form.values.logoImage) {
      return (
        <Button className='absolute z-40 btn right-2 top-2' onClick={removeFile}>
          Remove
        </Button>
      );
    }
    return null;
  };

  const DropzoneChildren = () => {
    if (form.values.logoImage != '') {
      return (
        <Box className='relative flex justify-center'>
          <img className='h-[300px]' src={form.values.logoImage} alt='Preview' />
        </Box>
      );
    }
    if (file)
      return (
        <Box className='relative flex justify-center'>
          <img className='h-[300px]' src={file.preview} alt='Preview' />
        </Box>
      );
    return (
      <Box className='min-h-[300px] pointer-events-none flex justify-center items-center text-center'>
        <div>
          <Text size='xl' inline>
            Drag app logo here, ensure it is a rectangle and transparent background
          </Text>
          <Text size='sm' color='dimmed' inline mt={7}>
            Drag app logo here, ensure it is a rectangle and transparent background
          </Text>
        </div>
      </Box>
    );
  };

  return (
    <Box className=''>
      <Grid align={'start'}>
        <Grid.Col md={12} xs={12}>
          <TextInput className='mt-4' placeholder='Admin URL' label='Admin Url' {...form.getInputProps('adminUrl')} />

          <TextInput className='mt-4' placeholder='Frontend URL' label='Frontend Url' {...form.getInputProps('frontendUrl')} />

          <TextInput className='mt-4' placeholder='API URL' label='API Url' {...form.getInputProps('apiUrl')} />

          <TextInput className='mt-4' placeholder='Websocket URL' label='Websocket Url' {...form.getInputProps('apiWebSocketUrl')} />

          <TextInput className='mt-4' placeholder='App name' label='App name' {...form.getInputProps('name')} />

          <div className='grid md:grid-cols-3 gap-x-3'>
            <NativeSelect
              className='w-full'
              placeholder='Enable Crypto'
              label='Enable Crypto'
              data={['Yes', 'No']}
              onChange={(e: any) => form.setFieldValue('isEnableCryptoSignals', e.target.value)}
              value={form.values.isEnableCryptoSignals}
              error={form.errors.isEnableCryptoSignals}
            />

            <NativeSelect
              className='w-full'
              placeholder='Enable Forex'
              label='Enable Forex'
              data={['Yes', 'No']}
              onChange={(e: any) => form.setFieldValue('isEnableForexSignals', e.target.value)}
              value={form.values.isEnableForexSignals}
              error={form.errors.isEnableForexSignals}
            />

            <NativeSelect
              className='w-full'
              placeholder='Enable Stocks'
              label='Enable Stocks'
              data={['Yes', 'No']}
              onChange={(e: any) => form.setFieldValue('isEnableStocksSignals', e.target.value)}
              value={form.values.isEnableStocksSignals}
              error={form.errors.isEnableStocksSignals}
            />
          </div>

          <div className='grid md:grid-cols-3 gap-x-3'>
            <TextInput
              className='w-full'
              placeholder='Sort Order Crypto'
              label='Sort Order Crypto'
              {...form.getInputProps('sortOrderCryptoSignals')}
            />
            <TextInput
              className='w-full'
              placeholder='Sort Order Forex'
              label='Sort Order Forex'
              {...form.getInputProps('sortOrderForexSignals')}
            />
            <TextInput
              className='w-full'
              placeholder='Sort Order Stocks'
              label='Sort Order Stocks'
              {...form.getInputProps('sortOrderStocksSignals')}
            />
          </div>

          <div className='grid md:grid-cols-3 gap-x-3'>
            <TextInput className='w-full' placeholder='Heading Crypto' label='Heading Crypto' {...form.getInputProps('headingNameCrypto')} />
            <TextInput className='w-full' placeholder='Heading Forex' label='Heading Forex' {...form.getInputProps('headingNameForex')} />
            <TextInput className='w-full' placeholder='Heading Stocks' label='Heading Stocks' {...form.getInputProps('headingNameStocks')} />
          </div>

          <div className='grid md:grid-cols-3 gap-x-3'>
            <NativeSelect
              className='w-full'
              placeholder='Show Crypto news'
              label='Show Crypto news'
              data={['Yes', 'No']}
              onChange={(e: any) => form.setFieldValue('isEnableCryptoNews', e.target.value)}
              value={form.values.isEnableCryptoNews}
              error={form.errors.isEnableCryptoNews}
            />

            <NativeSelect
              className='w-full'
              placeholder='Show Forex news'
              label='Show Forex news'
              data={['Yes', 'No']}
              onChange={(e: any) => form.setFieldValue('isEnableForexNews', e.target.value)}
              value={form.values.isEnableForexNews}
              error={form.errors.isEnableForexNews}
            />

            <NativeSelect
              className='w-full'
              placeholder='Show Stocks news'
              label='Show Stocks news'
              data={['Yes', 'No']}
              onChange={(e: any) => form.setFieldValue('isEnableStocksNews', e.target.value)}
              value={form.values.isEnableStocksNews}
              error={form.errors.isEnableStocksNews}
            />
          </div>

          <Box className='relative'>
            <DropzoneRemoveImage />
            <Dropzone
              className='z-0 p-2 mt-8'
              multiple={false}
              disabled={file != null || form.values.logoImage != ''}
              onDrop={handleDropFiles}
              onReject={(files) => console.log('rejected files', files)}
              maxSize={3 * 1024 ** 2}
              accept={IMAGE_MIME_TYPE}
            >
              <DropzoneChildren />
            </Dropzone>
          </Box>
        </Grid.Col>

        <Grid.Col md={12} xs={12}>
          <Box>
            <Button
              loading={isLoading}
              onClick={handleSubmit}
              leftIcon={<Send size={14} />}
              variant='filled'
              className='w-full mt-10 text-black transition border-0 bg-app-yellow hover:bg-opacity-90'
            >
              Submit
            </Button>
          </Box>
        </Grid.Col>
      </Grid>
    </Box>
  );
}

export interface CustomFile extends File {
  path?: string;
  preview?: string;
}
