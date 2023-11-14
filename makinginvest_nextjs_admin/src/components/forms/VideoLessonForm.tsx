import { Box, Button, Grid, NativeSelect, Text, Textarea, TextInput } from '@mantine/core';
import { Dropzone, IMAGE_MIME_TYPE } from '@mantine/dropzone';
import { useForm, yupResolver } from '@mantine/form';
import { showNotification } from '@mantine/notifications';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import { Send } from 'tabler-icons-react';
import * as Yup from 'yup';

import { VideoLessonModel } from '../../models/model.video_lesson';
import { getFirebaseStorageDownloadUrl } from '../../models_services/firebase_image_service';
import { apiCreateVideoLesson, apiGetVideoLesson, apiUpdateVideoLesson } from '../../models_services/firestore_video_lesson';
import { FormError } from './_FormError';
import FormSkelenton from './_FormSkelenton';

interface IProps {
  id?: string;
  videoLesson?: VideoLessonModel | null;
}

export default function VideoLessonForm({ id }: { id?: string }) {
  const [isInitLoading, setIsInitLoading] = useState(id != null ? true : false);
  const [videoLesson, setVideoLesson] = useState<VideoLessonModel | null>(null);

  async function getInitData() {
    if (id) setVideoLesson(await apiGetVideoLesson(id));
    setIsInitLoading(false);
  }

  useEffect(() => {
    getInitData();
  }, []);

  if (isInitLoading) return <FormSkelenton />;
  if (!videoLesson && id) return <FormError />;

  return <Form id={id} videoLesson={videoLesson} />;
}

function Form({ id, videoLesson }: IProps) {
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
    title: Yup.string().required('Required'),
    link: Yup.string().url('Invalid URL').required('Required'),
    image: Yup.string(),
    isFree: Yup.string().required('Required'),
    status: Yup.string().required('Required')
  });

  const form = useForm({
    validate: yupResolver(schema),
    initialValues: {
      title: videoLesson?.title ?? '',
      link: videoLesson?.link ?? '',
      image: videoLesson?.image ?? '',
      isFree: videoLesson?.isFree == false ? 'No' : 'Yes',
      status: videoLesson?.status ?? 'Draft'
    }
  });

  const handleSubmit = async () => {
    if (form.validate().hasErrors) return;

    try {
      setIsLoading(true);
      const s = new VideoLessonModel();
      s.title = form.values.title;
      s.link = form.values.link;
      s.timestampCreated = videoLesson?.timestampCreated ?? new Date();
      s.image = videoLesson?.image ?? '';
      s.isFree = form.values.isFree == 'Yes' ? true : false;
      s.status = form.values.status;

      if (file) s.image = await getFirebaseStorageDownloadUrl({ file: file! });

      if (!videoLesson) await apiCreateVideoLesson(s);
      if (videoLesson && id) await apiUpdateVideoLesson(id, s);

      setIsLoading(false);

      router.push('/video-lessons');

      showNotification({ title: 'Success', message: 'Video Lesson was created', autoClose: 6000 });
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
    if (file || form.values.image) {
      return (
        <Button className='absolute z-40 btn right-2 top-2' onClick={removeFile}>
          Remove
        </Button>
      );
    }
    return null;
  };

  const DropzoneChildren = () => {
    if (form.values.image != '') {
      return (
        <Box className='relative flex justify-center'>
          <img className='h-[300px]' src={form.values.image} alt='Preview' />
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
      <div className='grid grid-cols-1 md:grid-cols-2 md:gap-x-4 '>
        <NativeSelect className='' placeholder='Free?' label='Free?' data={['Yes', 'No']} {...form.getInputProps('isFree')} />
        <NativeSelect
          className=''
          placeholder='Status'
          label='Post status'
          data={['Draft', 'Published', 'Archived']}
          {...form.getInputProps('status')}
        />
      </div>
      <TextInput className='mt-4' placeholder='Title' label='Title' {...form.getInputProps('title')} />

      <TextInput className='mt-4' placeholder='Link' label='Link' {...form.getInputProps('link')} />
      <Box className='relative'>
        <DropzoneRemoveImage />
        <Dropzone
          className='z-0 p-2 mt-8'
          multiple={false}
          disabled={file != null || form.values.image != ''}
          onDrop={handleDropFiles}
          onReject={(files) => console.log('rejected files', files)}
          maxSize={3 * 1024 ** 2}
          accept={IMAGE_MIME_TYPE}>
          <DropzoneChildren />
        </Dropzone>
      </Box>

      <Box>
        <Button
          onClick={handleSubmit}
          loading={isLoading}
          leftIcon={<Send size={14} />}
          variant='filled'
          className='w-full mt-10 text-black transition border-0 bg-app-yellow hover:bg-opacity-90'>
          Submit
        </Button>
      </Box>
    </Box>
  );
}

export interface CustomFile extends File {
  path?: string;
  preview?: string;
}
