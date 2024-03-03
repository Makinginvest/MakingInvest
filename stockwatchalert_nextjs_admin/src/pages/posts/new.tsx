import { Button, Container, Text } from '@mantine/core';
import { ReactElement } from 'react';
import Page from '../../components/others/Page';

import PostForm from '../../components/forms/PostForm';
import AuthGuard from '../../guards/AuthGuard';
import Layout from '../../layouts';
import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

export default function DashboardPage() {
  const { setIsHandlePostSubmitCalled, isHandlePostSubmitCalled } = useFirestoreStoreAdmin((state) => state);

  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='New Post'>
          <Container size={'xl'} className='mt-3'>
            <div className='flex justify-between'>
              <Text className='text-2xl font-semibold leading-10 cursor-pointer'>Posts</Text>
              <div>
                <Button loading={isHandlePostSubmitCalled} className='btn-app' onClick={() => setIsHandlePostSubmitCalled(true)}>
                  Submit
                </Button>
              </div>
            </div>
            <div className='mt-10' />

            <PostForm />
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}
