module.exports = {
  important: true,
  corePlugins: {
    preflight: true
  },
  darkMode: 'class',
  mode: 'jit',
  content: [
    './src/components/**/*.{js,ts,jsx,tsx}',
    './src/layouts/**/*.{js,ts,jsx,tsx}',
    './src/forms/**/*.{js,ts,jsx,tsx}',
    './src/pages/**/*.{js,ts,jsx,tsx}',
    './src/pages_sections/**/*.{js,ts,jsx,tsx}'
  ],
  theme: {
    screens: {
      xs: { min: '0px' },
      sm: { min: '768px' },
      md: { min: '992px' },
      lg: { min: '1200px' },
      xl: { min: '1400px' },
      '2xl': { min: '1600px' }
    },
    transitionDuration: {
      DEFAULT: '300ms'
    },

    extend: {
      colors: {
        app: {
          DEFAULT: '#17191D',
          dark: '#17191D',
          yellow: '#FCCF2F',
          yellowText: '#EEB00E',
          black: '#0B0E11',
          white: '#fff',
          primary: '#5927E5',
          secondary: '#C237F5',
          tertiary: '#3DBEA8',
          dark: '#1F1926',
          light: '#FFFFFF',
          error: '#CD0000'
        },
        brand: {
          DEFAULT: '#24b47e',
          dark: '#00997B',
          yellow: '#FFCA28'
        },
        light: {
          DEFAULT: '#ffffff',
          base: '#646464',
          100: '#f9f9f9',
          200: '#f2f2f2',
          300: '#ededed',
          400: '#e6e6e6',
          500: '#dadada',
          600: '#d2d2d2',
          800: '#bcbcbc',
          900: '#a8a8a8'
        },
        dark: {
          DEFAULT: '#000000',
          base: '#a5a5a5',
          100: '#17191D',
          200: '#212121',
          250: '#252525',
          300: '#2a2a2a',
          400: '#323232',
          500: '#3e3e3e',
          600: '#4a4a4a',
          700: '#6e6e6e',
          800: '#808080',
          900: '#999999'
        },
        warning: '#e66767'
      },
      boxShadow: {
        card: '0px 0px 6px rgba(79, 95, 120, 0.1)',
        dropdown: '0px 10px 32px rgba(46, 57, 72, 0.2)',
        'bottom-nav': '0 -2px 3px rgba(0, 0, 0, 0.08)'
      },
      fontSize: {
        '10px': '.625rem',
        '13px': '13px',
        '14px': '14px',
        '15px': '15px',
        '16px': '16px'
      },
      fontFamily: {
        body: ["'Inter', sans-serif"]
      }
    }
  },
  plugins: []
};
