import { Box, Container, Text } from '@mantine/core';
import { useRouter } from 'next/router';
import UserForm from '../../components/forms/UserForm';
import Page from '../../components/others/Page';
import AuthGuard from '../../guards/AuthGuard';
import Layout from '../../layouts';

import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

export default function PageX() {
  const router = useRouter();
  const id = router.query.id as string;
  const { isAuthenticated, isInitialized } = useFirestoreStoreAdmin((state) => state);

  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='Users'>
          <Container size='xl' className=''>
            <Box className='flex flex-col w-full mx-auto mt-1 mb-10'>
              <Text className='text-2xl font-semibold leading-10 cursor-pointer'>Update User</Text>
            </Box>

            <UserForm id={id} />
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}
