import { path } from 'vuepress/utils'
import { defaultTheme } from '@vuepress/theme-default'

export const ideaspacesTheme = (options = {}) => {
  return {
    name: 'vuepress-theme-ideaspaces',
    extends: defaultTheme(options),
    clientConfigFile: path.resolve(__dirname, './client.js'),
  }
}

export default ideaspacesTheme