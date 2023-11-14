import { Box, Container, Text } from '@mantine/core';
import { useEffect } from 'react';
import Iconify from '../../components/others/Iconify';

import Page from '../../components/others/Page';

import AuthGuard from '../../guards/AuthGuard';
import Layout from '../../layouts';
import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

interface DashboardCardProps {
  title: string;
  value: number;
  icon: string;
}

function DashboardCard({ icon, title, value }: DashboardCardProps) {
  return (
    <Box className='flex justify-between w-full px-6 py-4 border rounded-lg  border-gray-200 dark:border-[#373A40]'>
      <div className='flex'>
        <Text className='mr-2 text-lg font-semibold leading-10 cursor-pointer'>{title}</Text>
        <Text className='text-lg font-semibold leading-10 cursor-pointer '>{value}</Text>
      </div>
      <Iconify icon={icon} className='h-[28px] w-[28px]' />
    </Box>
  );
}

export default function DashboardPage() {
  const { getDashboard, dashboard } = useFirestoreStoreAdmin((state) => state);

  useEffect(() => {
    getDashboard();
  }, []);

  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='App info'>
          <Container size={'xl'} className='mt-4'>
            <Text className='text-2xl font-semibold leading-10 cursor-pointer'>Dashboard</Text>

            <Text className='mt-5 text-lg font-semibold leading-10 cursor-pointer'>Overview</Text>
            <div className='grid grid-cols-1 mt-0 md:grid-cols-4 gap-x-3 gap-y-3'>
              <DashboardCard title='Users:' value={dashboard.totalUsers} icon='mdi:users-group' />
              <DashboardCard title='Posts:' value={dashboard.totalPosts} icon='material-symbols:local-post-office-outline' />
              <DashboardCard title='Announcements:' value={dashboard.totalAnnouncements} icon='tabler:info-square-rounded' />
              <DashboardCard title='Videos:' value={dashboard.totalVideoLessons} icon='bxs:videos' />
            </div>
            {/* <Text className='mt-5 text-lg font-semibold leading-10 cursor-pointer'>Open Signals</Text> */}
            {/* <div className='grid grid-cols-1 mt-0 md:grid-cols-3 gap-x-3 gap-y-3'>
              <DashboardCard title='Crypto Open:' value={dashboard.totalSignalsCryptoOpen} icon='tabler:coin-bitcoinp' />
              <DashboardCard title='Forex Open:' value={dashboard.totalSignalsForexOpen} icon='material-symbols:area-chart-outline-rounded' />
              <DashboardCard title='Stocks Open:' value={dashboard.totalSignalsStocksOpen} icon='material-symbols:insert-chart-rounded' />
            </div>
            <Text className='mt-5 text-lg font-semibold leading-10 cursor-pointer'>Closed Signals</Text>
            <div className='grid grid-cols-1 mt-0 md:grid-cols-3 gap-x-3 gap-y-3'>
              <DashboardCard title='Crypto Closed:' value={dashboard.totalSignalsCryptoClosed} icon='tabler:coin-bitcoin' />
              <DashboardCard
                title='Forex Closed:'
                value={dashboard.totalSignalsForexClosed}
                icon='material-symbols:area-chart-outline-rounded'
              />
              <DashboardCard title='Stocks Closed:' value={dashboard.totalSignalsStocksClosed} icon='material-symbols:insert-chart-rounded' />
            </div> */}
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}
