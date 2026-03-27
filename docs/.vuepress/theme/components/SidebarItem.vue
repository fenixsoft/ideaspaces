<template>
  <li>
    <!-- 有链接的项目 -->
    <div v-if="item.link" class="sidebar-link-wrapper">
      <RouterLink
        :to="item.link"
        class="sidebar-link"
        :class="{ active: isActive, heading: depth === 0 }"
      >
        {{ item.text }}
      </RouterLink>
      <!-- 当前页面激活时显示展开/收起按钮 -->
      <button
        v-if="isActive && pageHeaders.length > 0"
        class="toggle-btn"
        @click="toggleHeaders"
      >
        <span class="arrow" :class="showHeaders ? 'down' : 'right'" />
      </button>
    </div>

    <!-- 无链接的分组标题 -->
    <p
      v-else
      class="sidebar-heading"
      :class="{ collapsible: item.collapsible }"
      @click="toggleOpen"
    >
      {{ item.text }}
      <span v-if="item.collapsible" class="arrow" :class="isOpen ? 'down' : 'right'" />
    </p>

    <!-- 配置中的子菜单 -->
    <ul v-if="hasConfigChildren" v-show="isOpen || !item.collapsible" class="sidebar-children">
      <SidebarItem
        v-for="child in item.children"
        :key="child.text + child.link"
        :item="child"
        :depth="depth + 1"
      />
    </ul>

    <!-- 当前页面的标题大纲 -->
    <ul v-if="isActive && pageHeaders.length > 0 && showHeaders" class="sidebar-headers">
      <li v-for="header in pageHeaders" :key="header.link">
        <RouterLink :to="header.link" class="header-link" :class="{ active: isHeaderActive(header.link) }">
          {{ header.text }}
        </RouterLink>
        <!-- 嵌套标题 -->
        <ul v-if="header.children && header.children.length" class="sidebar-headers nested">
          <li v-for="subHeader in header.children" :key="subHeader.link">
            <RouterLink :to="subHeader.link" class="header-link nested" :class="{ active: isHeaderActive(subHeader.link) }">
              {{ subHeader.text }}
            </RouterLink>
          </li>
        </ul>
      </li>
    </ul>
  </li>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vuepress/client'
import { useHeaders } from '@theme/useSidebarItems'

const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  depth: {
    type: Number,
    default: 0
  }
})

const route = useRoute()
const headers = useHeaders()

// 是否有配置中的子菜单
const hasConfigChildren = computed(() => props.item.children && props.item.children.length > 0)

// 是否激活（当前页面）
const isActive = computed(() => {
  if (props.item.link) {
    // 规范化路径比较
    const itemPath = props.item.link.replace(/\.html$/, '/').replace(/\/$/, '')
    const routePath = route.path.replace(/\.html$/, '/').replace(/\/$/, '')
    return itemPath === routePath
  }
  return false
})

// 获取当前页面的标题
const pageHeaders = computed(() => {
  if (!isActive.value) return []
  // 跳过 h1，从 h2 开始
  const allHeaders = headers.value || []
  if (allHeaders.length > 0 && allHeaders[0].level === 1) {
    return allHeaders[0].children || []
  }
  return allHeaders
})

// 是否显示标题大纲
const showHeaders = ref(true)

// 是否默认展开
const isOpenDefault = computed(() => {
  if (props.item.collapsible) {
    return checkActiveInChildren(props.item.children, route.path)
  }
  return true
})

const isOpen = ref(isOpenDefault.value)

// 监听路由变化
watch(() => route.path, () => {
  isOpen.value = isOpenDefault.value
  showHeaders.value = true
})

function toggleOpen() {
  if (props.item.collapsible) {
    isOpen.value = !isOpen.value
  }
}

function toggleHeaders() {
  showHeaders.value = !showHeaders.value
}

function checkActiveInChildren(children, path) {
  if (!children) return false
  for (const child of children) {
    if (child.link) {
      const childPath = child.link.replace(/\.html$/, '/').replace(/\/$/, '')
      const currentPath = path.replace(/\.html$/, '/').replace(/\/$/, '')
      if (childPath === currentPath) return true
    }
    if (child.children && checkActiveInChildren(child.children, path)) return true
  }
  return false
}

// 检查标题是否激活
function isHeaderActive(headerLink) {
  return route.path + route.hash === headerLink
}
</script>

<style lang="scss" scoped>
.sidebar-heading {
  margin: 0;
  padding: 12px 16px;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: var(--c-text);
  cursor: default;

  &.collapsible {
    cursor: pointer;
    user-select: none;
  }

  .arrow {
    display: inline-block;
    margin-left: 8px;
    transition: transform 0.2s;

    &.right {
      transform: rotate(-90deg);
    }

    &.down {
      transform: rotate(0deg);
    }
  }
}

.sidebar-link-wrapper {
  display: flex;
  align-items: center;
}

.sidebar-link {
  flex: 1;
  display: block;
  padding: 12px 16px;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 400;
  color: var(--c-text-light);
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s;

  &:hover {
    color: var(--c-brand);
    background: var(--c-bg-light);
  }

  &.heading {
    font-weight: 600;
    color: var(--c-text);
  }

  &.active {
    color: var(--c-brand);
    background: var(--c-brand-light);
    font-weight: 500;
  }
}

.toggle-btn {
  padding: 4px 8px;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--c-text-light);

  .arrow {
    display: inline-block;
    transition: transform 0.2s;

    &.right {
      transform: rotate(-90deg);
    }

    &.down {
      transform: rotate(0deg);
    }
  }
}

.sidebar-children {
  list-style: none;
  padding-left: 16px;
  margin: 0;

  .sidebar-link {
    padding: 8px 16px;
    font-size: 13px;
  }
}

.sidebar-headers {
  list-style: none;
  padding-left: 32px;
  margin: 0;

  &.nested {
    padding-left: 16px;
  }
}

.header-link {
  display: block;
  padding: 6px 12px;
  font-family: 'Inter', sans-serif;
  font-size: 13px;
  font-weight: 400;
  color: var(--c-text-light);
  text-decoration: none;
  border-radius: 4px;
  transition: all 0.2s;

  &:hover {
    color: var(--c-brand);
  }

  &.active {
    color: var(--c-brand);
    font-weight: 500;
  }

  &.nested {
    font-size: 12px;
    padding: 4px 12px;
  }
}
</style>