import { Button, Container, Divider, NativeSelect, TextInput } from '@mantine/core';
import { useForm, yupResolver } from '@mantine/form';
import { showNotification } from '@mantine/notifications';

import { useEffect, useState } from 'react';
import { Send } from 'tabler-icons-react';
import * as Yup from 'yup';
import { StripeModel } from '../../models/model.stripe';

import { apiGetStripe, apiUpdateStripe } from '../../models_services/firestore_stripe_service';
import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

import FormSkelenton from './_FormSkelenton';

interface IProps {
  stripe: StripeModel | null;
}

export default function StripeForm() {
  const [isInitLoading, setIsInitLoading] = useState(true);
  const [stripeModel, setStripeModel] = useState<StripeModel | null>(null);

  async function getInitData() {
    setStripeModel(await apiGetStripe());
    setIsInitLoading(false);
  }

  useEffect(() => {
    getInitData();
  }, []);

  if (isInitLoading) return <FormSkelenton />;
  return <Form stripe={stripeModel} />;
}

function Form({ stripe }: IProps) {
  const [isLoading, setIsLoading] = useState(false);
  const { authUser } = useFirestoreStoreAdmin((state) => state);

  const schema = Yup.object({
    stripeTestKey: Yup.string().required('Required'),
    stripeLiveKey: Yup.string().required('Required'),
    stripeMonthlyProductTest: Yup.string().required('Required'),
    stripeMonthlyProductLive: Yup.string().required('Required'),
    stripeYearlyProductTest: Yup.string().required('Required'),
    stripeYearlyProductLive: Yup.string().required('Required'),
    isStripeKeyLive: Yup.string().required('Required')
  });

  const form = useForm({
    validate: yupResolver(schema),

    initialValues: {
      stripeTestKey: stripe?.stripeTestKey || '',
      stripeLiveKey: stripe?.stripeLiveKey || '',
      stripeMonthlyProductTest: stripe?.stripeMonthlyProductTest || '',
      stripeMonthlyProductLive: stripe?.stripeMonthlyProductLive || '',
      stripeYearlyProductTest: stripe?.stripeYearlyProductTest || '',
      stripeYearlyProductLive: stripe?.stripeYearlyProductLive || '',
      isStripeKeyLive: stripe?.isStripeKeyLive == true ? 'Yes' : 'No'
    }
  });

  const handleSubmit = async () => {
    if (form.validate().hasErrors) return;

    try {
      setIsLoading(true);
      const x = new StripeModel();
      x.stripeTestKey = form.values.stripeTestKey;
      x.stripeLiveKey = form.values.stripeLiveKey;
      x.stripeMonthlyProductTest = form.values.stripeMonthlyProductTest;
      x.stripeMonthlyProductLive = form.values.stripeMonthlyProductLive;
      x.stripeYearlyProductTest = form.values.stripeYearlyProductTest;
      x.stripeYearlyProductLive = form.values.stripeYearlyProductLive;
      x.isStripeKeyLive = form.values.isStripeKeyLive == 'Yes' ? true : false;

      await apiUpdateStripe(x);

      setIsLoading(false);

      showNotification({ color: 'blue', title: 'Success', message: 'Stripe updated', autoClose: 6000 });
    } catch (error: any) {
      setIsLoading(false);
      showNotification({
        color: 'red',
        title: 'Error',
        message: error.message,
        autoClose: 6000
      });
    }
  };

  return (
    <Container p={0}>
      <div className='mt-4'>
        <NativeSelect
          className=''
          placeholder='Use Live Mode?'
          label='Use Live mode'
          data={['Yes', 'No']}
          {...form.getInputProps('isStripeKeyLive')}
        />

        <TextInput className='mt-4' placeholder='Live Key' label='Live Key' maxLength={50} {...form.getInputProps('stripeLiveKey')} />
        <TextInput
          className='mt-4'
          placeholder='Live Monthly Product'
          label='Live Monthly Product'
          maxLength={50}
          {...form.getInputProps('stripeMonthlyProductLive')}
        />
        <TextInput
          className='mt-4'
          placeholder='Live Yearly Produc'
          label='Live Yearly Product'
          maxLength={50}
          {...form.getInputProps('stripeYearlyProductLive')}
        />

        <Divider className='mt-12 mb-8 border-red-500' />

        <TextInput className='mt-4' placeholder='Test Key' label='Test Key' maxLength={50} {...form.getInputProps('stripeTestKey')} />

        <TextInput
          className='mt-4'
          placeholder='Test Monthly Product'
          label='Test Monthly Product'
          maxLength={50}
          {...form.getInputProps('stripeMonthlyProductTest')}
        />
        <TextInput
          className='mt-4'
          placeholder='Test Yearly Produc'
          label='Test Yearly Product'
          maxLength={50}
          {...form.getInputProps('stripeYearlyProductTest')}
        />
      </div>
      <Button
        onClick={handleSubmit}
        leftIcon={<Send size={14} />}
        variant='filled'
        disabled={isLoading || authUser?.isSuperAdmin == false}
        className='w-full mt-4 h-[40px] bg-app-primary text-white border-0 hover:opacity-90 hover:text-md'>
        Submit
      </Button>
    </Container>
  );
}
