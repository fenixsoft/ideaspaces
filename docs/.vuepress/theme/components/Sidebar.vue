<template>
  <aside class="sidebar">
    <!-- 使用默认主题的侧边栏组件 -->
    <VPSidebar />
  </aside>
</template>

<script setup>
import VPSidebar from '@theme/VPSidebar.vue'
</script>

<style lang="scss" scoped>
.sidebar {
  position: fixed;
  top: 64px;
  left: 0;
  bottom: 0;
  width: 280px;
  background: #FFFFFF;
  border-right: 1.5px solid #E4E4E7;
  overflow-y: auto;
}

// 覆盖默认主题的样式 - 与 pencil 设计稿一致
:deep(.vp-sidebar) {
  padding: 24px 16px;
  background: transparent;
  border: none;
}

:deep(.vp-sidebar-group) {
  margin-bottom: 8px;
}

:deep(.vp-sidebar-group-title) {
  font-size: 14px;
  font-weight: 600;
  color: #71717A;
  letter-spacing: 1px;
  text-transform: uppercase;
  padding: 0 12px;
  margin-bottom: 16px;
}

:deep(.vp-sidebar-item) {
  display: flex;
  align-items: center;
  padding: 12px;
  margin: 4px 0;
  border-radius: 8px;
  color: #71717A;
  font-size: 14px;
  font-weight: 400;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  transition: all 0.2s ease;

  &:hover {
    color: #18181B;
    background: #FAFAFA;
  }

  &.active {
    color: #2563EB;
    font-weight: 500;
    background: #EFF6FF;
  }
}
</style>