/**
 * Design Machine Learning Applications 本地服务
 * 提供 Python 代码沙箱执行 API
 */
import express from 'express'
import cors from 'cors'
import { fileURLToPath } from 'url'
import { resolve } from 'path'
import sandboxRouter from './routes/sandbox.js'

export const app = express()
const PORT = process.env.PORT || 3001

// 中间件
app.use(cors())
app.use(express.json())

// 健康检查
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() })
})

// 沙箱 API
app.use('/api/sandbox', sandboxRouter)

// 错误处理
app.use((err, req, res, next) => {
  console.error('Error:', err)
  res.status(500).json({
    success: false,
    error: err.message || 'Internal Server Error'
  })
})

// 仅在直接运行时启动服务器（被 import 时不启动）
// 使用路径比较，兼容 Windows 和 Unix 系统
const __filename = fileURLToPath(import.meta.url)
const entryPoint = resolve(process.argv[1] || '')

if (__filename === entryPoint) {
  app.listen(PORT, () => {
    console.log(`🚀 DMLA 本地服务已启动`)
    console.log(`   API: http://localhost:${PORT}`)
    console.log(`   健康检查: http://localhost:${PORT}/api/health`)
  })
}

export default app