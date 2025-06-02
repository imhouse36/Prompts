# Node.js 环境配置详细指南

## 🌍 完整后端环境配置

### 高级环境管理器
```javascript
// config/environment.js - 完整环境管理
const dotenv = require('dotenv')
const path = require('path')
const os = require('os')

class AdvancedEnvironmentManager {
  constructor() {
    this.environment = this.detectEnvironment()
    this.loadEnvironmentConfig()
    this.validateRequiredVars()
  }

  /**
   * 智能环境检测
   * 支持多种检测方式确保准确性
   */
  detectEnvironment() {
    // 1. 优先检查 NODE_ENV
    if (process.env.NODE_ENV) {
      return process.env.NODE_ENV
    }

    // 2. 检查启动参数
    const args = process.argv
    if (args.includes('--production') || args.includes('--prod')) {
      return 'production'
    }
    if (args.includes('--staging') || args.includes('--stage')) {
      return 'staging'
    }
    if (args.includes('--development') || args.includes('--dev')) {
      return 'development'
    }

    // 3. 检查端口号
    const port = process.env.PORT || 3000
    if (port === 80 || port === 443) {
      return 'production'
    }
    if (port >= 8000 && port < 9000) {
      return 'staging'
    }

    // 4. 检查主机名
    const hostname = os.hostname()
    if (hostname.includes('prod') || hostname.includes('live')) {
      return 'production'
    }
    if (hostname.includes('staging') || hostname.includes('test')) {
      return 'staging'
    }

    // 5. 检查环境变量指示器
    if (process.env.KUBERNETES_SERVICE_HOST) {
      return 'production' // Kubernetes 环境
    }
    if (process.env.DOCKER_CONTAINER) {
      return 'staging' // Docker 容器
    }

    // 6. 默认开发环境
    return 'development'
  }

  /**
   * 加载对应环境的配置文件
   */
  loadEnvironmentConfig() {
    const envFile = `.env.${this.environment}`
    const envPath = path.resolve(process.cwd(), envFile)
    
    // 先加载基础配置
    dotenv.config({ path: '.env' })
    
    // 再加载环境特定配置（会覆盖基础配置）
    dotenv.config({ path: envPath })
    
    // 设置 NODE_ENV
    process.env.NODE_ENV = this.environment
    
    console.log(`🌍 Environment: ${this.environment}`)
    console.log(`📋 Config file: ${envFile}`)
  }

  /**
   * 验证必需的环境变量
   */
  validateRequiredVars() {
    const required = this.getRequiredVars()
    const missing = []

    required.forEach(varName => {
      if (!process.env[varName]) {
        missing.push(varName)
      }
    })

    if (missing.length > 0) {
      console.error('❌ Missing required environment variables:')
      missing.forEach(varName => {
        console.error(`   - ${varName}`)
      })
      
      if (this.environment === 'production') {
        process.exit(1) // 生产环境必须有完整配置
      } else {
        console.warn('⚠️ Some variables are missing, using defaults for development')
      }
    }
  }

  /**
   * 获取各环境必需的变量
   */
  getRequiredVars() {
    const baseRequired = ['PORT', 'JWT_SECRET']
    
    const envSpecific = {
      development: [],
      staging: ['MONGODB_URI_STAGING', 'REDIS_URL'],
      production: [
        'MONGODB_URI_PROD',
        'REDIS_URL', 
        'SMTP_HOST',
        'SMTP_USER',
        'SMTP_PASS',
        'ALLOWED_ORIGINS'
      ]
    }

    return [...baseRequired, ...(envSpecific[this.environment] || [])]
  }

  /**
   * 获取完整配置对象
   */
  getConfig() {
    return {
      // 基础配置
      environment: this.environment,
      port: parseInt(process.env.PORT, 10) || this.getDefaultPort(),
      host: process.env.HOST || this.getDefaultHost(),
      
      // 数据库配置
      database: this.getDatabaseConfig(),
      
      // Redis配置
      redis: this.getRedisConfig(),
      
      // JWT配置
      jwt: this.getJWTConfig(),
      
      // CORS配置
      cors: this.getCorsConfig(),
      
      // 安全配置
      security: this.getSecurityConfig(),
      
      // 日志配置
      logging: this.getLoggingConfig(),
      
      // 邮件配置
      email: this.getEmailConfig(),
      
      // 文件上传配置
      upload: this.getUploadConfig(),
      
      // 第三方服务配置
      services: this.getServicesConfig()
    }
  }

  getDefaultPort() {
    return {
      development: 3000,
      staging: 8080,
      production: 8080
    }[this.environment]
  }

  getDefaultHost() {
    return {
      development: 'localhost',
      staging: '0.0.0.0',
      production: '0.0.0.0'
    }[this.environment]
  }

  /**
   * 数据库配置
   */
  getDatabaseConfig() {
    const uriKey = `MONGODB_URI_${this.environment.toUpperCase()}`
    const uri = process.env[uriKey] || process.env.MONGODB_URI || this.getDefaultMongoURI()

    return {
      uri,
      options: {
        maxPoolSize: this.environment === 'production' ? 20 : 10,
        minPoolSize: this.environment === 'production' ? 5 : 2,
        maxIdleTimeMS: 30000,
        serverSelectionTimeoutMS: 5000,
        socketTimeoutMS: 45000,
        retryWrites: true,
        w: 'majority',
        ...(this.environment === 'production' && {
          ssl: true,
          sslValidate: true
        })
      }
    }
  }

  getDefaultMongoURI() {
    return {
      development: 'mongodb://localhost:27017/app_dev',
      staging: 'mongodb://localhost:27017/app_staging',
      production: null // 生产环境必须提供
    }[this.environment]
  }

  /**
   * Redis配置
   */
  getRedisConfig() {
    const redisUrl = process.env.REDIS_URL
    
    if (redisUrl) {
      return { url: redisUrl }
    }

    return {
      host: process.env.REDIS_HOST || 'localhost',
      port: parseInt(process.env.REDIS_PORT, 10) || 6379,
      password: process.env.REDIS_PASSWORD,
      db: parseInt(process.env.REDIS_DB, 10) || 0,
      retryDelayOnFailover: 100,
      maxRetriesPerRequest: 3,
      ...(this.environment === 'production' && {
        enableReadyCheck: true,
        lazyConnect: true
      })
    }
  }

  /**
   * JWT配置
   */
  getJWTConfig() {
    const secret = process.env.JWT_SECRET || this.getDefaultJWTSecret()
    
    return {
      secret,
      accessTokenExpiry: process.env.JWT_ACCESS_EXPIRY || '15m',
      refreshTokenExpiry: process.env.JWT_REFRESH_EXPIRY || '7d',
      issuer: process.env.JWT_ISSUER || 'your-app',
      audience: process.env.JWT_AUDIENCE || 'your-app-users',
      algorithm: 'HS256'
    }
  }

  getDefaultJWTSecret() {
    if (this.environment === 'production') {
      throw new Error('JWT_SECRET is required in production')
    }
    return `dev_jwt_secret_${this.environment}_not_for_production`
  }

  /**
   * CORS配置
   */
  getCorsConfig() {
    const origins = this.getAllowedOrigins()
    
    return {
      origin: origins,
      methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
      allowedHeaders: [
        'Origin',
        'X-Requested-With',
        'Content-Type',
        'Accept',
        'Authorization',
        'X-API-Key'
      ],
      exposedHeaders: ['X-Total-Count', 'X-Page-Count'],
      credentials: true,
      maxAge: this.environment === 'production' ? 86400 : 0, // 24小时缓存
      preflightContinue: false,
      optionsSuccessStatus: 204
    }
  }

  getAllowedOrigins() {
    const originsEnv = process.env.ALLOWED_ORIGINS
    
    if (originsEnv) {
      return originsEnv.split(',').map(origin => origin.trim())
    }

    // 默认允许的源
    const defaultOrigins = {
      development: [
        'http://localhost:3000',
        'http://localhost:5173',
        'http://localhost:8080',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:5173'
      ],
      staging: [
        'https://staging.yourdomain.com',
        'https://test.yourdomain.com'
      ],
      production: [] // 生产环境必须明确指定
    }

    return defaultOrigins[this.environment] || []
  }

  /**
   * 安全配置
   */
  getSecurityConfig() {
    return {
      // 密码加密配置
      bcrypt: {
        saltRounds: this.environment === 'production' ? 12 : 10
      },
      
      // 速率限制配置
      rateLimit: {
        windowMs: 15 * 60 * 1000, // 15分钟
        max: this.environment === 'production' ? 100 : 1000,
        standardHeaders: true,
        legacyHeaders: false,
        message: {
          error: 'Too many requests, please try again later'
        }
      },
      
      // Helmet安全头配置
      helmet: {
        contentSecurityPolicy: this.environment === 'production',
        crossOriginEmbedderPolicy: this.environment === 'production',
        hsts: this.environment === 'production' ? {
          maxAge: 31536000,
          includeSubDomains: true,
          preload: true
        } : false
      },
      
      // 会话配置
      session: {
        secret: process.env.SESSION_SECRET || this.getDefaultSessionSecret(),
        name: 'sessionId',
        resave: false,
        saveUninitialized: false,
        cookie: {
          secure: this.environment === 'production',
          httpOnly: true,
          maxAge: 24 * 60 * 60 * 1000, // 24小时
          sameSite: this.environment === 'production' ? 'strict' : 'lax'
        }
      }
    }
  }

  getDefaultSessionSecret() {
    if (this.environment === 'production') {
      throw new Error('SESSION_SECRET is required in production')
    }
    return `dev_session_secret_${this.environment}`
  }

  /**
   * 日志配置
   */
  getLoggingConfig() {
    return {
      level: process.env.LOG_LEVEL || this.getDefaultLogLevel(),
      format: this.environment === 'production' ? 'json' : 'combined',
      
      // 控制台日志
      console: {
        enabled: this.environment !== 'production',
        colorize: this.environment === 'development',
        timestamp: true
      },
      
      // 文件日志
      file: {
        enabled: this.environment !== 'development',
        filename: `logs/app-${this.environment}.log`,
        maxsize: 10 * 1024 * 1024, // 10MB
        maxFiles: 5,
        tailable: true
      },
      
      // 错误日志
      error: {
        enabled: true,
        filename: `logs/error-${this.environment}.log`,
        level: 'error'
      }
    }
  }

  getDefaultLogLevel() {
    return {
      development: 'debug',
      staging: 'info',
      production: 'warn'
    }[this.environment]
  }

  /**
   * 邮件配置
   */
  getEmailConfig() {
    return {
      smtp: {
        host: process.env.SMTP_HOST,
        port: parseInt(process.env.SMTP_PORT, 10) || 587,
        secure: process.env.SMTP_SECURE === 'true',
        auth: {
          user: process.env.SMTP_USER,
          pass: process.env.SMTP_PASS
        }
      },
      from: process.env.SMTP_FROM || 'noreply@yourdomain.com',
      templates: {
        path: path.resolve(process.cwd(), 'templates/emails'),
        options: {
          extension: 'hbs',
          layoutsDir: 'layouts',
          defaultLayout: 'main'
        }
      }
    }
  }

  /**
   * 文件上传配置
   */
  getUploadConfig() {
    return {
      // 文件大小限制
      limits: {
        fileSize: this.environment === 'production' ? 10 * 1024 * 1024 : 50 * 1024 * 1024, // 生产10MB，开发50MB
        files: 5, // 最多5个文件
        fields: 20 // 最多20个字段
      },
      
      // 允许的文件类型
      allowedTypes: [
        'image/jpeg',
        'image/png',
        'image/gif',
        'image/webp',
        'application/pdf',
        'text/plain',
        'application/json'
      ],
      
      // 存储配置
      storage: {
        type: process.env.STORAGE_TYPE || 'local', // local, s3, cloudinary
        local: {
          destination: path.resolve(process.cwd(), 'uploads'),
          publicPath: '/uploads'
        },
        s3: {
          bucket: process.env.AWS_S3_BUCKET,
          region: process.env.AWS_REGION || 'us-east-1',
          accessKeyId: process.env.AWS_ACCESS_KEY_ID,
          secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
        }
      }
    }
  }

  /**
   * 第三方服务配置
   */
  getServicesConfig() {
    return {
      // 支付服务
      payment: {
        stripe: {
          secretKey: process.env.STRIPE_SECRET_KEY,
          publishableKey: process.env.STRIPE_PUBLISHABLE_KEY,
          webhookSecret: process.env.STRIPE_WEBHOOK_SECRET
        }
      },
      
      // 监控服务
      monitoring: {
        sentry: {
          dsn: process.env.SENTRY_DSN,
          environment: this.environment,
          enabled: this.environment !== 'development'
        }
      },
      
      // 缓存服务
      cache: {
        redis: this.getRedisConfig(),
        ttl: {
          default: 300, // 5分钟
          user: 900,    // 15分钟
          static: 3600  // 1小时
        }
      }
    }
  }
}

// 创建并导出环境管理器实例
const envManager = new AdvancedEnvironmentManager()
module.exports = envManager.getConfig()
module.exports.envManager = envManager
```

