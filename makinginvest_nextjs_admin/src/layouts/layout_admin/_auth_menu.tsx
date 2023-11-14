import { ActionIcon, Box, Divider, Menu, useMantineColorScheme } from '@mantine/core';
import { useRouter } from 'next/router';
import { ArrowsLeftRight, Settings, User } from 'tabler-icons-react';
import { signOut } from '../../models_services/firebase_auth_services';

export function AuthMenu() {
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();
  const router = useRouter();

  function handleSignOut() {
    signOut();
    router.push('/signin');
  }
  return (
    <Box className='flex items-center mr-2'>
      <Menu shadow='md' trigger='hover' openDelay={100} closeDelay={400} position='bottom-end'>
        <Menu.Target>
          <ActionIcon>
            <User />
          </ActionIcon>
        </Menu.Target>

        <Menu.Dropdown>
          <Menu.Item className='mt-2' icon={<ArrowsLeftRight size={14} />} onClick={() => toggleColorScheme()}>
            Switch Theme
          </Menu.Item>
          <Menu.Item className='mt-2 mb-2' color='red' icon={<Settings size={14} />} onClick={handleSignOut}>
            Sign out
          </Menu.Item>
        </Menu.Dropdown>
      </Menu>
    </Box>
  );
}
