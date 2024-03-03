import { NextApiRequest, NextApiResponse } from 'next/types';

function handler(req: NextApiRequest, res: NextApiResponse) {
  res.status(200).json({ name: 'A server lives here' });
}
