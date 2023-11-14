import { Box, Button, Grid, NativeSelect, Text, TextInput } from '@mantine/core';
import { Dropzone, IMAGE_MIME_TYPE } from '@mantine/dropzone';
import { useForm, yupResolver } from '@mantine/form';
import { showNotification } from '@mantine/notifications';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { Send } from 'tabler-icons-react';
import * as Yup from 'yup';

import { DatePicker } from '@mantine/dates';
import { AuthUserModel } from '../../models/model.authuser';
import { getFirebaseStorageDownloadUrl } from '../../models_services/firebase_image_service';
import { apiGetUser, apiUpdateUser } from '../../models_services/firestore_user_service';
import { FormError } from './_FormError';
import FormSkelenton from './_FormSkelenton';

interface IProps {
  id?: string;
  user?: AuthUserModel | null;
}

export default function UserForm({ id }: { id?: string }) {
  const [isInitLoading, setIsInitLoading] = useState(id != null ? true : false);
  const [user, setUser] = useState<AuthUserModel | null>(null);

  async function getInitData() {
    if (id) setUser(await apiGetUser(id));
    setIsInitLoading(false);
  }

  useEffect(() => {
    getInitData();
  }, []);

  if (isInitLoading) return <FormSkelenton />;
  if (!user && id) return <FormError />;

  return <Form id={id} user={user} />;
}

function Form({ id, user }: IProps) {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [file, setFile] = useState<CustomFile | null>(null);

  const handleDropFiles = (files: File[]) => {
    if (files.length > 0) {
      const file = files[0];
      setFile(Object.assign(file, { preview: URL.createObjectURL(file) }));
    }
  };

  const schema = Yup.object({
    profileImage: Yup.string(),
    subIsLifetime: Yup.string(),
    subIsLifetimeExpirationDateTime: Yup.date().nullable(),
    isAdmin: Yup.string(),
    isSuperAdmin: Yup.string(),
    username: Yup.string()
  });

  const form = useForm({
    validate: yupResolver(schema),
    initialValues: {
      isAdmin: user?.isAdmin == true ? 'Yes' : 'No',
      isSuperAdmin: user?.isSuperAdmin == true ? 'Yes' : 'No',
      subIsLifetime: user?.subIsLifetime == true ? 'Yes' : 'No',
      subIsLifetimeExpirationDateTime: user?.subIsLifetimeExpirationDateTime ?? null,
      profileImage: user?.profileImage ?? '',
      username: user?.username ?? ''
    }
  });

  const handleSubmit = async () => {
    if (form.validate().hasErrors) return;

    try {
      setIsLoading(true);
      const s = new AuthUserModel();
      s.isAdmin = form.values.isAdmin == 'Yes' ? true : false;
      s.isSuperAdmin = form.values.isSuperAdmin == 'Yes' ? true : false;
      s.subIsLifetime = form.values.subIsLifetime == 'Yes' ? true : false;
      s.subIsLifetimeExpirationDateTime = form.values.subIsLifetimeExpirationDateTime;
      s.username = form.values.username;
      s.profileImage = form.values.profileImage;

      if (file) s.profileImage = await getFirebaseStorageDownloadUrl({ file: file! });

      if (user && id) await apiUpdateUser(id, s);

      setIsLoading(false);

      router.push('/users');

      showNotification({ title: 'Success', message: 'User updated', autoClose: 6000 });
    } catch (error) {
      console.log(error);
      setIsLoading(false);
      showNotification({ color: 'red', title: 'Error', message: 'There was an error creating the announcement', autoClose: 6000 });
    }
  };

  const DropzoneRemoveImage = () => {
    const removeFile = () => {
      form.setFieldValue('image', '');
      setFile(null);
    };
    if (file || form.values.profileImage) {
      return (
        <Button className='absolute z-40 btn right-2 top-2' onClick={removeFile}>
          Remove
        </Button>
      );
    }
    return null;
  };

  const DropzoneChildren = () => {
    if (form.values.profileImage != '') {
      return (
        <Box className='relative flex justify-center'>
          <img className='h-[300px]' src={form.values.profileImage} alt='Preview' />
        </Box>
      );
    }
    if (file)
      return (
        <Box className='relative flex justify-center'>
          <img className='h-[300px]' src={file.preview} alt='Preview' />
        </Box>
      );
    return (
      <Box className='min-h-[300px] pointer-events-none flex justify-center items-center text-center'>
        <div>
          <Text size='xl' inline>
            Drag images here or click to select files
          </Text>
          <Text size='sm' color='dimmed' inline mt={7}>
            Attach as many files as you like, each file should not exceed 5mb
          </Text>
        </div>
      </Box>
    );
  };

  return (
    <Box className=''>
      <Grid align={'start'}>
        <Grid.Col md={12} xs={12}>
          <Box className='relative'>
            <DropzoneRemoveImage />
            <Dropzone
              className='z-0 p-2 mt-8'
              multiple={false}
              disabled={file != null || form.values.profileImage != ''}
              onDrop={handleDropFiles}
              onReject={(files) => console.log('rejected files', files)}
              maxSize={3 * 1024 ** 2}
              accept={IMAGE_MIME_TYPE}
            >
              <DropzoneChildren />
            </Dropzone>
          </Box>

          <NativeSelect
            className='mt-4'
            placeholder='Superadmin?'
            label='Superadmin?'
            data={['Yes', 'No']}
            {...form.getInputProps('isSuperAdmin')}
          />
          <NativeSelect className='mt-4' placeholder='Admin?' label='Admin?' data={['Yes', 'No']} {...form.getInputProps('isAdmin')} />
          <NativeSelect
            className='mt-4'
            placeholder='Lifetime sub?'
            label='Lifetime sub?'
            data={['Yes', 'No']}
            {...form.getInputProps('subIsLifetime')}
          />

          <DatePicker
            className='col-span-1'
            label='Lifetime sub end date (Leave blank if the subscription never expires)'
            {...form.getInputProps('subIsLifetimeExpirationDateTime')}
          />

          <TextInput className='mt-4' placeholder='Title' label='Username' {...form.getInputProps('username')} />
        </Grid.Col>

        <Grid.Col md={12} xs={12}>
          <Box>
            <Button
              onClick={handleSubmit}
              leftIcon={<Send size={14} />}
              variant='filled'
              className='w-full mt-10 text-black transition border-0 bg-app-yellow hover:bg-opacity-90'
            >
              Submit
            </Button>
          </Box>
        </Grid.Col>
      </Grid>
    </Box>
  );
}

export interface CustomFile extends File {
  path?: string;
  preview?: string;
}
