/**
 * 代码高亮主题配置
 * 定义 PrismJS 高亮主题列表，用于设置页面下拉选择
 */

export const HIGHLIGHT_THEMES = [
  {
    id: 'default',
    name: '当前样式',
    cssPath: null // 不加载 PrismJS 主题，保持自定义样式
  },
  {
    id: 'prism',
    name: 'Default',
    cssPath: 'prismjs/themes/prism.min.css'
  },
  {
    id: 'prism-coy',
    name: 'Coy',
    cssPath: 'prismjs/themes/prism-coy.min.css'
  },
  {
    id: 'prism-dark',
    name: 'Dark',
    cssPath: 'prismjs/themes/prism-dark.min.css'
  },
  {
    id: 'prism-funky',
    name: 'Funky',
    cssPath: 'prismjs/themes/prism-funky.min.css'
  },
  {
    id: 'prism-okaidia',
    name: 'Okaidia',
    cssPath: 'prismjs/themes/prism-okaidia.min.css'
  },
  {
    id: 'prism-solarizedlight',
    name: 'Solarized Light',
    cssPath: 'prismjs/themes/prism-solarizedlight.min.css'
  },
  {
    id: 'prism-tomorrow',
    name: 'Tomorrow Night',
    cssPath: 'prismjs/themes/prism-tomorrow.min.css'
  },
  {
    id: 'prism-twilight',
    name: 'Twilight',
    cssPath: 'prismjs/themes/prism-twilight.min.css'
  }
]

// 样例代码片段，用于实时预览高亮效果
export const SAMPLE_CODE = `# 这是一个示例代码片段
def hello_world(name: str) -> str:
    """返回问候语"""
    message = f"Hello, {name}!"
    print(message)
    return message

class User:
    def __init__(self, name: str):
        self.name = name

# 调用函数
result = hello_world("World")`

// 默认主题
export const DEFAULT_THEME = 'default'

// 获取主题配置
export function getThemeConfig(themeId) {
  return HIGHLIGHT_THEMES.find(theme => theme.id === themeId) || HIGHLIGHT_THEMES[0]
}