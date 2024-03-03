import { Image, useMantineColorScheme } from '@mantine/core';

export function AppLogo() {
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();
  return <img src={colorScheme == 'dark' ? '/svg/logo-white.svg' : '/svg/logo-black.svg'} width={140} height={60} className='' />;
}
