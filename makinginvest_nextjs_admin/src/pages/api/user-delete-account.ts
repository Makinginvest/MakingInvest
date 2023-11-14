import { NextApiRequest, NextApiResponse } from 'next/types';
import { authAdmin, firestoreAdmin } from '../../_firebase/firebase_admin';
import { withAuth } from '../../_firebase/firebase_admin_auth';

async function handler(req: NextApiRequest, res: NextApiResponse) {
  const userId = req.body.userId;
  const email = req.body.email;

  if (req.method === 'PATCH' || req.method === 'POST') {
    try {
      const user = await authAdmin.getUser(userId);
      if (!user) return res.status(400).json({ error: 'User not found' });

      await authAdmin.deleteUser(userId);
      await firestoreAdmin.collection('users').doc(userId).delete();

      res.json({ message: 'User deleted' });
    } catch (error: any) {
      res.status(400).json({ message: error.message });
    }
  }
}

export default withAuth(handler);
