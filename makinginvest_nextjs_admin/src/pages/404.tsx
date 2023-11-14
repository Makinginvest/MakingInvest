import { Box, Button } from '@mantine/core';
import Link from 'next/link';
import { ReactElement } from 'react';
import Page from '../components/others/Page';
import Layout from '../layouts';

export default function FourZeroFourPage() {
  return (
    <Page title='404 Page Not Found'>
      <Box className='min-h-[85vh] flex flex-col items-center justify-center'>
        <img src='/svg/404.svg' className='h-[300px]' />
        <Link href='/' passHref>
          <Button className='w-[200px] mt-12 border-0 bg-app-yellow text-black hover:bg-opacity-90 transition'>Go Home</Button>
        </Link>
      </Box>
    </Page>
  );
}

FourZeroFourPage.getLayout = function getLayout(page: ReactElement) {
  return <Layout variant='admin'>{page}</Layout>;
};
