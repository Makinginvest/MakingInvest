import { Button, Container, TextInput } from '@mantine/core';
import { useForm, yupResolver } from '@mantine/form';
import { showNotification } from '@mantine/notifications';

import { useEffect, useState } from 'react';
import { Send } from 'tabler-icons-react';
import * as Yup from 'yup';
import { SMTPModel } from '../../models/model.smtp';

import { apiGetSMTP, apiUpdateSMTP } from '../../models_services/firestore_smtp_service';
import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

import FormSkelenton from './_FormSkelenton';

interface IProps {
  smtp: SMTPModel | null;
}

export default function SMTPForm() {
  const [isInitLoading, setIsInitLoading] = useState(true);
  const [smtp, setSMTP] = useState<SMTPModel | null>(null);

  async function getInitData() {
    setSMTP(await apiGetSMTP());
    setIsInitLoading(false);
  }

  useEffect(() => {
    getInitData();
  }, []);

  if (isInitLoading) return <FormSkelenton />;
  return <Form smtp={smtp} />;
}

function Form({ smtp }: IProps) {
  const [isLoading, setIsLoading] = useState(false);
  const { authUser } = useFirestoreStoreAdmin((state) => state);

  const schema = Yup.object({
    email: Yup.string().required('Required'),
    password: Yup.string().required('Required'),
    host: Yup.string().required('Required'),
    port: Yup.string().required('Required')
  });

  const form = useForm({
    validate: yupResolver(schema),

    initialValues: {
      email: smtp?.email || '',
      password: smtp?.password || '',
      host: smtp?.host || '',
      port: smtp?.port || ''
    }
  });

  const handleSubmit = async () => {
    if (form.validate().hasErrors) return;

    try {
      setIsLoading(true);
      const x = new SMTPModel();
      x.email = form.values.email;
      x.password = form.values.password;
      x.host = form.values.host;
      x.port = form.values.port;

      await apiUpdateSMTP(x);

      setIsLoading(false);

      showNotification({ color: 'blue', title: 'Success', message: 'Smtp updated', autoClose: 6000 });
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
        <TextInput className='mt-4' placeholder='Email' label='Email' maxLength={50} {...form.getInputProps('email')} />
        <TextInput className='mt-4' placeholder='Password' label='Password' maxLength={50} {...form.getInputProps('password')} />
        <TextInput className='mt-4' placeholder='Host' label='Host' maxLength={50} {...form.getInputProps('host')} />
        <TextInput className='mt-4' placeholder='Port' label='Port' maxLength={50} {...form.getInputProps('port')} />
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

export interface CustomFile extends File {
  path?: string;
  preview?: string;
}