### Express应用完整配置
```javascript
// app.js - Express应用完整配置
const express = require('express')
const cors = require('cors')
const helmet = require('helmet')
const compression = require('compression')
const rateLimit = require('express-rate-limit')
const session = require('express-session')
const MongoStore = require('connect-mongo')
const morgan = require('morgan')
const path = require('path')

const config = require('./config/environment')
const errorHandler = require('./middlewares/errorHandler')
const notFoundHandler = require('./middlewares/notFoundHandler')
const requestLogger = require('./middlewares/requestLogger')
const authMiddleware = require('./middlewares/auth')

class AppBuilder {
  constructor() {
    this.app = express()
    this.setupApp()
  }

  /**
   * 设置Express应用
   */
  setupApp() {
    // 基础中间件
    this.setupBasicMiddlewares()
    
    // 安全中间件
    this.setupSecurityMiddlewares()
    
    // 业务中间件
    this.setupBusinessMiddlewares()
    
    // 路由
    this.setupRoutes()
    
    // 错误处理
    this.setupErrorHandling()
  }

  /**
   * 基础中间件
   */
  setupBasicMiddlewares() {
    // 压缩响应
    this.app.use(compression())
    
    // 请求日志
    if (config.environment !== 'test') {
      this.app.use(morgan(config.environment === 'production' ? 'combined' : 'dev'))
    }
    
    // 静态文件服务
    this.app.use('/uploads', express.static(path.join(__dirname, '../uploads')))
    this.app.use('/public', express.static(path.join(__dirname, '../public')))
    
    // 请求解析
    this.app.use(express.json({ 
      limit: '10mb',
      verify: this.rawBodyParser
    }))
    this.app.use(express.urlencoded({ 
      extended: true, 
      limit: '10mb' 
    }))
  }

  /**
   * 原始请求体解析器（用于webhook验证）
   */
  rawBodyParser(req, res, buf, encoding) {
    if (buf && buf.length) {
      req.rawBody = buf.toString(encoding || 'utf8')
    }
  }

  /**
   * 安全中间件
   */
  setupSecurityMiddlewares() {
    // Helmet安全头
    this.app.use(helmet(config.security.helmet))
    
    // CORS跨域
    this.app.use(cors(config.cors))
    
    // 速率限制
    const limiter = rateLimit(config.security.rateLimit)
    this.app.use('/api/', limiter)
    
    // 会话管理
    this.app.use(session({
      ...config.security.session,
      store: MongoStore.create({
        mongoUrl: config.database.uri,
        touchAfter: 24 * 3600 // lazy session update
      })
    }))
    
    // 信任代理（用于生产环境负载均衡）
    if (config.environment === 'production') {
      this.app.set('trust proxy', 1)
    }
  }

  /**
   * 业务中间件
   */
  setupBusinessMiddlewares() {
    // 请求日志记录
    this.app.use(requestLogger)
    
    // 健康检查
    this.app.get('/health', (req, res) => {
      res.status(200).json({
        status: 'OK',
        environment: config.environment,
        timestamp: new Date().toISOString(),
        uptime: process.uptime(),
        memory: process.memoryUsage()
      })
    })
    
    // API版本信息
    this.app.get('/api', (req, res) => {
      res.json({
        name: 'Your API',
        version: '1.0.0',
        environment: config.environment,
        documentation: '/api/docs'
      })
    })
  }

  /**
   * 设置路由
   */
  setupRoutes() {
    // 认证路由（无需token）
    this.app.use('/api/auth', require('./routes/auth'))
    
    // 公共路由（无需token）
    this.app.use('/api/public', require('./routes/public'))
    
    // 受保护的API路由（需要token）
    this.app.use('/api/users', authMiddleware.authenticateToken, require('./routes/users'))
    this.app.use('/api/admin', authMiddleware.authenticateToken, authMiddleware.requireRole('admin'), require('./routes/admin'))
    
    // 文件上传路由
    this.app.use('/api/upload', authMiddleware.authenticateToken, require('./routes/upload'))
    
    // Webhook路由（特殊处理）
    this.app.use('/api/webhooks', require('./routes/webhooks'))
  }

  /**
   * 错误处理
   */
  setupErrorHandling() {
    // 404处理
    this.app.use(notFoundHandler)
    
    // 全局错误处理
    this.app.use(errorHandler)
  }

  /**
   * 获取应用实例
   */
  getApp() {
    return this.app
  }
}

module.exports = new AppBuilder().getApp()
```

