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
  const { isAuthenticated } = useFirestoreStoreAdmin((state) => state);

  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='Video Lesson'>
          <Container size='xl' className=''>
            <Box className='flex flex-col w-full mx-auto mt-20 mb-10'>
              <Text className='text-2xl font-semibold leading-10 cursor-pointer'>Update Video Lesson</Text>
            </Box>
            <VideoLessonForm id={id} />
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}
