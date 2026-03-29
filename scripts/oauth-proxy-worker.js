/**
 * GitHub OAuth 代理 - 腾讯云云函数
 *
 * 部署步骤：
 * 1. 登录腾讯云控制台，进入云函数 SCF
 * 2. 创建新函数，选择 Node.js 运行环境
 * 3. 上传此代码文件
 * 4. 配置触发器（API 网关），获得访问 URL
 */

const express = require('express')
const app = express()

// 中间件
app.use(express.json())

// CORS 头
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*')
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
  res.header('Access-Control-Allow-Headers', 'Content-Type')
  if (req.method === 'OPTIONS') {
    return res.sendStatus(200)
  }
  next()
})

// OAuth 配置
const OAUTH_CONFIG = {
  clientId: 'Ov23liQbtfoZGMcsU9VV',
  clientSecret: 'f93311c59cbe51af671a3aa95af64028d4d7d1d3'
}

// 健康检查
app.get('/', (req, res) => {
  res.json({ status: 'ok', service: 'github-oauth-proxy' })
})

// OAuth token 交换
app.get('/callback', async (req, res) => {
  const { code } = req.query

  if (!code) {
    return res.status(400).json({ error: 'Missing code parameter' })
  }

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

// POST 方式也支持（某些客户端使用 POST）
app.post('/callback', async (req, res) => {
  const { code } = req.body

  if (!code) {
    return res.status(400).json({ error: 'Missing code parameter' })
  }

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
  })
}

// 导出供云函数使用
module.exports = app