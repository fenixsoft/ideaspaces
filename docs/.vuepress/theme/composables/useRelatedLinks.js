import { useSidebarItems } from '@theme/useSidebarItems'
import { useThemeLocaleData } from '@theme/useThemeData'
import { computed } from 'vue'
import { resolveRoute, usePageFrontmatter, useRoute } from 'vuepress/client'
import { isPlainObject, isString } from 'vuepress/shared'

/**
 * 从路由解析 AutoLink 属性
 */
const getAutoLink = (config, currentPath) => {
  const { notFound, meta, path } = resolveRoute(config, currentPath)
  return notFound
    ? { text: path, link: path }
    : {
        text: meta.title || path,
        link: path,
      }
}

/**
 * 将 sidebar items 扁平化为一维数组，保留所有可链接项
 * 过滤掉锚点链接（以 # 开头），只保留真正的页面链接
 * 这样可以实现跨组导航
 */
const flattenSidebarItems = (sidebarItems, result = []) => {
  for (const item of sidebarItems) {
    // 如果有 link 且不是锚点，添加到结果
    if (item.link && !item.link.startsWith('#')) {
      result.push(item)
    }
    // 如果有 prefix 且是有效路由且不是锚点，也添加
    if ('prefix' in item && !item.prefix?.startsWith('#') && !resolveRoute(item.prefix).notFound) {
      result.push({
        ...item,
        link: item.prefix,
      })
    }
    // 递归处理 children
    if ('children' in item && item.children) {
      flattenSidebarItems(item.children, result)
    }
  }
  return result
}

/**
 * 从 frontmatter 配置解析 prev/next
 */
const resolveFromFrontmatterConfig = (config, currentPath) => {
  if (config === false) {
    return false
  }
  if (isString(config)) {
    return getAutoLink(config, currentPath)
  }
  if (isPlainObject(config)) {
    return {
      ...config,
      link: getAutoLink(config.link, currentPath).link,
    }
  }
  return null
}

/**
 * 从扁平化的 sidebar items 中查找 prev/next
 * 支持跨组导航
 */
const resolveFromFlattenedSidebar = (flattenedItems, currentPath, offset) => {
  const linkIndex = flattenedItems.findIndex((item) => item.link === currentPath)
  if (linkIndex !== -1) {
    const targetItem = flattenedItems[linkIndex + offset]
    if (!targetItem) return null
    if (targetItem.link) return targetItem
    return null
  }
  return null
}

/**
 * 自定义的 useRelatedLinks，实现跨组导航
 * 通过扁平化 sidebar items，让 Next 可以跨组链接
 */
export const useRelatedLinks = () => {
  const frontmatter = usePageFrontmatter()
  const themeLocale = useThemeLocaleData()
  const sidebarItems = useSidebarItems()
  const route = useRoute()

  // 扁平化 sidebar items，实现跨组导航
  const flattenedItems = computed(() => flattenSidebarItems(sidebarItems.value))

  const prevLink = computed(() => {
    const prevConfig = resolveFromFrontmatterConfig(frontmatter.value.prev, route.path)
    return prevConfig === false
      ? null
      : (prevConfig ??
          (themeLocale.value.prev === false
            ? null
            : resolveFromFlattenedSidebar(flattenedItems.value, route.path, -1)))
  })

  const nextLink = computed(() => {
    const nextConfig = resolveFromFrontmatterConfig(frontmatter.value.next, route.path)
    return nextConfig === false
      ? null
      : (nextConfig ??
          (themeLocale.value.next === false
            ? null
            : resolveFromFlattenedSidebar(flattenedItems.value, route.path, 1)))
  })

  return {
    prevLink,
    nextLink,
  }
}