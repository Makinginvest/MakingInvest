import { NextApiRequest, NextApiResponse } from 'next/types';
import * as nodemailer from 'nodemailer';
import { firestoreAdmin } from '../../_firebase/firebase_admin';

async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    try {
      const { email, name, message } = req.body;
      if (!email || !name || !message) res.status(400).json({ message: 'Missing required fields' });

      let querySmtp = await firestoreAdmin.collection('appControlsPrivate').doc('smtp').get();
      let smtp = querySmtp.data() || null;
      if (!smtp) res.status(500).json({ message: 'Missing SMTP credentials' });
      if (!smtp!.email || !smtp!.password || !smtp!.host || !smtp!.port) res.status(500).json({ message: 'Missing SMTP credentials' });

      let queryAppName = await firestoreAdmin.collection('appControlsPublic').doc('appInfo').get();
      let appName = queryAppName.data()?.name || 'MakingInvest';

      const mailBody = `
      <div>
        <h2>${appName} Contact Form</h2>
        <p>Name: ${name}</p>
        <p>Email: ${email}</p>
        <p>Message: ${message}</p>
      </div>
    `;

      const emails = [smtp!.email];

      sendMail(emails, mailBody, `${appName} Contact Form`, smtp, appName);
      res.status(200).send('Sent!');
    } catch (error: any) {
      res.status(500).json({ message: error.message });
    }
  }
}

async function sendMail(emailAddresses: string[], mailBody: string, subject: string, smtp: any, appName: string) {
  const transporter = nodemailer.createTransport({
    host: smtp.host,
    port: Number(smtp.port),
    secure: true,
    auth: {
      user: `${smtp.email}`,
      pass: `${smtp.password}`
    }
  });

  const mailOptions = {
    from: `Contact alert for ${appName} <${smtp.email}>`,
    to: `${emailAddresses}`,
    subject: `${subject}`,
    html: `${mailBody}`
  };

  transporter.sendMail(mailOptions, (error: any, data: any) => {
    if (error) console.log(error);
    if (!error) console.log('Sent!');
  });
}

export default handler;
