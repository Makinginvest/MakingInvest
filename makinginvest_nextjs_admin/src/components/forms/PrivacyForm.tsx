import { Container } from '@mantine/core';
import { useForm, yupResolver } from '@mantine/form';
import { showNotification } from '@mantine/notifications';

import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

import * as Yup from 'yup';
import { PrivacyModel } from '../../models/model.privacy';
import { apiGetPrivacy, apiUpdatePrivacy } from '../../models_services/firestore_privacy_service';

import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

import { FramerFadeIn } from '../framer_motion/FramerFadeIn';
import { RichTextEditor } from '../rte/RichTextEditor';
import { FormError } from './_FormError';
import FormSkelenton from './_FormSkelenton';

interface IProps {
  id?: string;
  privacy: PrivacyModel | null;
}

export default function PrivacyForm() {
  const [isInitLoading, setIsInitLoading] = useState(true);
  const [privacyModel, setPrivacyModel] = useState<PrivacyModel | null>(null);

  async function getInitData() {
    setPrivacyModel(await apiGetPrivacy());
    setIsInitLoading(false);
  }

  useEffect(() => {
    getInitData();
  }, []);

  if (isInitLoading) return <FormSkelenton />;
  if (!privacyModel) return <FormError />;

  return <Form privacy={privacyModel} />;
}

function Form({ privacy }: IProps) {
  const schema = Yup.object({
    data: Yup.string().required('Required')
  });

  const form = useForm({
    validate: yupResolver(schema),

    initialValues: {
      data: privacy?.data || ''
    }
  });

  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const { isHandlePrivacySubmitCalled } = useFirestoreStoreAdmin((state) => state);
  const { setIsHandlePrivacySubmitCalled } = useFirestoreStoreAdmin((state) => state);

  useEffect(() => {
    if (isHandlePrivacySubmitCalled) {
      handleSubmit();
    }
  }, [isHandlePrivacySubmitCalled]);

  const handleSubmit = async () => {
    console.log(form.values);
    if (form.validate().hasErrors) {
      setIsHandlePrivacySubmitCalled(false);
      return;
    }
    try {
      setIsLoading(true);
      const x = new PrivacyModel();
      x.data = form.values.data;
      await apiUpdatePrivacy(x);

      setIsHandlePrivacySubmitCalled(false);
      showNotification({ color: 'blue', title: 'Success', message: 'Privacy updated', autoClose: 6000 });
    } catch (error: any) {
      setIsHandlePrivacySubmitCalled(false);

      showNotification({
        color: 'red',
        title: 'Error',
        message: error.message,
        autoClose: 6000
      });
    }
  };

  return (
    <Container className='max-w-[1600px]' p={0}>
      <RichTextEditor value={form.values.data} onChange={(v: any) => form.setValues({ ...form.values, data: v })} className=' ' id='rte' />

      <div className='pb-20' />
    </Container>
  );
}

export interface CustomFile extends File {
  path?: string;
  preview?: string;
}
