import { defineClientConfig } from 'vuepress/client'
import { setupHeaders, setupSidebarItems } from '@theme/useSidebarItems'
import { setupDarkMode } from '@theme/useDarkMode'
import Layout from './layouts/Layout.vue'
import Navbar from './components/Navbar.vue'
import Sidebar from './components/Sidebar.vue'
import Home from './components/Home.vue'
import './styles/index.scss'

export default defineClientConfig({
  layouts: {
    Layout,
  },
  enhance({ app }) {
    // 注册全局组件
    app.component('Navbar', Navbar)
    app.component('Sidebar', Sidebar)
    app.component('Home', Home)
  },
  setup() {
    // 初始化默认主题的功能
    setupDarkMode()
    setupHeaders()
    setupSidebarItems()
  },
})