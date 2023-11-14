import dynamic from 'next/dynamic';
import styles from './RichTextEditor.module.scss';

const RTE = dynamic(() => import('@mantine/rte'), {
  ssr: false,
  loading: () => null
});

export function RichTextEditor({ ...props }) {
  return <RTE {...props} className={`${styles.rte} ${props.className} min-h-[500px] post-dangerously`} placeholder='Write something...' />;
}
