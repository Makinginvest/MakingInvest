import { Container } from '@mantine/core';
import { useForm, yupResolver } from '@mantine/form';
import { showNotification } from '@mantine/notifications';

import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

import * as Yup from 'yup';
import { TermsModel } from '../../models/model.terms';

import { apiGetTerms, apiUpdateTerms } from '../../models_services/firestore_terms_service';
import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

import { FramerFadeIn } from '../framer_motion/FramerFadeIn';
import { RichTextEditor } from '../rte/RichTextEditor';
import { FormError } from './_FormError';
import FormSkelenton from './_FormSkelenton';

interface IProps {
  id?: string;
  terms: TermsModel | null;
}

export default function TermsForm() {
  const [isInitLoading, setIsInitLoading] = useState(true);
  const [termsModel, setTermsModel] = useState<TermsModel | null>(null);

  async function getInitData() {
    setTermsModel(await apiGetTerms());
    setIsInitLoading(false);
  }

  useEffect(() => {
    getInitData();
  }, []);

  if (isInitLoading) return <FormSkelenton />;
  if (!termsModel) return <FormError />;

  return <Form terms={termsModel} />;
}

function Form({ terms }: IProps) {
  const schema = Yup.object({
    data: Yup.string().required('Required')
  });

  const form = useForm({
    validate: yupResolver(schema),

    initialValues: {
      data: terms?.data || ''
    }
  });

  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const { isHandleTermsSubmitCalled } = useFirestoreStoreAdmin((state) => state);
  const { setIsHandleTermsSubmitCalled } = useFirestoreStoreAdmin((state) => state);

  useEffect(() => {
    if (isHandleTermsSubmitCalled) {
      handleSubmit();
    }
  }, [isHandleTermsSubmitCalled]);

  const handleSubmit = async () => {
    console.log(form.values);
    if (form.validate().hasErrors) {
      setIsHandleTermsSubmitCalled(false);
      return;
    }

    try {
      setIsLoading(true);
      const x = new TermsModel();
      x.data = form.values.data;
      await apiUpdateTerms(x);

      setIsHandleTermsSubmitCalled(false);
      showNotification({ color: 'blue', title: 'Success', message: 'Terms updated', autoClose: 6000 });
    } catch (error: any) {
      setIsHandleTermsSubmitCalled(false);
      showNotification({
        color: 'red',
        title: 'Error',
        message: error.message,
        autoClose: 6000
      });
    }
  };

  return (
    <Container size={'xl'} p={0}>
      <RichTextEditor value={form.values.data} onChange={(v: any) => form.setValues({ ...form.values, data: v })} className='' id='rte' />
      <div className='pb-20' />
    </Container>
  );
}

export interface CustomFile extends File {
  path?: string;
  preview?: string;
}