### 数据库连接管理
```javascript
// config/database.js - 数据库连接管理
const mongoose = require('mongoose')
const config = require('./environment')

class DatabaseManager {
  constructor() {
    this.connection = null
    this.retryCount = 0
    this.maxRetries = 5
    this.retryDelay = 5000
  }

  /**
   * 连接数据库
   */
  async connect() {
    try {
      console.log('🔌 Connecting to MongoDB...')
      
      this.connection = await mongoose.connect(config.database.uri, config.database.options)
      
      console.log('✅ MongoDB connected successfully')
      console.log(`📍 Database: ${this.connection.connection.name}`)
      
      this.setupEventListeners()
      this.retryCount = 0
      
      return this.connection
      
    } catch (error) {
      console.error('❌ MongoDB connection failed:', error.message)
      
      if (this.retryCount < this.maxRetries) {
        this.retryCount++
        console.log(`🔄 Retrying connection in ${this.retryDelay / 1000}s (attempt ${this.retryCount}/${this.maxRetries})`)
        
        await new Promise(resolve => setTimeout(resolve, this.retryDelay))
        return this.connect()
      } else {
        console.error('💥 Max connection retries reached, exiting...')
        process.exit(1)
      }
    }
  }

  /**
   * 设置连接事件监听器
   */
  setupEventListeners() {
    const db = mongoose.connection

    db.on('error', (error) => {
      console.error('❌ MongoDB connection error:', error)
    })

    db.on('disconnected', () => {
      console.warn('⚠️ MongoDB disconnected')
      if (config.environment === 'production') {
        this.reconnect()
      }
    })

    db.on('reconnected', () => {
      console.log('🔄 MongoDB reconnected')
    })

    // 优雅关闭
    process.on('SIGINT', () => {
      this.disconnect()
    })

    process.on('SIGTERM', () => {
      this.disconnect()
    })
  }

  /**
   * 重新连接
   */
  async reconnect() {
    try {
      await mongoose.disconnect()
      await this.connect()
    } catch (error) {
      console.error('❌ Reconnection failed:', error)
    }
  }

  /**
   * 断开连接
   */
  async disconnect() {
    try {
      await mongoose.disconnect()
      console.log('👋 MongoDB disconnected gracefully')
      process.exit(0)
    } catch (error) {
      console.error('❌ Error during disconnection:', error)
      process.exit(1)
    }
  }

  /**
   * 获取连接状态
   */
  getConnectionState() {
    const states = {
      0: 'disconnected',
      1: 'connected',
      2: 'connecting',
      3: 'disconnecting'
    }
    
    return {
      state: states[mongoose.connection.readyState],
      host: mongoose.connection.host,
      port: mongoose.connection.port,
      name: mongoose.connection.name
    }
  }
}

module.exports = new DatabaseManager()
```

