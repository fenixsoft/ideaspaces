import { defineClientConfig } from 'vuepress/client'
import { setupHeaders, setupSidebarItems } from '@theme/useSidebarItems'
import { setupDarkMode } from '@theme/useDarkMode'
import Layout from './layouts/Layout.vue'
import Preview from './layouts/Preview.vue'
import { getSiteConfig } from './utils/configMigration.js'
import { getThemeConfig } from './config/highlightThemes.js'
import './styles/index.scss'

// 各主题对应的背景色
const THEME_BG_COLORS = {
  'default': '#282C34',
  'prism': '#f5f2f0',
  'prism-coy': '#fdfdfd',
  'prism-dark': '#1d1f21',
  'prism-funky': '#000',
  'prism-okaidia': '#272822',
  'prism-solarizedlight': '#fdf6e3',
  'prism-tomorrow': '#1d1f21',
  'prism-twilight': '#141414'
}

const THEME_LINK_ID = 'prism-theme-css'

/**
 * 动态加载 PrismJS 主题 CSS
 */
function loadThemeCSS(themeId) {
  if (typeof document === 'undefined') return

  // 移除之前加载的主题
  const existingLink = document.getElementById(THEME_LINK_ID)
  if (existingLink) {
    existingLink.remove()
  }

  const themeConfig = getThemeConfig(themeId)

  // 设置主题背景色 CSS 变量
  const bgColor = THEME_BG_COLORS[themeId] || '#282C34'
  document.documentElement.style.setProperty('--code-theme-bg', bgColor)

  // 如果主题不需要加载 CSS（如默认主题），添加标记类
  if (!themeConfig.cssPath) {
    document.body.classList.add('custom-highlight-theme')
    return
  }

  // 移除自定义样式标记
  document.body.classList.remove('custom-highlight-theme')

  // 动态创建 link 元素加载 CSS
  const link = document.createElement('link')
  link.id = THEME_LINK_ID
  link.rel = 'stylesheet'
  link.type = 'text/css'

  // 使用 CDN 加载 PrismJS 主题
  const themeName = themeConfig.cssPath.replace('prismjs/themes/', '').replace('.min.css', '')
  link.href = `https://cdn.jsdelivr.net/npm/prismjs@1.29.0/themes/${themeName}.min.css`

  document.head.appendChild(link)

  console.log(`[HighlightLoader] 加载主题: ${themeConfig.name}, 背景色: ${bgColor}`)
}

/**
 * 处理配置变更事件
 */
function handleConfigChange(event) {
  const config = event.detail
  if (config && config.highlightTheme) {
    loadThemeCSS(config.highlightTheme)
  }
}

export default defineClientConfig({
  layouts: {
    Layout,
    Preview,
  },
  setup() {
    // 初始化默认主题的功能
    setupDarkMode()
    setupHeaders()
    setupSidebarItems()

    // 禁止浏览器翻译（网站本身就是中文）
    if (typeof document !== 'undefined') {
      document.documentElement.setAttribute('translate', 'no')

      // 初始化代码高亮主题
      const config = getSiteConfig()
      loadThemeCSS(config.highlightTheme || 'default')

      // 监听配置变更事件
      window.addEventListener('site-config-changed', handleConfigChange)
    }
  }
})