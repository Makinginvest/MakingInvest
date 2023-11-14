import { Button, Container, TextInput } from '@mantine/core';
import { useForm, yupResolver } from '@mantine/form';
import { showNotification } from '@mantine/notifications';

import { useEffect, useState } from 'react';
import { Send } from 'tabler-icons-react';
import * as Yup from 'yup';
import { AppControlsPublicModel } from '../../models/model.app_controls';
import {
  apiGetAppControlsPublic,
  apiUpdateAppControlsPublic,
  apiUpdateAppControlsPublicLinks
} from '../../models_services/firestore_appcontrols_service';

import FormSkelenton from './_FormSkelenton';

interface IProps {
  links: AppControlsPublicModel | null;
}

export default function LinksForm() {
  const [isInitLoading, setIsInitLoading] = useState(true);
  const [linksModel, setLinkModel] = useState<AppControlsPublicModel | null>(null);

  async function getInitData() {
    setLinkModel(await apiGetAppControlsPublic());
    setIsInitLoading(false);
  }

  useEffect(() => {
    getInitData();
  }, []);

  if (isInitLoading) return <FormSkelenton />;
  return <Form links={linksModel} />;
}

function Form({ links: smtp }: IProps) {
  const [isLoading, setIsLoading] = useState(false);

  const schema = Yup.object({
    googlePlay: Yup.string().url(),
    appStore: Yup.string().url(),
    facebook: Yup.string().url(),
    instagram: Yup.string().url(),
    twitter: Yup.string().url(),
    youtube: Yup.string().url(),
    telegram: Yup.string().url(),
    whatsapp: Yup.string().url(),
    support: Yup.string().url(),
    terms: Yup.string().url(),
    privacy: Yup.string().url()
  });

  const form = useForm({
    validate: yupResolver(schema),

    initialValues: {
      googlePlay: smtp?.linkGooglePlay || '',
      appStore: smtp?.linkAppStore || '',
      facebook: smtp?.linkFacebook || '',
      instagram: smtp?.linkInstagram || '',
      twitter: smtp?.linkTwitter || '',
      youtube: smtp?.linkYoutube || '',
      telegram: smtp?.linkTelegram || '',
      whatsapp: smtp?.linkWhatsapp || '',
      support: smtp?.linkSupport || '',
      terms: smtp?.linkTerms || '',
      privacy: smtp?.linkPivacy || ''
    }
  });

  const handleSubmit = async () => {
    if (form.validate().hasErrors) return;

    try {
      setIsLoading(true);
      const x = new AppControlsPublicModel();
      x.linkGooglePlay = form.values.googlePlay;
      x.linkAppStore = form.values.appStore;
      x.linkFacebook = form.values.facebook;
      x.linkInstagram = form.values.instagram;
      x.linkTwitter = form.values.twitter;
      x.linkYoutube = form.values.youtube;
      x.linkTelegram = form.values.telegram;
      x.linkWhatsapp = form.values.whatsapp;
      x.linkSupport = form.values.support;
      x.linkTerms = form.values.terms;
      x.linkPivacy = form.values.privacy;

      await apiUpdateAppControlsPublicLinks(x);

      setIsLoading(false);

      showNotification({ color: 'blue', title: 'Success', message: 'Links updated', autoClose: 6000 });
    } catch (error: any) {
      setIsLoading(false);
      showNotification({
        color: 'red',
        title: 'Error',
        message: error.message,
        autoClose: 6000
      });
    }
  };

  // 5 mega bytes

  return (
    <Container p={0}>
      <div className='mt-4'>
        <TextInput className='mt-4' placeholder='Terms' label='Terms' maxLength={50} {...form.getInputProps('terms')} />
        <TextInput className='mt-4' placeholder='Privacy' label='Privacy' maxLength={50} {...form.getInputProps('privacy')} />
        <TextInput className='mt-4' placeholder='Google Play' label='Google Play' maxLength={50} {...form.getInputProps('googlePlay')} />
        <TextInput className='mt-4' placeholder='App Store' label='App Store' maxLength={50} {...form.getInputProps('appStore')} />
        <TextInput className='mt-4' placeholder='Facebook' label='Facebook' maxLength={50} {...form.getInputProps('facebook')} />
        <TextInput className='mt-4' placeholder='Instagram' label='Instagram' maxLength={50} {...form.getInputProps('instagram')} />
        <TextInput className='mt-4' placeholder='Twitter' label='Twitter' maxLength={50} {...form.getInputProps('twitter')} />
        <TextInput className='mt-4' placeholder='Youtube' label='Youtube' maxLength={50} {...form.getInputProps('youtube')} />
        <TextInput className='mt-4' placeholder='Telegram' label='Telegram' maxLength={50} {...form.getInputProps('telegram')} />
        <TextInput className='mt-4' placeholder='Whatsapp' label='Whatsapp' maxLength={50} {...form.getInputProps('whatsapp')} />
        <TextInput className='mt-4' placeholder='Support' label='Support' maxLength={50} {...form.getInputProps('support')} />
      </div>
      <Button
        onClick={handleSubmit}
        leftIcon={<Send size={14} />}
        variant='filled'
        disabled={isLoading}
        className='w-full mt-4 h-[40px] bg-app-primary text-white border-0 hover:opacity-90 hover:text-md'>
        Submit
      </Button>
    </Container>
  );
}
