import { Box } from '@mantine/core';
import Head from 'next/head';
import { forwardRef, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  meta?: ReactNode;
  title: string;
}

const Page = forwardRef<HTMLDivElement, Props>(({ children, title = '', meta, ...other }, ref) => (
  <>
    <Head>
      <title>{`${title} | MakingInvest`}</title>
      {meta}
    </Head>

    <Box sx={{}} ref={ref} {...other}>
      {children}
    </Box>
  </>
));

export default Page;
