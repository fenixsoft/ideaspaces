<template>
  <div class="home">
    <!-- Hero 区域 -->
    <section class="hero">
      <h1 class="hero-title">{{ heroTitle }}</h1>
      <p class="hero-description">{{ heroDescription }}</p>
      <div class="hero-actions">
        <RouterLink to="/python/" class="btn btn-primary">
          开始探索
        </RouterLink>
        <RouterLink to="/arch/design" class="btn btn-secondary">
          查看文档
        </RouterLink>
      </div>
    </section>

    <!-- 功能特性 -->
    <section class="features">
      <h2 class="features-title">核心功能</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
            </svg>
          </div>
          <h3 class="feature-title">知识管理</h3>
          <p class="feature-description">基于 Markdown 的知识库，支持分类管理、标签索引，让你的知识有序沉淀</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="16 18 22 12 16 6" />
              <polyline points="8 6 2 12 8 18" />
            </svg>
          </div>
          <h3 class="feature-title">代码沙箱</h3>
          <p class="feature-description">本地部署支持 Docker 沙箱，可在浏览器中直接运行 Python 代码，支持 GPU 加速</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
          </div>
          <h3 class="feature-title">评论互动</h3>
          <p class="feature-description">基于 GitHub Issues 的评论系统，支持 OAuth 登录，让讨论更加便捷</p>
        </div>
      </div>
    </section>

    <!-- 部署模式 -->
    <section class="deployment">
      <h2 class="section-title">双模式部署</h2>
      <div class="deployment-grid">
        <div class="deployment-card">
          <div class="card-header">
            <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"/>
              <line x1="2" y1="12" x2="22" y2="12"/>
              <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
            </svg>
            <h3>互联网模式</h3>
          </div>
          <ul class="card-list">
            <li>GitHub Pages 静态部署</li>
            <li>无需后端服务</li>
            <li>GitHub Issues 评论系统</li>
            <li>Mermaid 流程图支持</li>
          </ul>
        </div>
        <div class="deployment-card">
          <div class="card-header">
            <svg class="card-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
              <line x1="8" y1="21" x2="16" y2="21"/>
              <line x1="12" y1="17" x2="12" y2="21"/>
            </svg>
            <h3>本地模式</h3>
          </div>
          <ul class="card-list">
            <li>本地 Node.js 服务</li>
            <li>Docker 代码沙箱</li>
            <li>GPU 加速支持</li>
            <li>文件系统操作</li>
          </ul>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { usePageFrontmatter } from '@vuepress/client'

const frontmatter = usePageFrontmatter()

// Hero 配置
const heroTitle = computed(() => {
  return frontmatter.value.heroText || '交互式知识管理平台'
})

const heroDescription = computed(() => {
  return frontmatter.value.tagline || '整理知识、分享见解、交互学习'
})
</script>

<style lang="scss" scoped>
.home {
  max-width: 1440px;
  margin: 0 auto;
}

.hero {
  padding: 80px 48px;
  text-align: center;
}

.hero-title {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 48px;
  font-weight: 600;
  color: var(--c-text);
  margin: 0 0 16px;
  letter-spacing: -1px;
}

.hero-description {
  font-family: 'Inter', sans-serif;
  font-size: 20px;
  font-weight: 400;
  color: var(--c-text-light);
  margin: 0 0 32px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
}

.btn {
  display: inline-flex;
  align-items: center;
  padding: 12px 24px;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.2s;

  &.btn-primary {
    background: var(--c-brand);
    color: #fff;

    &:hover {
      filter: brightness(1.1);
    }
  }

  &.btn-secondary {
    border: 1.5px solid var(--c-border);
    color: var(--c-text);

    &:hover {
      background: var(--c-bg-light);
    }
  }
}

.features {
  padding: 64px 48px;
  background: var(--c-bg-light);
}

.features-title {
  font-family: 'Inter', sans-serif;
  font-size: 28px;
  font-weight: 600;
  color: var(--c-text);
  text-align: center;
  margin: 0 0 48px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: var(--c-bg);
  border: 1.5px solid var(--c-border);
  border-radius: 16px;
  padding: 24px;
}

.feature-icon {
  width: 48px;
  height: 48px;
  background: var(--c-brand-light);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;

  svg {
    width: 24px;
    height: 24px;
    stroke: var(--c-brand);
  }
}

.feature-title {
  font-family: 'Inter', sans-serif;
  font-size: 18px;
  font-weight: 600;
  color: var(--c-text);
  margin: 0 0 8px;
}

.feature-description {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 400;
  color: var(--c-text-light);
  line-height: 1.6;
  margin: 0;
}

.deployment {
  padding: 64px 48px;
}

.section-title {
  font-family: 'Inter', sans-serif;
  font-size: 28px;
  font-weight: 600;
  color: var(--c-text);
  text-align: center;
  margin: 0 0 48px;
}

.deployment-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  max-width: 800px;
  margin: 0 auto;
}

.deployment-card {
  background: var(--c-bg);
  border: 1.5px solid var(--c-border);
  border-radius: 16px;
  padding: 32px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;

  h3 {
    font-family: 'Inter', sans-serif;
    font-size: 18px;
    font-weight: 600;
    color: var(--c-text);
    margin: 0;
  }
}

.card-icon {
  width: 32px;
  height: 32px;
  stroke: var(--c-brand);
}

.card-list {
  list-style: none;
  padding: 0;
  margin: 0;

  li {
    font-family: 'Inter', sans-serif;
    font-size: 14px;
    color: var(--c-text-light);
    padding: 8px 0;
    border-bottom: 1px solid var(--c-border);

    &:last-child {
      border-bottom: none;
    }

    &::before {
      content: '•';
      color: var(--c-brand);
      margin-right: 8px;
    }
  }
}

@media (max-width: 768px) {
  .features-grid {
    grid-template-columns: 1fr;
  }

  .deployment-grid {
    grid-template-columns: 1fr;
  }

  .hero-title {
    font-size: 32px;
  }
}
</style>