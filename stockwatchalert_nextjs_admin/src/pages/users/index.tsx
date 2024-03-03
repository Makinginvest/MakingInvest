import { Box, Container, Text } from '@mantine/core';
import { useModals } from '@mantine/modals';
import { createColumnHelper } from '@tanstack/react-table';
import { useRouter } from 'next/router';
import { Edit } from 'tabler-icons-react';
import Page from '../../components/others/Page';
import { BaseTable } from '../../components/tables/BaseTable';
import AuthGuard from '../../guards/AuthGuard';
import Layout from '../../layouts';
import { AuthUserModel } from '../../models/model.authuser';

import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';
import { fDate } from '../../utils/format_time';

const columnHelper = createColumnHelper<AuthUserModel>();

const columns = [
  columnHelper.accessor('createdDateTime', {
    header: 'Created',
    cell: (info) => fDate(info.getValue())
  }),
  columnHelper.accessor('lastLoginDateTime', {
    header: 'Last login',
    cell: (info) => fDate(info.getValue())
  }),

  columnHelper.accessor('id', {
    header: 'User Id',
    cell: (info) => <Box className='flex items-center'>{info.row.original.id}</Box>
  }),

  columnHelper.accessor('getRoleString', {
    header: `Role`,
    cell: (info) => <Text>{info.getValue()}</Text>
  }),

  columnHelper.accessor('email', {
    header: 'Email',
    cell: (info) => (info.getValue() == '' ? 'N/A' : info.getValue())
  }),

  columnHelper.accessor('getHasSubscriptionString', {
    header: `Sub`,
    cell: (info) => <Text>{info.getValue()}</Text>
  }),

  columnHelper.accessor('getSubscriptionEndDate', {
    header: `Sub End`,
    cell: (info) => fDate(info.getValue())
  }),

  columnHelper.accessor('userId', {
    header: 'Action',
    cell: (info) => (
      <Box className='flex items-center'>
        <TableActions authUser={info.row.original} />
      </Box>
    )
  })
];

export default function SignalsIndexPage() {
  const authUsers = useFirestoreStoreAdmin((state) => state.authUsers);

  const router = useRouter();
  const access = (router.query.access as string) || '';

  const data = filterUsers();

  function filterUsers() {
    if (access === 'superadmin') return authUsers.filter((user) => user.isSuperAdmin === true);
    if (access === 'admin') return authUsers.filter((user) => user.isAdmin === true);
    if (access === 'subscriber') return authUsers.filter((user) => user.getHasSubscription === true);
    if (access === 'lifetime') return authUsers.filter((user) => user.subIsLifetime === true);
    return authUsers;
  }

  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='Users'>
          <Container size='xl' className='mb-20'>
            <Box className='flex items-center justify-between mt-1 mb-5 text-center'>
              <Text className='text-2xl font-semibold leading-10 cursor-pointer'>Users</Text>
            </Box>

            <BaseTable data={data} columns={columns} />
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}

/* ----------------------------- NOTE FUNCTIONS ----------------------------- */

function TableActions({ authUser }: { authUser: AuthUserModel }) {
  const router = useRouter();
  const modals = useModals();

  return (
    <Box className='flex'>
      <Edit size={20} className='mr-2 cursor-pointer text-app-yellow' onClick={() => router.push(`/users/${authUser.id}`)} />{' '}
    </Box>
  );
}
