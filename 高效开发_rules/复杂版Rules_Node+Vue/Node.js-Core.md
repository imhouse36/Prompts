---
description: Node.js and Express.js best practices for backend development
globs: **/*.js, **/*.ts, src/**/*.ts
---

# Node.js 核心开发规范

## 🎯 核心技术栈
- **后端**：Node.js + Express.js + TypeScript
- **数据库**：MongoDB + Mongoose ODM
- **认证**：JWT + bcrypt
- **环境**：双环境自动检测和切换
- **测试**：Jest + Supertest

## 🌍 环境配置要求
### 自动环境检测原则
- **智能环境识别**：根据NODE_ENV、端口、域名自动判断环境
- **配置自动加载**：开发/生产环境配置文件自动切换
- **数据库自动切换**：开发/生产数据库连接自动选择
- **CORS自适应**：跨域配置根据环境自动调整
- **安全策略**：生产环境安全机制自动启用

### 核心环境配置
```javascript
// config/environment.js - 环境自动检测
class EnvironmentManager {
  detectEnvironment() {
    // 1. 检查NODE_ENV
    if (process.env.NODE_ENV === 'production') return 'production'
    
    // 2. 检查端口（生产环境通常使用80/443/8080等）
    const port = process.env.PORT || 3000
    if (port === 80 || port === 443 || port >= 8000) return 'production'
    
    // 3. 检查主机名
    const hostname = require('os').hostname()
    if (hostname.includes('localhost') || hostname.includes('127.0.0.1')) {
      return 'development'
    }
    
    return 'development'
  }
  
  getConfig() {
    const env = this.detectEnvironment()
    
    return {
      environment: env,
      port: process.env.PORT || (env === 'production' ? 8080 : 3000),
      
      // 数据库自动切换
      database: {
        uri: env === 'production' 
          ? process.env.MONGODB_URI_PROD 
          : process.env.MONGODB_URI_DEV || 'mongodb://localhost:27017/app_dev'
      },
      
      // JWT配置
      jwt: {
        secret: process.env.JWT_SECRET || this.getDefaultSecret(env),
        expiresIn: '7d'
      },
      
      // CORS自动配置
      cors: {
        origins: env === 'production' 
          ? process.env.ALLOWED_ORIGINS?.split(',') || []
          : ['http://localhost:8080', 'http://localhost:3000']
      }
    }
  }
}

module.exports = new EnvironmentManager().getConfig()
```

### 环境变量文件
```bash
# .env.development
NODE_ENV=development
PORT=3000
MONGODB_URI_DEV=mongodb://localhost:27017/app_dev
JWT_SECRET=dev_secret_key
ALLOWED_ORIGINS=http://localhost:8080,http://localhost:3000

# .env.production
NODE_ENV=production
PORT=8080
MONGODB_URI_PROD=mongodb://your-prod-server/app_prod
JWT_SECRET=your_production_secret_key
ALLOWED_ORIGINS=https://yourdomain.com
```

## 📁 项目结构（简化）
```
Node/
├── src/
│   ├── config/           # 配置管理
│   │   ├── environment.js    # 环境检测
│   │   ├── database.js       # 数据库配置
│   │   └── cors.js           # CORS配置
│   ├── controllers/      # 控制器层
│   ├── routes/          # 路由定义
│   ├── middlewares/     # 中间件
│   │   ├── auth.js          # JWT认证
│   │   ├── errorHandler.js  # 错误处理
│   │   └── validation.js    # 参数验证
│   ├── models/          # 数据模型
│   ├── services/        # 业务逻辑层
│   └── utils/           # 工具函数
├── tests/               # 测试文件
├── .env.development     # 开发环境变量
├── .env.production      # 生产环境变量
└── server.js           # 服务入口
```

## 🔧 核心编码规范
### 控制器设计
```javascript
/**
 * 用户控制器
 * @description 处理用户相关的HTTP请求
 */
class UserController {
  /**
   * 获取用户信息
   * @param {Object} req - Express请求对象
   * @param {Object} res - Express响应对象
   */
  async getUser(req, res) {
    try {
      const { userId } = req.params
      
      // 参数验证
      if (!userId) {
        return res.status(400).json({
          success: false,
          message: 'User ID is required'
        })
      }
      
      // 业务逻辑
      const user = await userService.findById(userId)
      
      if (!user) {
        return res.status(404).json({
          success: false,
          message: 'User not found'
        })
      }
      
      // 成功响应
      res.status(200).json({
        success: true,
        data: user
      })
      
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      })
    }
  }
}

module.exports = new UserController()
```

### 中间件模式
```javascript
// middlewares/auth.js - JWT认证中间件
const jwt = require('jsonwebtoken')
const config = require('../config/environment')

/**
 * JWT认证中间件
 * @param {Object} req - 请求对象
 * @param {Object} res - 响应对象
 * @param {Function} next - 下一个中间件
 */
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization']
  const token = authHeader && authHeader.split(' ')[1]
  
  if (!token) {
    return res.status(401).json({
      success: false,
      message: 'Access token required'
    })
  }
  
  jwt.verify(token, config.jwt.secret, (err, user) => {
    if (err) {
      return res.status(403).json({
        success: false,
        message: 'Invalid or expired token'
      })
    }
    
    req.user = user
    next()
  })
}

module.exports = { authenticateToken }
```

