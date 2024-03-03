import { Box, Button, Text, TextInput } from '@mantine/core';
import { useForm, yupResolver } from '@mantine/form';
import { showNotification } from '@mantine/notifications';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { Send } from 'tabler-icons-react';
import * as Yup from 'yup';
import { createSuperAdminUserWithEmail } from '../../models_services/firebase_auth_services';

import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

export default function SignInForm() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const { isAuthenticated, isInitialized } = useFirestoreStoreAdmin((state) => state);
  const { streamAuthUserAdmin } = useFirestoreStoreAdmin((state) => state);

  const schema = Yup.object({
    email: Yup.string().required('Required'),
    password: Yup.string().required('Required'),
    passwordConfirm: Yup.string().oneOf([Yup.ref('password'), null], 'Passwords must match')
  });

  const form = useForm({
    validate: yupResolver(schema),

    initialValues: {
      email: '',
      password: '',
      passwordConfirm: ''
    }
  });

  const handleSubmit = async () => {
    if (form.validate().hasErrors) return;
    try {
      setIsLoading(true);
      await createSuperAdminUserWithEmail(form.values.email, form.values.password);

      router.push('/dashboard');
      streamAuthUserAdmin();

      setIsLoading(false);
    } catch (error) {
      setIsLoading(false);
      console.log(error);
      showNotification({
        color: 'red',
        title: 'Error',
        message: 'Invalid email or password',
        autoClose: 6000
      });
    }
  };

  return (
    <Box className='xs:w-full sm:w-[600px] py-10 px-6 rounded-md h-screen'>
      <Box className='flex flex-col w-full mx-auto text-center'>
        <Text className='mt-10 font-bold xs:text-xl sm:text-2xl'>Welcome to MakingInvest</Text>
        <Text className='mt-2 font-bold xs:text-md sm:text-lg'>Please create the admin users below</Text>
      </Box>

      <Box className='flex flex-col items-center mt-8'>
        <Box className='w-full'>
          <TextInput className='mt-4' placeholder='Email' label='Email' {...form.getInputProps('email')} />
          <TextInput type='password' className='mt-4' placeholder='Password' label='Password' {...form.getInputProps('password')} />

          <TextInput
            type='password'
            className='mt-4'
            placeholder='Confirm Password'
            label='Confirm Password'
            {...form.getInputProps('passwordConfirm')}
          />

          <Button
            onClick={handleSubmit}
            loading={isLoading}
            leftIcon={<Send size={14} />}
            variant='filled'
            className='w-full mt-10 text-black transition border-0 bg-app-yellow hover:bg-opacity-90'>
            Sign up with email
          </Button>
        </Box>
      </Box>
    </Box>
  );
}
