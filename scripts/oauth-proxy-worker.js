/**
 * GitHub OAuth 代理 - 腾讯云云函数
 *
 * 支持 CORS 跨域请求
 * 所有请求都在根路径处理，避免 API 网关路径匹配问题
 */

const express = require('express')
const app = express()

// 中间件
app.use(express.json())

// CORS 配置 - 允许多个域名
const ALLOWED_ORIGINS = [
  'https://ai.icyfenix.cn',
  'https://fenixsoft.github.io',
  'http://localhost:8080',
  'http://localhost:8081',
  'http://localhost:3001'
]

app.use((req, res, next) => {
  const origin = req.headers.origin

  // 检查是否在允许列表中
  if (origin && ALLOWED_ORIGINS.includes(origin)) {
    res.header('Access-Control-Allow-Origin', origin)
  } else {
    // 允许所有域名（开发环境）
    res.header('Access-Control-Allow-Origin', '*')
  }

  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  res.header('Access-Control-Max-Age', '86400') // 预检请求缓存 24 小时

  // 预检请求直接返回
  if (req.method === 'OPTIONS') {
    return res.sendStatus(204)
  }
  next()
})

// OAuth 配置
const OAUTH_CONFIG = {
  clientId: 'Ov23liQbtfoZGMcsU9VV',
  clientSecret: 'f93311c59cbe51af671a3aa95af64028d4d7d1d3'
}

// 根路径处理所有请求
app.all('/', async (req, res) => {
  const code = req.query.code || req.body?.code

  // 无 code 时返回健康检查
  if (!code) {
    return res.json({ status: 'ok', service: 'github-oauth-proxy' })
  }

  // 有 code 时进行 OAuth token 交换
  try {
    const response = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        client_id: OAUTH_CONFIG.clientId,
        client_secret: OAUTH_CONFIG.clientSecret,
        code: code
      })
    })

    const data = await response.json()
    res.json(data)
  } catch (error) {
    console.error('OAuth proxy error:', error)
    res.status(500).json({ error: error.message })
  }
})

// 本地开发
if (require.main === module) {
  const port = process.env.PORT || 9000
  app.listen(port, () => {
    console.log(`OAuth proxy running at http://localhost:${port}`)
    console.log(`Allowed origins: ${ALLOWED_ORIGINS.join(', ')}`)
  })
}

// 导出供云函数使用
module.exports = app