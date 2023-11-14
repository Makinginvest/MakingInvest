import { Box, Container, Text } from '@mantine/core';
import { useRouter } from 'next/router';
import AnnouncementForm from '../../components/forms/AnnouncementForm';
import Page from '../../components/others/Page';
import AuthGuard from '../../guards/AuthGuard';
import Layout from '../../layouts';
import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

export default function AnnouncementIndexPage() {
  const router = useRouter();
  const id = router.query.id as string;

  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='Contact'>
          <Container size='xl' className=''>
            <Box className='flex flex-col w-full mx-auto mt-2 mb-10'>
              <Text className='text-xl font-medium leading-10'>Create a new announcement</Text>
            </Box>
            <AnnouncementForm id={id} />
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}
