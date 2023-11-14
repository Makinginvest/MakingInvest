import { NextApiRequest, NextApiResponse } from 'next/types';
import { authAdmin } from './firebase_admin';

export function withAuth(handler: any) {
  return async (req: NextApiRequest, res: NextApiResponse) => {
    console.log('req.query', req.query);
    console.log('req.body', req.body);
    const jsonWebToken = (req.query.jsonWebToken as string) || (req.body.jsonWebToken as string);
    if (!jsonWebToken) return res.status(400).json({ error: 'Missing jsonWebToken' });

    const decodedToken = await authAdmin.verifyIdToken(jsonWebToken);
    if (!decodedToken) return res.status(400).json({ error: 'Invalid jsonWebToken' });
    console.log('req.body', req.body);
    req.body.userId = decodedToken.user_id;
    req.body.email = decodedToken.email;

    return handler(req, res);
  };
}
