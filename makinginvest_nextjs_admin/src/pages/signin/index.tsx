import { Container } from '@mantine/core';
import { GetStaticProps } from 'next';
import SignInForm from '../../components/forms/SignInForm';
import SignUpForm from '../../components/forms/SignUpForm';
import Page from '../../components/others/Page';
import Layout from '../../layouts';
import { firestoreAdmin } from '../../_firebase/firebase_admin';

interface Props {
  isSuperAdminConfigured?: boolean | null | undefined;
}

export default function SignInPage({ isSuperAdminConfigured }: Props) {
  return (
    <Layout variant='logoOnly'>
      <Page title='Signin'>
        <Container size='xl' className='flex items-center justify-center'>
          {isSuperAdminConfigured && <SignInForm />}
          {!isSuperAdminConfigured && <SignUpForm />}
        </Container>
      </Page>
    </Layout>
  );
}

export async function getServerSideProps(context: GetStaticProps) {
  try {
    const appControl = await firestoreAdmin.collection('appControlsPrivate').doc('appControlsPrivate').get();
  } catch (error) {
    console.log(error);
  }
  const appControl = await firestoreAdmin.collection('appControlsPrivate').doc('appControlsPrivate').get();

  const isSuperAdminConfigured = appControl.data()?.isSuperAdminConfigured || false;

  return {
    props: {
      isSuperAdminConfigured: isSuperAdminConfigured
    }
  };
}
