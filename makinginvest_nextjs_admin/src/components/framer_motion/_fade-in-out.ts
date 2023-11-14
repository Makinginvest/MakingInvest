export function fadeInOut(type: string = 'easeInOut', duration: number = 0.3) {
  return {
    animate: {
      opacity: 1,
      scale: 1,
      transition: { type, duration }
    },
    initial: {
      opacity: 0,
      scale: 1.02,
      transition: { type, duration }
    }
  };
}
