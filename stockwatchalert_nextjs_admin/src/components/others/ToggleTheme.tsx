import { Box, Group, Switch, useMantineColorScheme, useMantineTheme } from '@mantine/core';
import { IconMoonStars, IconSun } from '@tabler/icons';

type Props = {
  classname?: string;
};

export function ToggleTheme({ classname }: Props) {
  const { colorScheme, toggleColorScheme } = useMantineColorScheme();
  const theme = useMantineTheme();

  return (
    <Group className={`flex items-center ${classname}`}>
      <Switch
        className='mb-3 p-0'
        checked={colorScheme === 'dark'}
        onChange={() => toggleColorScheme()}
        size='lg'
        color={theme.colorScheme === 'dark' ? 'gray' : 'dark'}
        onLabel={<IconSun size={24} stroke={2.5} color={theme.colors.yellow[4]} />}
        offLabel={<IconMoonStars size={24} stroke={2.5} color={theme.colors.blue[6]} />}
      />
    </Group>
  );
}
