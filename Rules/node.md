# Node.js 高效开发指南

## 🎯 推荐技术栈
- **核心**: Node.js + Express + TypeScript
- **数据库**: MongoDB (小项目可用 SQLite)
- **认证**: JWT + bcrypt
- **测试**: Jest

## 📁 简洁项目结构
```
src/
├── routes/          # 路由定义
├── controllers/     # 业务逻辑
├── models/         # 数据模型
├── middleware/     # 中间件
├── utils/          # 工具函数
├── config/         # 配置文件
└── types/          # TypeScript类型
```

## 🔧 核心开发原则

### 1. 环境配置 (简化版)
```javascript
// config/index.js
const config = {
  env: process.env.NODE_ENV || 'development',
  port: process.env.PORT || 3000,
  
  database: {
    url: process.env.MONGODB_URL || 'mongodb://localhost:27017/myapp'
  },
  
  jwt: {
    secret: process.env.JWT_SECRET || 'dev-secret',
    expiresIn: '7d'
  }
}

module.exports = config
```

```bash
# .env.development
NODE_ENV=development
PORT=3000
MONGODB_URL=mongodb://localhost:27017/myapp_dev
JWT_SECRET=dev_secret

# .env.production
NODE_ENV=production
PORT=8080
MONGODB_URL=mongodb://your-server/myapp_prod
JWT_SECRET=your_production_secret
```

### 2. 控制器模式 (简洁版)
```javascript
// controllers/userController.js

/**
 * 用户控制器
 */
const userController = {
  // 获取用户信息
  async getUser(req, res) {
    try {
      const { id } = req.params
      const user = await User.findById(id)
      
      if (!user) {
        return res.status(404).json({ 
          success: false, 
          message: '用户不存在' 
        })
      }
      
      res.json({ 
        success: true, 
        data: user 
      })
    } catch (error) {
      res.status(500).json({ 
        success: false, 
        message: error.message 
      })
    }
  },

  // 创建用户
  async createUser(req, res) {
    try {
      const user = new User(req.body)
      await user.save()
      
      res.status(201).json({ 
        success: true, 
        data: user 
      })
    } catch (error) {
      res.status(400).json({ 
        success: false, 
        message: error.message 
      })
    }
  }
}

module.exports = userController
```

### 3. 认证中间件
```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken')
const config = require('../config')

const authMiddleware = (req, res, next) => {
  const token = req.header('Authorization')?.replace('Bearer ', '')
  
  if (!token) {
    return res.status(401).json({ 
      success: false, 
      message: '访问令牌缺失' 
    })
  }
  
  try {
    const decoded = jwt.verify(token, config.jwt.secret)
    req.user = decoded
    next()
  } catch (error) {
    res.status(401).json({ 
      success: false, 
      message: '令牌无效' 
    })
  }
}

module.exports = authMiddleware
```

### 4. 数据模型设计
```javascript
// models/User.js
const mongoose = require('mongoose')
const bcrypt = require('bcrypt')

const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true,
    trim: true
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true
  },
  password: {
    type: String,
    required: true,
    minlength: 6
  }
}, {
  timestamps: true
})

// 密码加密
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next()
  this.password = await bcrypt.hash(this.password, 10)
  next()
})

// 密码验证
userSchema.methods.comparePassword = function(password) {
  return bcrypt.compare(password, this.password)
}

module.exports = mongoose.model('User', userSchema)
```

## 🛡️ 基础安全设置
```javascript
// app.js
const express = require('express')
const cors = require('cors')
const helmet = require('helmet')

const app = express()

// 基础安全和跨域
app.use(helmet())
app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(',') || 'http://localhost:8080'
}))

// 请求解析
app.use(express.json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true }))

// 统一错误处理
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).json({
    success: false,
    message: '服务器内部错误'
  })
})
```

## 🚀 性能要点
- 使用连接池管理数据库连接
- 频繁查询的数据考虑缓存
- 大文件上传使用流处理
- 生产环境使用 PM2 或类似工具

## ✅ 开发检查清单 (3项核心)
开发完成后检查：
- [ ] **错误处理**: 是否添加了 try-catch 和适当的错误响应
- [ ] **数据验证**: 是否验证了请求参数和数据格式
- [ ] **安全考虑**: 敏感操作是否需要认证，密码是否加密

## 📚 常用代码片段

### API 响应格式
```javascript
// utils/response.js
const sendSuccess = (res, data, message = '成功') => {
  res.json({
    success: true,
    data,
    message
  })
}

const sendError = (res, message = '错误', statusCode = 400) => {
  res.status(statusCode).json({
    success: false,
    message
  })
}

module.exports = { sendSuccess, sendError }
```

### 参数验证
```javascript
// middleware/validate.js
const validate = (schema) => {
  return (req, res, next) => {
    const { error } = schema.validate(req.body)
    if (error) {
      return res.status(400).json({
        success: false,
        message: error.details[0].message
      })
    }
    next()
  }
}

module.exports = validate
```

### 路由定义
```javascript
// routes/users.js
const express = require('express')
const userController = require('../controllers/userController')
const authMiddleware = require('../middleware/auth')

const router = express.Router()

router.get('/:id', userController.getUser)
router.post('/', userController.createUser)
router.put('/:id', authMiddleware, userController.updateUser)

module.exports = router
```

## 📊 日志建议
```javascript
// 简单的日志处理
const log = (level, message, data = null) => {
  const timestamp = new Date().toISOString()
  console.log(`[${timestamp}] ${level.toUpperCase()}: ${message}`, data || '')
}

module.exports = { log }
```

---
**记住**: 先让功能跑起来，再考虑优化。简单直接的代码比过度设计的代码更容易维护。 