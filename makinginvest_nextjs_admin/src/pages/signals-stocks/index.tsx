import { Box, Button, Container, Text } from '@mantine/core';
import { useModals } from '@mantine/modals';

import { showNotification } from '@mantine/notifications';
import { createColumnHelper } from '@tanstack/react-table';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { Edit, Trash } from 'tabler-icons-react';
import Page from '../../components/others/Page';
import { BaseTable } from '../../components/tables/BaseTable';
import AuthGuard from '../../guards/AuthGuard';
import Layout from '../../layouts';
import { SignalModel } from '../../models/model.signal';

import { apiDeleteSignal } from '../../models_services/firestore_signals_service';
import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';
import { fDate, fDateTimeSuffix } from '../../utils/format_time';

const columnHelper = createColumnHelper<SignalModel>();

const columns = [
  columnHelper.accessor('entryDateTime', {
    header: 'Entry Date',
    cell: (info) => fDateTimeSuffix(info.getValue()),
    size: 200
  }),

  columnHelper.accessor('getSignalOpenStatus', {
    header: 'Status',
    cell: (info) => <Text>{info.getValue()}</Text>
  }),
  columnHelper.accessor('isAuto', {
    header: 'Auto',
    cell: (info) => <Text>{info.getValue() ? 'Yes' : 'No'}</Text>
  }),

  columnHelper.accessor('isFree', {
    header: 'Free',
    cell: (info) => <Text>{info.getValue() ? 'Yes' : 'No'}</Text>
  }),
  columnHelper.accessor('entryType', {
    header: 'Type',
    cell: (info) => info.getValue()
  }),

  columnHelper.accessor('symbol', {
    header: 'Symbol',
    cell: (info) => info.getValue()
  }),
  columnHelper.accessor('entryPrice', {
    header: 'Entry',
    cell: (info) => info.getValue()
  }),
  columnHelper.accessor('stopLoss', {
    header: 'Stop Loss',
    cell: (info) => info.getValue()
  }),
  columnHelper.accessor('takeProfit1', {
    header: 'Take Profit',
    cell: (info) => info.getValue()
  }),
  columnHelper.accessor('takeProfit2', {
    header: 'Take Profit',
    cell: (info) => info.getValue()
  }),
  columnHelper.accessor('takeProfit3', {
    header: 'Take Profit',
    cell: (info) => info.getValue()
  }),

  columnHelper.accessor('id', {
    header: 'Action',
    cell: (info) => (
      <Box className='flex items-center justify-center '>
        <TableActions id={info.row.original.id} />
      </Box>
    )
  })
];

export default function SignalsIndexPage() {
  const signalsOpen = useFirestoreStoreAdmin((state) => state.signalsStocksOpen) || [];
  const signalsClosed = useFirestoreStoreAdmin((state) => state.signalsStocksClosed) || [];

  const router = useRouter();
  const isClosed = (router.query.isClosed as string) || '';

  const data = filterSignals();

  function filterSignals() {
    if (isClosed === 'false') return signalsOpen;
    if (isClosed === 'true') return signalsClosed;
    return signalsOpen;
  }

  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='MakingInvest'>
          <Container size='xl' className=''>
            <Box className='flex items-center justify-between mt-2 mb-5 text-center'>
              <Text className='text-2xl font-semibold leading-10 cursor-pointer'>{isClosed == 'true' ? 'Closed' : 'Open'} stock signals</Text>

              <div>
                <Link href='/signals-stocks/create?isAuto=false' className='mr-4'>
                  <Button
                    type='submit'
                    variant='white'
                    className='text-white transition bg-opacity-50 border-0 bg-app-secondary hover:bg-opacity-90'>
                    New manual signal
                  </Button>
                </Link>

                <Link href='/signals-stocks/create?isAuto=true'>
                  <Button type='submit' variant='white' className='text-black transition border-0 bg-app-yellow hover:bg-opacity-90'>
                    New auto signal
                  </Button>
                </Link>
              </div>
            </Box>

            <BaseTable data={data} columns={columns} />
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}

/* ----------------------------- NOTE FUNCTIONS ----------------------------- */

function TableActions({ id }: { id: string }) {
  const router = useRouter();
  const modals = useModals();

  const handleDelete = async (modalId: string) => {
    modals.closeModal(modalId);
    try {
      if (id) await apiDeleteSignal({ id: id!, dbPath: 'signalsStocks' });
      showNotification({ title: 'Success', message: 'Signal deleted', autoClose: 6000 });
    } catch (error) {
      showNotification({ color: 'red', title: 'Error', message: 'There was an error deleting the signal', autoClose: 6000 });
    }
  };

  const openDeleteModal = () => {
    const modalId = modals.openModal({
      title: 'Are you sure you want to proceed?',
      centered: true,
      children: (
        <>
          <Text size='sm'>Delete this signal? This action cannot be undone.</Text>
          <Box className='flex justify-end mt-6'>
            <Button
              variant='outline'
              className='mx-2 border w-min border-light-800 text-dark-400'
              fullWidth
              onClick={() => modals.closeModal(modalId)}
              mt='md'>
              No don't delete it
            </Button>

            <Button className='mx-2 w-min btn-delete' fullWidth onClick={() => handleDelete(modalId)} mt='md'>
              Delete signal
            </Button>
          </Box>
        </>
      )
    });
  };

  return (
    <Box className='flex'>
      <Edit size={20} className='mr-2 cursor-pointer text-app-yellow' onClick={() => router.push(`/signals-stocks/${id}`)} />{' '}
      <Trash size={20} className='text-red-400 cursor-pointer' onClick={openDeleteModal} />
    </Box>
  );
}
