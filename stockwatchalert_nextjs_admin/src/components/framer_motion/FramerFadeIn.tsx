import { m } from 'framer-motion';

interface Props {
  children: React.ReactNode;
  duration?: number;
  delay?: number;
  type?: string;
  className?: string;
  id?: string;
}

export function FramerFadeIn({ children, duration = 0.5, type = 'easeInOut', className = '', delay = 0, id }: Props) {
  return (
    <m.div
      id={id}
      className={className}
      initial='initial'
      whileInView='animate'
      viewport={{ once: true }}
      transition={{ duration: duration, type: type, delay: delay }}
      variants={{
        animate: { opacity: 1, scale: 1 },
        initial: { opacity: 0, scale: 1.02 }
      }}>
      {children}
    </m.div>
  );
}
