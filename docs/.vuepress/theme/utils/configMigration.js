/**
 * 配置迁移脚本
 * 将旧的 sandbox-config 数据迁移到新的 site-config
 */

const OLD_CONFIG_KEY = 'sandbox-config'
const NEW_CONFIG_KEY = 'site-config'

/**
 * 迁移旧的沙箱配置到新的站点配置
 * 如果存在旧的 sandbox-config，读取并合并到 site-config
 * 迁移完成后删除旧的 key
 */
export function migrateConfig() {
  if (typeof window === 'undefined') return

  try {
    const oldConfig = localStorage.getItem(OLD_CONFIG_KEY)
    const newConfig = localStorage.getItem(NEW_CONFIG_KEY)

    // 如果旧配置存在且新配置不存在，执行迁移
    if (oldConfig && !newConfig) {
      const parsedOldConfig = JSON.parse(oldConfig)
      const migratedConfig = {
        sandboxEndpoint: parsedOldConfig.endpoint || 'http://localhost:3001',
        highlightTheme: 'default' // 默认使用当前样式
      }

      localStorage.setItem(NEW_CONFIG_KEY, JSON.stringify(migratedConfig))
      localStorage.removeItem(OLD_CONFIG_KEY)

      console.log('[Config Migration] 成功迁移配置:', migratedConfig)
      return migratedConfig
    }

    // 如果旧配置存在且新配置也存在，只删除旧配置
    if (oldConfig && newConfig) {
      localStorage.removeItem(OLD_CONFIG_KEY)
      console.log('[Config Migration] 删除旧配置，保留现有配置')
    }
  } catch (error) {
    console.error('[Config Migration] 迁移失败:', error)
  }
}

/**
 * 获取站点配置
 * 如果配置不存在，返回默认配置
 */
export function getSiteConfig() {
  if (typeof window === 'undefined') {
    return {
      sandboxEndpoint: 'http://localhost:3001',
      highlightTheme: 'default'
    }
  }

  migrateConfig() // 确保每次获取时检查迁移

  try {
    const config = localStorage.getItem(NEW_CONFIG_KEY)
    if (config) {
      return JSON.parse(config)
    }
  } catch (error) {
    console.error('[Config] 读取配置失败:', error)
  }

  // 返回默认配置
  return {
    sandboxEndpoint: 'http://localhost:3001',
    highlightTheme: 'default'
  }
}

/**
 * 保存站点配置
 */
export function saveSiteConfig(config) {
  if (typeof window === 'undefined') return

  try {
    localStorage.setItem(NEW_CONFIG_KEY, JSON.stringify(config))
    console.log('[Config] 配置已保存:', config)
  } catch (error) {
    console.error('[Config] 保存配置失败:', error)
  }
}