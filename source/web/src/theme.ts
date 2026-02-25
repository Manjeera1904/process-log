import { createSuperNovaTheme, lightTheme } from 'supernova-core'

const primaryColor = '#802629'
const primaryLight = '#8026290a'
const secondaryColor = '#ffffff'
const accentColor = 'rgb(242 104 42 / 1)'
const borderColor = '#8026291f'

const theme = createSuperNovaTheme({
  ...lightTheme,
  palette: {
    mode: 'light',
    primary: {
      main: primaryColor,
      light: primaryLight,
      contrastText: '#ffffff',
    },
    secondary: {
      main: secondaryColor,
      contrastText: '#222222',
    },
    error: {
      main: '#AA1B04',
      dark: '#802629',
      light: '#FDECEA',
      contrastText: '#ffffff',
    },
    warning: {
      main: '#F2682A',
      light: '#FFF4E5',
      dark: '#C25B1E',
      contrastText: '#222222',
    },
    info: {
      main: '#0288d1',
      light: '#E3F2FD',
      dark: '#01579B',
      contrastText: '#ffffff',
    },
    success: {
      main: '#037E28',
      light: '#E6F4EA',
      dark: '#025C1F',
      contrastText: '#ffffff',
    },
    divider: borderColor,
    background: {
      default: '#f9f9f9',
      paper: '#ffffff',
    },
    text: {
      primary: '#222222',
      secondary: '#555555',
      disabled: '#999999',
    },
  },
  typography: {
    fontSize: 14,
    fontFamily: '"Roboto", sans-serif',

    h1: { fontSize: '2rem' },
    h2: { fontSize: '1.75rem' },
    h3: { fontSize: '1.5rem' },
    h4: { fontSize: '1.25rem' },
    h5: { fontSize: '1rem' },
    h6: { fontSize: '0.875rem' },
    body1: { fontSize: '1rem' },
    body2: { fontSize: '0.875rem' },
  },
  components: {
    ...lightTheme.components,
    MuiAppBar: {
      styleOverrides: {
        colorPrimary: {
          backgroundColor: primaryColor,
        },
      },
    },
    MuiSwitch: {
      styleOverrides: {
        switchBase: {
          color: '#ccc',
        },
        colorPrimary: {
          '&.Mui-checked': {
            color: accentColor,
          },
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        root: {
          overflow: 'hidden',
        },
        paper: {
          'position': 'inherit',
          'height': '100vh',
          '&::-webkit-overflow-scrolling': 'unset',
        },
      },
    },
  },
})

export default theme
export { accentColor }