### 数据模型设计
```javascript
// models/User.js - Mongoose用户模型
const mongoose = require('mongoose')
const bcrypt = require('bcrypt')

/**
 * 用户数据模型
 * @description 定义用户的数据结构和方法
 */
const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: [true, 'Username is required'],
    unique: true,
    trim: true,
    minlength: [3, 'Username must be at least 3 characters'],
    maxlength: [20, 'Username cannot exceed 20 characters']
  },
  
  email: {
    type: String,
    required: [true, 'Email is required'],
    unique: true,
    lowercase: true,
    match: [/^\S+@\S+\.\S+$/, 'Please enter a valid email']
  },
  
  password: {
    type: String,
    required: [true, 'Password is required'],
    minlength: [6, 'Password must be at least 6 characters']
  }
}, {
  timestamps: true,  // 自动添加createdAt和updatedAt
  toJSON: { transform: (doc, ret) => { delete ret.password; return ret; } }
})

// 密码加密中间件
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next()
  
  try {
    const salt = await bcrypt.genSalt(10)
    this.password = await bcrypt.hash(this.password, salt)
    next()
  } catch (error) {
    next(error)
  }
})

// 密码验证方法
userSchema.methods.comparePassword = async function(candidatePassword) {
  return bcrypt.compare(candidatePassword, this.password)
}

module.exports = mongoose.model('User', userSchema)
```

### 错误处理
```javascript
// middlewares/errorHandler.js - 统一错误处理
const config = require('../config/environment')

/**
 * 全局错误处理中间件
 * @param {Error} err - 错误对象
 * @param {Object} req - 请求对象
 * @param {Object} res - 响应对象
 * @param {Function} next - 下一个中间件
 */
const errorHandler = (err, req, res, next) => {
  let error = { ...err }
  error.message = err.message
  
  // 开发环境显示详细错误信息
  if (config.environment === 'development') {
    console.error('Error details:', err)
  }
  
  // Mongoose验证错误
  if (err.name === 'ValidationError') {
    const message = Object.values(err.errors).map(val => val.message).join(', ')
    error = { message, statusCode: 400 }
  }
  
  // JWT错误
  if (err.name === 'JsonWebTokenError') {
    error = { message: 'Invalid token', statusCode: 401 }
  }
  
  // 默认服务器错误
  res.status(error.statusCode || 500).json({
    success: false,
    message: error.message || 'Server Error',
    ...(config.environment === 'development' && { stack: err.stack })
  })
}

module.exports = errorHandler
```

## 🛡️ 安全规范
### 基础安全配置
```javascript
// app.js - Express应用安全配置
const express = require('express')
const helmet = require('helmet')
const cors = require('cors')
const rateLimit = require('express-rate-limit')
const config = require('./config/environment')

const app = express()

// 安全头部
app.use(helmet())

// CORS配置
app.use(cors({
  origin: config.cors.origins,
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}))

// 请求频率限制
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15分钟
  max: config.environment === 'production' ? 100 : 1000,
  message: {
    success: false,
    message: 'Too many requests, please try again later'
  }
})
app.use('/api/', limiter)

// JSON解析限制
app.use(express.json({ limit: '10mb' }))
app.use(express.urlencoded({ extended: true, limit: '10mb' }))
```

### API响应标准
```javascript
// 统一API响应格式
const sendResponse = (res, statusCode, success, data = null, message = '') => {
  res.status(statusCode).json({
    success,
    data,
    message,
    timestamp: new Date().toISOString()
  })
}

// 成功响应
const sendSuccess = (res, data, message = 'Success') => {
  sendResponse(res, 200, true, data, message)
}

// 错误响应
const sendError = (res, statusCode = 500, message = 'Internal Server Error') => {
  sendResponse(res, statusCode, false, null, message)
}

module.exports = { sendSuccess, sendError }
```

## 📊 性能要求
- **数据库连接池**：生产环境最大20个连接，开发环境10个
- **请求限制**：API请求体限制10MB，文件上传另行配置
- **缓存策略**：频繁查询数据使用Redis缓存
- **日志管理**：生产环境仅记录error级别，开发环境记录debug

## ✅ 代码检查要点
开发时必须检查：
- [ ] 是否添加函数级注释
- [ ] 是否进行参数验证
- [ ] 是否使用统一的错误处理
- [ ] API是否返回标准格式
- [ ] 敏感信息是否正确处理
- [ ] 数据库查询是否进行错误处理
- [ ] 中间件是否按正确顺序添加
- [ ] 环境变量是否正确配置

## 📚 详细文档引用
- 环境配置详细说明：`docs/node/environment-advanced.md`
- 安全配置指南：`docs/node/security-guide.md`
- 数据库最佳实践：`docs/node/database-guide.md`
- 部署配置指南：`docs/node/deployment-guide.md`