### 环境变量配置文件示例

```bash
# .env.development
NODE_ENV=development
PORT=3000
HOST=localhost

# 数据库配置
MONGODB_URI_DEVELOPMENT=mongodb://localhost:27017/yourapp_dev

# Redis配置  
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# JWT配置
JWT_SECRET=your_development_jwt_secret_key
JWT_ACCESS_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# 会话配置
SESSION_SECRET=your_development_session_secret

# 日志配置
LOG_LEVEL=debug

# 邮件配置
SMTP_HOST=smtp.mailtrap.io
SMTP_PORT=2525
SMTP_USER=your_mailtrap_user
SMTP_PASS=your_mailtrap_pass
SMTP_FROM=noreply@yourapp.com

# CORS配置
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# .env.production
NODE_ENV=production
PORT=8080
HOST=0.0.0.0

# 数据库配置
MONGODB_URI_PROD=mongodb+srv://username:password@cluster.mongodb.net/yourapp_prod

# Redis配置
REDIS_URL=redis://username:password@redis-host:6379

# JWT配置
JWT_SECRET=your_super_secure_production_jwt_secret_key
JWT_ACCESS_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d
JWT_ISSUER=yourapp.com
JWT_AUDIENCE=yourapp-users

# 会话配置
SESSION_SECRET=your_super_secure_production_session_secret

# 日志配置
LOG_LEVEL=warn

# 邮件配置
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASS=your_sendgrid_api_key
SMTP_FROM=noreply@yourapp.com

# CORS配置
ALLOWED_ORIGINS=https://yourapp.com,https://www.yourapp.com

# AWS配置
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_S3_BUCKET=yourapp-uploads

# 第三方服务
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

SENTRY_DSN=https://...@sentry.io/...
```

这个详细配置文档提供了完整的Node.js后端环境配置方案，包含了环境检测、数据库连接、安全配置、日志管理等各个方面的详细实现。 