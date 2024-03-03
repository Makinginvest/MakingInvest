import { createBreakpoint } from 'react-use';

const breakPoints = {
  xs: 0,
  sm: 768,
  md: 992,
  lg: 1200,
  xl: 1400,
  '2xl': 1600
};

export const useBreakpoint = createBreakpoint(breakPoints);
