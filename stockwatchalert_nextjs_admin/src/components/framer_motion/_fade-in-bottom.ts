export function fadeInBottom(type: string = 'spring', duration: number = 0.5) {
  return {
    animate: {
      y: 0,
      opacity: 1,
      transition: { type, duration }
    },
    initial: {
      y: 80,
      opacity: 0,
      transition: { type, duration }
    }
  };
}

export function fadeInBottomWithScaleX(type: string = 'spring', duration: number = 0.5) {
  return {
    animate: {
      y: 0,
      scaleX: 1,
      opacity: 1,
      transition: { type, duration }
    },
    initial: {
      y: 80,
      scaleX: 0.7,
      opacity: 0,
      transition: { type, duration }
    }
  };
}

export function fadeInBottomWithScaleY(type: string = 'easeInOut', duration: number = 0.4, delay: number = 0.05) {
  return {
    animate: {
      y: 0,
      scaleY: 1,
      opacity: 1,
      transition: { type, duration, delay }
    },
    initial: {
      y: '100%',
      scaleY: 0,
      opacity: 0,
      transition: { type, duration, delay }
    }
  };
}
