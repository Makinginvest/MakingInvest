import { Box, Container, Text } from '@mantine/core';
import Link from 'next/link';
import { useEffect, useState } from 'react';
import StripeForm from '../../components/forms/StripeForm';
import Page from '../../components/others/Page';

import AuthGuard from '../../guards/AuthGuard';
import Layout from '../../layouts';

export default function DashboardPage() {
  const [value, setValue] = useState('');

  useEffect(() => {
    console.log(value);
  }, [value]);

  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='Stripe'>
          <Container className='mt-4'>
            <div className='flex justify-between'>
              <Box className='flex items-center'>
                <Link href={'/tags'}>
                  <Text className='text-2xl font-semibold leading-10 cursor-pointer'>
                    Stripe Config <span className='text-xl'>(Only Super Admins can view and edit this page)</span>
                  </Text>
                </Link>
              </Box>
            </div>

            <div className='mt-10' />
            <StripeForm />
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}
