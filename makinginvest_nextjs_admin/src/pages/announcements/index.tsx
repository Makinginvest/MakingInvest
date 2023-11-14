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
import { AnnouncementModel } from '../../models/model.announcement';
import { apiDeleteAnnouncement } from '../../models_services/firestore_announcements_service';

import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';
import { fDate } from '../../utils/format_time';
import { truncateText } from '../../utils/trancate_text';

const columnHelper = createColumnHelper<AnnouncementModel>();

const columns = [
  columnHelper.accessor('timestampCreated', {
    header: 'Date',
    cell: (info) => fDate(info.getValue()),
    size: 170
  }),

  columnHelper.accessor('title', {
    header: 'Title',
    cell: (info) => info.getValue()
  }),
  columnHelper.accessor('body', {
    header: 'Body',
    cell: (info) => truncateText(info.getValue(), 50)
  }),
  columnHelper.accessor('link', {
    header: 'Link',
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

export default function AnnouncementIndexPage() {
  const { announcements } = useFirestoreStoreAdmin((state) => state);

  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='Contact'>
          <Container size='xl' className=''>
            <Box className='flex items-center justify-between mt-2 mb-5 text-center'>
              <Text className='text-2xl font-semibold leading-10 cursor-pointer'>Announcements</Text>
              <Link href='/announcements/create'>
                <Button type='submit' variant='white' className='text-black transition border-0 bg-app-yellow hover:bg-opacity-90'>
                  New Announcement
                </Button>
              </Link>
            </Box>

            <BaseTable data={announcements} columns={columns} />
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}

function TableActions({ id }: { id: string }) {
  const router = useRouter();
  const modals = useModals();

  const handleDelete = async (modalId: string) => {
    modals.closeModal(modalId);
    try {
      await apiDeleteAnnouncement(id);
      showNotification({ title: 'Success', message: 'Announcement deleted', autoClose: 6000 });
    } catch (error) {
      showNotification({ color: 'red', title: 'Error', message: 'There was an error deleting the announcement', autoClose: 6000 });
    }
  };

  const openDeleteModal = () => {
    const modalId = modals.openModal({
      title: 'Are you sure you want to proceed?',
      centered: true,
      children: (
        <>
          <Text size='sm'>Delete this announcement? This action cannot be undone.</Text>
          <Box className='flex justify-end mt-6'>
            <Button variant='outline' className='mx-2 w-min' fullWidth onClick={() => modals.closeModal(modalId)} mt='md'>
              No don't delete it
            </Button>

            <Button className='mx-2 w-min btn-delete' fullWidth onClick={() => handleDelete(modalId)} mt='md'>
              Delete Announcement
            </Button>
          </Box>
        </>
      )
    });
  };

  return (
    <Box className='flex'>
      <Edit className='mr-2 cursor-pointer text-app-yellow' onClick={() => router.push(`/announcements/${id}`)} />{' '}
      <Trash className='text-red-400 cursor-pointer' onClick={openDeleteModal} />
    </Box>
  );
}
