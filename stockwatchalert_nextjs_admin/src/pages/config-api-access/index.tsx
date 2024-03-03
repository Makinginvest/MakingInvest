import { Box, Button, Container, Divider, Text } from '@mantine/core';

import Page from '../../components/others/Page';

import AuthGuard from '../../guards/AuthGuard';
import Layout from '../../layouts';
import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

export default function DashboardPage() {
  const { apiControlsPublic } = useFirestoreStoreAdmin((state) => state);
  return (
    <AuthGuard>
      <Layout variant='admin'>
        <Page title='App info'>
          <Container size={'xl'} className='mt-4'>
            <div className='flex justify-between'>
              <Box className='flex items-center'>
                <Text className='text-2xl font-semibold leading-10 cursor-pointer'>Api Access</Text>
              </Box>
            </div>

            {/* <Text>
              <pre>{JSON.stringify(apiControlsPublic, null, 2)}</pre>
            </Text> */}

            <div className='mt-5' />

            {apiControlsPublic.apiHasAccess && (
              <div>
                <Text>Great you have api access!!!</Text>
                <Text>Enjoy the benefits below</Text>
                <Divider className='my-5' />
                <Text className='mb-4'>Benefits of having api access:</Text>
                <Text className='mb-1'>- Live prices in your app</Text>
                <Text className='mb-1'>- Automatic take profit and stop loss</Text>
                <Text className='mb-1'>- Just add your signals and forget it!</Text>
                <Text className='mb-1'>- Live news</Text>

                <div className='mt-5' />
                <Text>
                  <Button className='btn-app'>
                    <a href='https://t.me/codememory' target='_blank'>
                      Contact us on telegram
                    </a>
                  </Button>
                </Text>
              </div>
            )}

            {!apiControlsPublic.apiHasAccess && (
              <div>
                <Text>Sorry you dont have api access yet.</Text>
                <Text>You can enable by contracting us on telegram via the link below</Text>
                <Divider className='my-5' />
                <Text className='mb-4'>Benefits of having api access:</Text>
                <Text className='mb-1'>- Live prices in your app</Text>
                <Text className='mb-1'>- Automatic take profit and stop loss</Text>
                <Text className='mb-1'>- Just add your signals and forget it!</Text>
                <Text className='mb-1'>- Live news</Text>

                <div className='mt-5' />
                <Text>
                  <Button className='btn-app'>
                    <a href='https://t.me/codememory' target='_blank'>
                      Contact us on telegram
                    </a>
                  </Button>
                </Text>
              </div>
            )}
          </Container>
        </Page>
      </Layout>
    </AuthGuard>
  );
}
