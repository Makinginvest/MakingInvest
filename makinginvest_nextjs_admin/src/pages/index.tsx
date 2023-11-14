import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useFirestoreStoreAdmin } from '../models_store/firestore_store_admin';

export default function Index() {
  const { isAuthenticated, isInitialized } = useFirestoreStoreAdmin((state) => state);

  const router = useRouter();

  function getRouter() {
    if (!isInitialized) return;
    if (isAuthenticated) return router.push('/dashboard');
    if (!isAuthenticated) return router.push('/signin');
  }

  useEffect(() => {
    getRouter();
  }, [isAuthenticated, isInitialized]);

  return <div></div>;
}
