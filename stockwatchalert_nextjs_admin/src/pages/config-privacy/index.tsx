import { Box, Button, Container, Text } from '@mantine/core';
import { useRouter } from 'next/router';

import PrivacyForm from '../../components/forms/PrivacyForm';
import Page from '../../components/others/Page';
import AuthGuard from '../../guards/AuthGuard';
import Layout from '../../layouts';
import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

export default function DashboardPage() {
  const router = useRouter();
  const id = router.query.id as string;

  const { setIsHandlePrivacySubmitCalled, isHandlePrivacySubmitCalled } = useFirestoreStoreAdmin((state) => state);

  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='Privacy'>
          <Container size={'xl'} className='mt-3'>
            <div className='flex justify-between'>
              <Box className='flex items-center'>
                <Text className='text-2xl font-semibold leading-10 cursor-pointer'>Privacy</Text>
              </Box>

              <div>
                <Button loading={isHandlePrivacySubmitCalled} className='btn-app' onClick={() => setIsHandlePrivacySubmitCalled(true)}>
                  Submit
                </Button>
              </div>
            </div>

            <div className='mt-10' />

            <PrivacyForm />
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}
