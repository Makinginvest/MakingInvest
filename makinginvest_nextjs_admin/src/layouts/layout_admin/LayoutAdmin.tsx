import { AppShell, Burger, Header, MediaQuery, useMantineTheme } from '@mantine/core';
import Link from 'next/link';
import { useState } from 'react';
import { AppLogo } from '../../components/others/AppLogo';

import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';
import { AuthMenu } from './_auth_menu';
import { NavbarAdmin } from './_navbar_admin';

type Props = {
  children: React.ReactNode;
};

export default function LayoutAdmin({ children }: Props) {
  const { isAuthenticated, isInitialized } = useFirestoreStoreAdmin((state) => state);

  const theme = useMantineTheme();
  const [opened, setOpened] = useState(false);

  if (!isInitialized) return <div />;
  if (!isAuthenticated) return <div />;

  return (
    <AppShell
      className='bg-white dark:bg-[#1B1C1E] overflow-x-hidden'
      navbarOffsetBreakpoint='md'
      header={
        <Header height={55} p='md'>
          <div style={{ display: 'flex', alignItems: 'center', height: '100%' }}>
            <Link href={isAuthenticated ? '/dashboard' : '/signin'} className=''>
              <AppLogo />
            </Link>
            <div className='flex-grow' />

            <AuthMenu />

            <MediaQuery largerThan='md' styles={{ display: 'none' }}>
              <Burger opened={opened} onClick={() => setOpened((o) => !o)} size='sm' color={theme.colors.gray[6]} />
            </MediaQuery>
          </div>
        </Header>
      }
      navbar={<NavbarAdmin isOpen={opened} />}>
      {children}
    </AppShell>
  );
}
