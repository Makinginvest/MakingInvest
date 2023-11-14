import { useRouter } from 'next/router';
import { ReactNode, useEffect, useState } from 'react';
import { useFirestoreStoreAdmin } from '../models_store/firestore_store_admin';
import NoAccessPage from '../pages/no-access';

type Props = {
  children: ReactNode;
};

export default function AuthGuard({ children }: Props) {
  const { pathname, push } = useRouter();
  const [requestedLocation, setRequestedLocation] = useState<string | null>(null);

  const { isAuthenticated, isInitialized, authUser } = useFirestoreStoreAdmin((state) => state);

  useEffect(() => {
    if (requestedLocation && pathname !== requestedLocation) {
      setRequestedLocation(null);
      push(requestedLocation);
    }
  }, [pathname, push, requestedLocation]);

  if (!isInitialized) return <div />;

  if (pathname.includes('/reset-password')) {
    if (pathname !== requestedLocation) setRequestedLocation(pathname);
    push('/reset-password');
    return <div />;
  }

  if (!isAuthenticated && pathname.includes('/signin')) {
    if (pathname !== requestedLocation) setRequestedLocation(pathname);
    push('/signin');
    return <div />;
  }

  if (!isAuthenticated) {
    push('/signin');
    return <div />;
  }

  if (isAuthenticated && (authUser?.isSuperAdmin === true || authUser?.isAdmin === true || authUser?.isTestAdmin === true)) {
    return <>{children}</>;
  }

  if (isAuthenticated && authUser?.isSuperAdmin === false && authUser?.isAdmin === false && authUser?.isTestAdmin === false) {
    return <NoAccessPage />;
  }

  return <div />;
}
