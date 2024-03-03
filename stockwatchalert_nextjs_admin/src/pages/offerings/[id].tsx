import { Box, Container, Text } from '@mantine/core';
import { useRouter } from 'next/router';
import Page from '../../components/others/Page';
import AuthGuard from '../../guards/AuthGuard';
import Layout from '../../layouts';

import OfferingForm from '../../components/forms/OfferingForm';

export default function AnnouncementEditPage() {
  const router = useRouter();
  const id = router.query.id as string;

  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='Contact'>
          <Container size='xl' className=''>
            <Box className='flex flex-col w-full mx-auto mt-2 mb-10'>
              <Text className='text-2xl font-semibold leading-10 cursor-pointer'>Update Offering</Text>
            </Box>
            <OfferingForm id={id} />
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}
