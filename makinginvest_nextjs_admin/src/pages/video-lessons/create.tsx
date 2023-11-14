import { Box, Container, Text } from '@mantine/core';
import { useRouter } from 'next/router';
import { ReactElement } from 'react';
import VideoLessonForm from '../../components/forms/VideoLessonForm';
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
        <Page title='Video Lesson'>
          <Container size='xl' className=''>
            <Box className='flex flex-col w-full mx-auto mt-10 mb-10'>
              <Text className='text-xl font-medium leading-10'>Create a new video</Text>
            </Box>
            <VideoLessonForm id={id} />
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}
