import { Box, Button, Text, TextInput } from '@mantine/core';
import { useForm, yupResolver } from '@mantine/form';
import { showNotification } from '@mantine/notifications';
import { useRouter } from 'next/router';
import { useState } from 'react';
import { Send } from 'tabler-icons-react';
import * as Yup from 'yup';
import { signinWithEmail } from '../../models_services/firebase_auth_services';

import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

export default function SignInForm() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const { isAuthenticated, isInitialized } = useFirestoreStoreAdmin((state) => state);
  const { streamAuthUserAdmin } = useFirestoreStoreAdmin((state) => state);

  const schema = Yup.object({
    email: Yup.string().required('Required'),
    password: Yup.string().required('Required')
  });

  const form = useForm({
    validate: yupResolver(schema),

    initialValues: {
      email: '',
      password: ''
    }
  });

  const handleSubmit = async () => {
    if (form.validate().hasErrors) return;
    try {
      setIsLoading(true);
      await signinWithEmail(form.values.email, form.values.password);

      router.push('/dashboard');
      streamAuthUserAdmin();

      setIsLoading(false);
    } catch (error) {
      setIsLoading(false);
      showNotification({
        color: 'red',
        title: 'Error',
        message: 'Invalid email or password',
        autoClose: 6000
      });
    }
  };

  return (
    <Box className='xs:w-full sm:w-[500px] py-10 px-6 rounded-md'>
      <Box className='flex flex-col w-full mx-auto text-center '>
        <Text className='mt-4 text-2xl font-bold'>MakingInvest account login</Text>
      </Box>

      <Box className='flex flex-col items-center mt-8'>
        <Box className='w-full'>
          <TextInput placeholder='Email' label='Email' radius={0} {...form.getInputProps('email')} />
          <TextInput type='password' className='mt-4' placeholder='Password' label='Password' {...form.getInputProps('password')} />

          <Button
            onClick={handleSubmit}
            loading={isLoading}
            leftIcon={<Send size={14} />}
            variant='filled'
            className='w-full mt-10 text-black transition border-0 bg-app-yellow hover:bg-opacity-90'>
            Sign in with email
          </Button>
        </Box>

        <Box className='flex flex-col flex-wrap items-start justify-start w-full mt-4'>
          <Button
            onClick={() => router.push('/reset-password')}
            className='btn-text text-app-yellowText hover:text-opacity-80 text-[14px] mt-[2px] transition'>
            Forgot password?
          </Button>
        </Box>
      </Box>
    </Box>
  );
}
