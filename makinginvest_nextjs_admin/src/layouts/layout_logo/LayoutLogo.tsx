import { AppShell, Burger, Header, MediaQuery, useMantineTheme } from '@mantine/core';
import Link from 'next/link';
import { useState } from 'react';
import { AppLogo } from '../../components/others/AppLogo';

import { useFirestoreStoreAdmin } from '../../models_store/firestore_store_admin';

type Props = {
  children: React.ReactNode;
};

export default function LayoutLogo({ children }: Props) {
  const { isAuthenticated, isInitialized } = useFirestoreStoreAdmin((state) => state);

  const theme = useMantineTheme();
  const [opened, setOpened] = useState(false);

  if (!isInitialized) return <div />;

  return (
    <AppShell
      className='bg-white dark:bg-[#1B1C1E] overflow-x-hidden'
      navbarOffsetBreakpoint='md'
      header={
        <Header height={55} p='md'>
          <div style={{ display: 'flex', alignItems: 'center', height: '100%' }}>
            <Link href={isAuthenticated ? '/' : '/'}>
              <AppLogo />
            </Link>
            <div className='flex-grow' />

            <MediaQuery largerThan='md' styles={{ display: 'none' }}>
              <Burger opened={opened} onClick={() => setOpened((o) => !o)} size='sm' color={theme.colors.gray[6]} />
            </MediaQuery>
          </div>
        </Header>
      }>
      {children}
    </AppShell>
  );
}
