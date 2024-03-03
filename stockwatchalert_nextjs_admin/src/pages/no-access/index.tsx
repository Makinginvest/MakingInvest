import { Box, Button, Text } from '@mantine/core';
import Link from 'next/link';
import router, { useRouter } from 'next/router';
import Router from 'next/router';
import Page from '../../components/others/Page';
import Layout from '../../layouts';
import { signOut } from '../../models_services/firebase_auth_services';

export default function NoAccessPage() {
  const router = useRouter();
  function _signOut() {
    signOut();
    router.push('/signin');
  }
  return (
    <Page title='No Access'>
      <Box className='flex flex-col items-center justify-center h-screen dark:bg-dark-100 bg-light-100'>
        <Text className='mb-10 font-bold'>You dont have access to this page. Please contact the admin.</Text>
        <img src='/svg/404.svg' className='h-[300px]' />
        <Button onClick={_signOut} className='w-[200px] mt-12 border-0 bg-app-primary text-white hover:bg-opacity-90 transition'>
          Back to sign in
        </Button>
      </Box>
    </Page>
  );
}
