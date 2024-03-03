import { Box, Button, Container, Text } from '@mantine/core';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { ReactElement } from 'react';
import TermsForm from '../../components/forms/TermsForm';
import Iconify from '../../components/others/Iconify';
import Page from '../../components/others/Page';
import AuthGuard from '../../guards/AuthGuard';
import Layout from '../../layouts';
import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

export default function TermsPage() {
  const router = useRouter();
  const id = router.query.id as string;

  const { setIsHandleTermsSubmitCalled, isHandleTermsSubmitCalled } = useFirestoreStoreAdmin((state) => state);

  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='Terms'>
          <Container size={'xl'} className='mt-3'>
            <div className='flex justify-between'>
              <Box className='flex items-center'>
                <Text className='text-2xl font-semibold leading-10 cursor-pointer'>Terms and Condition</Text>
              </Box>

              <div>
                <Button loading={isHandleTermsSubmitCalled} className='btn-app' onClick={() => setIsHandleTermsSubmitCalled(true)}>
                  Submit
                </Button>
              </div>
            </div>

            <div className='mt-10' />

            <TermsForm />
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}
