import { m } from 'framer-motion';

interface Props {
  children: React.ReactNode;
  duration?: number;
  type?: string;
  delay?: number;
  className?: string;
}

export function FramerStaggered({ children, duration = 0.5, type = 'easeInOut', delay = 0.03, className = '' }: Props) {
  return (
    <m.div
      className={className}
      initial='initial'
      whileInView='animate'
      viewport={{ once: true }}
      transition={{ duration: duration, type: type, delay: delay }}
      variants={{
        initial: { opacity: 0, translateX: -50 },
        animate: { opacity: 1, translateX: 0 }
      }}>
      {children}
    </m.div>
  );
}
