import { Box, Container, Text } from '@mantine/core';
import { useRouter } from 'next/router';
import { ReactElement } from 'react';
import Page from '../../components/others/Page';
import SignalForm from '../../components/forms/SignalForm';
import Layout from '../../layouts';

import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';
import AuthGuard from '../../guards/AuthGuard';

export default function SignalsEditPage() {
  const router = useRouter();
  const id = router.query.id as string;
  const { isAuthenticated, isInitialized } = useFirestoreStoreAdmin((state) => state);

  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='Edit signal'>
          <Container size='xl' className=''>
            <Box className='flex flex-col w-full mx-auto mt-2 mb-10'>
              <Text className='text-2xl font-semibold leading-10 cursor-pointer'>Create a new stocks signal</Text>
              <Text className='italic font-semibold leading-10 cursor-pointer text-md'>
                Please note if the take profit is zero the value will not be shown in the app
              </Text>
              <Text className='italic font-semibold leading-10 cursor-pointer text-md'>
                When closing signals, its a good idea to include the closing time
              </Text>
              <Text className='italic font-semibold leading-10 cursor-pointer text-md'>Please specify pip or percentages</Text>
            </Box>

            <SignalForm id={id} market='stocks' dbPath='signalsStocks' />
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}
