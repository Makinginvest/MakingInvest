import { Box, Button, Container, Text, TextInput } from '@mantine/core';
import { useForm, yupResolver } from '@mantine/form';
import { showNotification } from '@mantine/notifications';
import { useRouter } from 'next/router';

import { ReactElement, useState } from 'react';
import { Send } from 'tabler-icons-react';
import * as Yup from 'yup';
import Page from '../../components/others/Page';
import Layout from '../../layouts';
import { resetPassword } from '../../models_services/firebase_auth_services';

export default function ResetPasswordPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const schema = Yup.object({
    email: Yup.string().required('Required')
  });

  const form = useForm({
    validate: yupResolver(schema),

    initialValues: {
      email: ''
    }
  });

  const handleSubmit = async () => {
    if (form.validate().hasErrors) return;

    try {
      setIsLoading(true);
      await resetPassword(form.values.email);
      setIsLoading(false);
      showNotification({ title: 'Success', message: 'Password reset link sent', autoClose: 6000 });

      setTimeout(() => {
        router.push('/signin');
      }, 5000);
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
    <Layout variant='logoOnly'>
      <Page title='Reset password'>
        <Container size='xs' className='h-[calc(100vh-200px)] flex flex-col justify-center items-center'>
          <Box className='flex flex-col w-full mx-auto mt-4 mb-10'>
            <Text className='text-3xl font-medium leading-10 text-center'>Reset Password</Text>
            <TextInput className='mt-4' placeholder='Email' label='Email' {...form.getInputProps('email')} />

            <Button
              onClick={handleSubmit}
              loading={isLoading}
              leftIcon={<Send size={14} />}
              variant='filled'
              className='w-full mt-10 text-black transition border-0 bg-app-yellow hover:bg-opacity-90'
            >
              Submit
            </Button>

            <Box className='flex justify-end'>
              <Button className='mt-8 btn-text' onClick={() => router.push('/signin')}>
                Go to sign in
              </Button>
            </Box>
          </Box>
        </Container>
      </Page>
    </Layout>
  );
}
