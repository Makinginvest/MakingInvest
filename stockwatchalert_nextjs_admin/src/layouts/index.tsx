import { ReactNode } from 'react';
import LayoutAdmin from './layout_admin/LayoutAdmin';
import LayoutLogo from './layout_logo/LayoutLogo';

type Props = {
  children: ReactNode;
  variant?: 'logoOnly' | 'admin';
};

export default function Layout({ children, variant = 'admin' }: Props) {
  if (variant === 'logoOnly') return <LayoutLogo>{children}</LayoutLogo>;
  if (variant === 'admin') return <LayoutAdmin>{children}</LayoutAdmin>;
  return <LayoutAdmin>{children}</LayoutAdmin>;
}
