import { ActionIcon, Box, Divider, Menu, useMantineColorScheme } from '@mantine/core';
import { ArrowsLeftRight, Settings, User } from 'tabler-icons-react';
import { signOut } from '../../models_services/firebase_auth_services';

export function AuthMenu() {
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();
  return (
    <Box className='flex items-center mr-2'>
      <Menu shadow='md' width={200}>
        <Menu.Target>
          <ActionIcon>
            <User />
          </ActionIcon>
        </Menu.Target>

        <Menu.Dropdown>
          <Menu.Label>Profile</Menu.Label>
          <Divider />

          <Menu.Item className='mt-2' icon={<ArrowsLeftRight size={14} />} onClick={() => toggleColorScheme()}>
            Switch Theme
          </Menu.Item>
          <Menu.Item className='mt-2 mb-2' color='red' icon={<Settings size={14} />} onClick={() => signOut()}>
            Sign out
          </Menu.Item>
        </Menu.Dropdown>
      </Menu>
    </Box>
  );
}

// className='flex items-center mr-2'
