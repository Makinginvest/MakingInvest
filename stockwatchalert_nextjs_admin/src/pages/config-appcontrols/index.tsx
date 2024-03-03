import { Box, Container, Text } from '@mantine/core';
import AppControlsForm from '../../components/forms/AppControlsForm';

import Page from '../../components/others/Page';

import AuthGuard from '../../guards/AuthGuard';
import Layout from '../../layouts';

export default function DashboardPage() {
  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='App info'>
          <Container className='mt-4'>
            <div className='flex justify-between'>
              <Box className='flex items-center'>
                <Text className='text-2xl font-semibold leading-10 cursor-pointer'>App Settings</Text>
              </Box>
            </div>

            <div className='mt-10' />
            <AppControlsForm />
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}
