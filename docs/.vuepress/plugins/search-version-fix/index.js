import { path, fs } from 'vuepress/utils'
import { getDirname } from 'vuepress/utils'

const __dirname = getDirname(import.meta.url)

/**
 * 修复 vuepress-plugin-search-pro 的版本字段兼容性问题
 *
 * 问题：vuepress-plugin-search-pro 打包的 worker 期望 `serializationVersion` 字段，
 * 但 SlimSearch 2.2.x/2.3.x 使用 `version` 字段。
 *
 * 解决方案：在生成的 worker 文件中，修改反序列化函数，使其同时支持两个字段名。
 */
export const searchVersionFixPlugin = {
  name: 'search-version-fix',

  onGenerated: async (app) => {
    const workerPath = path.resolve(app.dir.dest(), 'search-pro.worker.js')

    if (await fs.pathExists(workerPath)) {
      let content = await fs.readFile(workerPath, 'utf-8')

      // 修复版本字段检查逻辑
      // 原始: serializationVersion:c},a)=>{if(c!==1&&c!==2)
      // 修改后: serializationVersion:c,version:v},a)=>{const ver=c??v;if(ver!==1&&ver!==2)

      // 方法1：修改反序列化函数的参数解构，添加对 version 字段的支持
      const originalPattern = /serializationVersion:c\},a\)=>\{if\(c!==1&&c!==2\)/
      const replacement = 'serializationVersion:c,version:v},a)=>{const ver=c??v;if(ver!==1&&ver!==2)'

      if (originalPattern.test(content)) {
        content = content.replace(originalPattern, replacement)
        await fs.writeFile(workerPath, content)
        app.env.isDebug && console.log('[search-version-fix] 已修复 worker 版本字段兼容性')
      }
    }
  }
}