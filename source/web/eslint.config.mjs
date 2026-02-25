import antfu from '@antfu/eslint-config'

import i18next from 'eslint-plugin-i18next'

export const config = [
  {
    formatters: true,
    react: true,
    ignores: ['.azuredevops', '.azure-pipelines'],
  },
  {
    rules: {
      'react-refresh/only-export-components': 'off',
    },
  },
  i18next.configs['flat/recommended'],
]

export default antfu(...config)
