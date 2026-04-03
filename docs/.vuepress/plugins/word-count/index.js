/**
 * 字数统计插件
 * 参考 awesome-fenix 的 read-time 插件实现
 * 在构建时计算 Markdown 文章的字数，支持中英文混合统计
 */

// 全局字数统计对象（构建时收集所有页面的字数）
const globalWords = {}

/**
 * 预处理 Markdown 内容，移除语法标记但保留代码和公式内容
 *
 * 字数统计规则（详见 openspec/specs/word-count-plugin/spec.md）：
 * - 代码块 ```...``` 和行内代码 `...`：计入字数（移除语法标记，保留内容）
 * - 行内公式 $...$ 和块级公式 $$...$$：计入字数（移除语法标记，保留内容）
 * - 链接、图片、HTML标签、frontmatter：不计入字数
 */
function preprocessMarkdown(content) {
  if (!content) return ''

  let text = content

  // 代码块：移除 ``` 和语言标记（可能包含空格），保留代码内容
  text = text.replace(/```[^\n]*\n([\s\S]*?)```/g, '$1')

  // 行内代码：移除 ` 符号，保留内容
  text = text.replace(/`([^`]+)`/g, '$1')

  // 块级公式：移除 $$ 符号，保留公式内容
  text = text.replace(/\$\$([\s\S]*?)\$\$/g, '$1')

  // 行内公式：移除 $ 符号，保留公式内容
  text = text.replace(/\$([^\$\n]+?)\$/g, '$1')

  // 以下内容不计入字数
  text = text.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')  // 链接：保留显示文字
  text = text.replace(/!\[[^\]]*\]\([^)]+\)/g, '')     // 图片：完全移除
  text = text.replace(/<[a-zA-Z\/][^>]*>/g, '')        // HTML标签：只匹配真正的标签（字母开头）
  text = text.replace(/^---[\s\S]*?---/m, '')          // Frontmatter：完全移除

  // Markdown 格式标记（保留文字内容）
  text = text.replace(/^#{1,6}\s+/gm, '')               // 标题标记
  text = text.replace(/\*\*?([^*]+)\*\*?/g, '$1')       // 粗体/斜体
  text = text.replace(/__?([^_]+)__?/g, '$1')           // 粗体/斜体

  return text
}

/**
 * 计算字数（支持中英文混合）
 * 基于 awesome-fenix 的 fnGetCpmisWords 算法
 */
function countWords(str) {
  if (!str) return 0

  let sLen = 0
  try {
    str = str.replace(/(\r\n+|\s+|　+)/g, '龘')
    str = str.replace(/[\x00-\xff]/g, 'm')
    str = str.replace(/m+/g, '*')
    str = str.replace(/龘+/g, '')
    sLen = str.length
  } catch (e) {
    console.error('字数统计出错:', e)
  }

  return sLen
}

/**
 * VuePress 2 插件：字数统计
 */
const wordCountPlugin = (options = {}) => {
  return {
    name: 'vuepress-plugin-word-count',

    // VuePress 2: 使用 onInitialized 钩子收集所有页面字数并写入临时文件
    async onInitialized(app) {
      // 第一遍：收集所有页面的字数
      for (const page of app.pages) {
        let wordCount = 0

        // 如果 frontmatter 中已有 wordCount，使用预设值
        if (page.frontmatter?.wordCount) {
          wordCount = page.frontmatter.wordCount
        } else {
          const content = page.content || ''
          if (content) {
            const plainText = preprocessMarkdown(content)
            wordCount = countWords(plainText)
          }
        }

        globalWords[page.path] = wordCount
        page.data.wordCount = wordCount
      }

      // 第二遍：将 globalWords 注入到每个页面（用于页面级别显示）
      for (const page of app.pages) {
        page.data.readingTime = {
          words: page.data.wordCount,
          minutes: page.data.wordCount / 500,
          globalWords: { ...globalWords }  // 复制一份，确保每个页面都有完整数据
        }
      }

      // 构建 wordCountData 结构 {path: {title, wordCount}}
      const wordCountData = {}
      for (const page of app.pages) {
        wordCountData[page.path] = {
          title: page.title,
          wordCount: page.data.wordCount || 0
        }
      }

      // 在 onInitialized 中写入临时文件（异步操作必须在此完成）
      await app.writeTemp(
        'word-count/data.js',
        `export const wordCountData = ${JSON.stringify(wordCountData)}`
      )

      await app.writeTemp(
        'word-count/client.js',
        `import { defineClientConfig } from 'vuepress/client'
import { wordCountData } from './data.js'

export default defineClientConfig({
  enhance({ app }) {
    app.provide('wordCountData', wordCountData)
  }
})`
      )
    },

    // clientConfigFile 只返回文件路径（文件已在 onInitialized 中写入）
    clientConfigFile(app) {
      return app.dir.temp('word-count/client.js')
    }
  }
}

export default wordCountPlugin