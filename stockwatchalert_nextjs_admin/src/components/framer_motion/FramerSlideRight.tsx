import { m } from 'framer-motion';

interface Props {
  children: React.ReactNode;
  duration?: number;
  delay?: number;
  type?: string;
  className?: string;
  id?: string;
}

export function FramerSlideRight({ children, duration = 0.5, type = 'easeInOut', className = '', delay = 0, id }: Props) {
  return (
    <m.div
      id={id}
      className={className}
      initial='initial'
      whileInView='animate'
      viewport={{ once: true }}
      transition={{ duration: duration, type: type, delay: delay }}
      variants={{
        animate: { x: 0, opacity: 1 },
        initial: { x: -50, opacity: 0 }
      }}>
      {children}
    </m.div>
  );
}
