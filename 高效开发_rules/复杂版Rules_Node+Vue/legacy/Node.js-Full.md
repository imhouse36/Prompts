---
description: Node.js and Express.js best practices for backend development
globs: **/*.js, **/*.ts, src/**/*.ts
---

# Node.js + Express + MongoDB + Vue.js 开发规范 (.cursorrules)

## 🎯 项目技术栈规范

### 核心技术栈
- **后端**: Node.js + Express.js
- **数据库**: MongoDB + Mongoose ODM
- **前端**: Vue.js (管理面板)
- **认证**: JSON Web Tokens (JWT)
- **版本控制**: Git
- **部署**: 适配本地调试与线上生产环境同时支持，自动环境检测和切换，完美支持双环境运行
- **测试**: Jest/Mocha + Supertest

### 环境支持要求
- 本地调试环境自动检测和智能切换
- 生产环境无缝部署和自动切换
- 完整的CORS跨域支持和域名白名单机制
- 双环境配置文件自动加载
- 开发/生产数据库自动切换
- API接口环境自适应

## 📁 项目结构规范

```bash
project-root/
├── server/               # 后端服务目录
│   ├── src/              # 主源代码目录
│   │   ├── config/       # 配置文件
│   │   │   ├── database.js    # 数据库配置
│   │   │   ├── cors.js        # CORS配置
│   │   │   ├── environment.js # 环境检测配置
│   │   │   └── index.js       # 统一配置入口
│   │   ├── controllers/  # 控制器（业务逻辑）
│   │   ├── routes/       # 路由定义
│   │   ├── middlewares/  # 自定义中间件
│   │   │   ├── auth.js        # JWT认证中间件
│   │   │   ├── errorHandler.js
│   │   │   └── validation.js  # 输入验证中间件
│   │   ├── models/       # Mongoose数据模型
│   │   ├── services/     # 业务逻辑层
│   │   ├── utils/        # 工具函数
│   │   │   ├── logger.js      # 日志工具
│   │   │   ├── encryption.js  # 加密工具
│   │   │   └── helpers.js     # 通用助手函数
│   │   └── app.js        # Express应用初始化
│   ├── tests/            # 后端测试目录
│   │   ├── unit/         # 单元测试
│   │   ├── integration/  # 集成测试
│   │   └── e2e/          # 端到端测试
│   ├── .env.development  # 开发环境变量
│   ├── .env.production   # 生产环境变量
│   ├── package.json      # 后端依赖
│   └── server.js         # 服务入口文件
├── client/               # Vue.js前端目录
│   ├── src/
│   │   ├── components/   # Vue组件
│   │   │   ├── common/   # 公共组件
│   │   │   ├── layout/   # 布局组件
│   │   │   └── business/ # 业务组件
│   │   ├── views/        # 页面视图
│   │   ├── router/       # Vue Router配置
│   │   ├── store/        # Vuex/Pinia状态管理
│   │   ├── composables/  # Vue 3 Composition API
│   │   ├── api/          # API服务层
│   │   │   ├── config.js # API配置和环境检测
│   │   │   ├── auth.js   # 认证相关API
│   │   │   └── modules/  # 业务模块API
│   │   ├── utils/        # 前端工具函数
│   │   ├── styles/       # 样式文件
│   │   │   ├── variables.scss # SCSS变量
│   │   │   ├── mixins.scss    # SCSS混入
│   │   │   └── components/    # 组件样式
│   │   ├── assets/       # 静态资源
│   │   └── main.js       # Vue应用入口
│   ├── public/
│   ├── .env.development  # 前端开发环境变量
│   ├── .env.production   # 前端生产环境变量
│   ├── vue.config.js     # Vue CLI配置
│   └── package.json      # 前端依赖
├── shared/               # 前后端共享
│   ├── types/            # TypeScript类型定义
│   ├── constants/        # 共享常量
│   └── utils/            # 共享工具函数
├── docker/               # Docker配置
├── docs/                 # 项目文档
├── .gitignore           # Git忽略文件
├── package.json         # 项目根依赖
└── README.md            # 项目说明
```

## 🔧 编码风格规范

### JavaScript/Node.js规范
```javascript
/**
 * 变量命名规范
 * - 变量和函数: camelCase
 * - 类名: PascalCase  
 * - 常量: UPPER_SNAKE_CASE
 * - 文件名: kebab-case
 * - Vue组件: PascalCase
 */

// ✅ 推荐写法
const userService = require('./services/user-service');
const MAX_LOGIN_ATTEMPTS = 3;

class UserController {
  /**
   * 获取用户信息
   * @param {Object} req - Express请求对象
   * @param {Object} res - Express响应对象
   * @returns {Promise<void>}
   */
  async getUser(req, res) {
    try {
      const { userId } = req.params;
      const user = await userService.findById(userId);
      
      if (!user) {
        return res.status(404).json({
          success: false,
          message: 'User not found'
        });
      }
      
      res.status(200).json({
        success: true,
        data: user
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: error.message
      });
    }
  }
}
```

### Vue.js编码规范
```vue
<!-- ✅ Vue组件标准格式 -->
<template>
  <div class="user-management">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">{{ pageTitle }}</h1>
      <el-button 
        type="primary" 
        @click="handleAddUser"
        :loading="isLoading"
      >
        添加用户
      </el-button>
    </div>
    
    <!-- 用户列表 -->
    <div class="user-list">
      <UserTable 
        :users="users" 
        :loading="tableLoading"
        @edit="handleEditUser"
        @delete="handleDeleteUser"
      />
    </div>
    
    <!-- 用户对话框 -->
    <UserDialog 
      v-model:visible="dialogVisible"
      :user="currentUser"
      @save="handleSaveUser"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useUserStore } from '@/store/modules/user'
import { useMessage } from '@/composables/useMessage'
import UserTable from '@/components/business/UserTable.vue'
import UserDialog from '@/components/business/UserDialog.vue'

/**
 * 用户管理页面组件
 * 功能：用户的增删改查操作
 */

// 状态管理
const userStore = useUserStore()
const { showSuccess, showError } = useMessage()

// 响应式数据
const isLoading = ref(false)
const tableLoading = ref(false)
const dialogVisible = ref(false)
const currentUser = ref(null)

// 计算属性
const pageTitle = computed(() => '用户管理')
const users = computed(() => userStore.users)

/**
 * 处理添加用户
 */
const handleAddUser = () => {
  currentUser.value = null
  dialogVisible.value = true
}

/**
 * 处理编辑用户
 * @param {Object} user - 用户对象
 */
const handleEditUser = (user) => {
  currentUser.value = { ...user }
  dialogVisible.value = true
}

/**
 * 处理删除用户
 * @param {Object} user - 用户对象
 */
const handleDeleteUser = async (user) => {
  try {
    await userStore.deleteUser(user.id)
    showSuccess('删除成功')
  } catch (error) {
    showError(`删除失败: ${error.message}`)
  }
}

/**
 * 处理保存用户
 * @param {Object} userData - 用户数据
 */
const handleSaveUser = async (userData) => {
  try {
    if (userData.id) {
      await userStore.updateUser(userData)
      showSuccess('更新成功')
    } else {
      await userStore.createUser(userData)
      showSuccess('创建成功')
    }
    dialogVisible.value = false
  } catch (error) {
    showError(`保存失败: ${error.message}`)
  }
}

/**
 * 加载用户列表
 */
const loadUsers = async () => {
  try {
    tableLoading.value = true
    await userStore.fetchUsers()
  } catch (error) {
    showError(`加载失败: ${error.message}`)
  } finally {
    tableLoading.value = false
  }
}

// 生命周期
onMounted(() => {
  loadUsers()
})
</script>

<style scoped lang="scss">
.user-management {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    
    .page-title {
      margin: 0;
      font-size: 24px;
      font-weight: 600;
      color: var(--color-text-primary);
    }
  }
  
  .user-list {
    background: var(--color-bg-container);
    border-radius: 8px;
    padding: 24px;
  }
}
</style>
```

## 🌍 环境自动检测和切换配置

### 后端环境配置
```javascript
// server/src/config/environment.js
/**
 * 环境自动检测和配置管理
 * 支持开发、测试、生产环境自动切换
 */
class EnvironmentManager {
  constructor() {
    this.environment = this.detectEnvironment()
    this.loadEnvironmentConfig()
  }
  
  /**
   * 自动检测运行环境
   * @returns {string} 环境类型
   */
  detectEnvironment() {
    // 1. 优先使用NODE_ENV环境变量
    if (process.env.NODE_ENV) {
      return process.env.NODE_ENV
    }
    
    // 2. 根据启动方式检测
    if (process.argv.includes('--production')) {
      return 'production'
    }
    
    if (process.argv.includes('--development')) {
      return 'development'
    }
    
    // 3. 根据端口检测
    const port = process.env.PORT || 3000
    if (port === 80 || port === 443 || port > 8000) {
      return 'production'
    }
    
    // 4. 根据域名检测
    const hostname = process.env.HOSTNAME || require('os').hostname()
    if (hostname.includes('localhost') || hostname.includes('127.0.0.1')) {
      return 'development'
    }
    
    // 5. 默认开发环境
    return 'development'
  }
  
  /**
   * 加载对应环境的配置文件
   */
  loadEnvironmentConfig() {
    require('dotenv').config({
      path: `.env.${this.environment}`
    })
    
    // 设置环境变量
    process.env.NODE_ENV = this.environment
    
    console.log(`🌍 Environment detected: ${this.environment}`)
    console.log(`📋 Config loaded: .env.${this.environment}`)
  }
  
  /**
   * 获取当前环境配置
   * @returns {Object} 配置对象
   */
  getConfig() {
    const baseConfig = {
      environment: this.environment,
      port: parseInt(process.env.PORT, 10) || (this.environment === 'production' ? 8080 : 3000),
      
      // 数据库配置 - 自动切换
      database: {
        uri: this.environment === 'production'
          ? process.env.MONGODB_URI_PROD
          : process.env.MONGODB_URI_DEV || 'mongodb://localhost:27017/app_dev',
        options: {
          maxPoolSize: this.environment === 'production' ? 20 : 10
        }
      },
      
      // JWT配置
      jwt: {
        secret: process.env.JWT_SECRET || this.getDefaultJWTSecret(),
        expiresIn: process.env.JWT_EXPIRES_IN || '7d'
      },
      
      // CORS配置 - 自动切换
      cors: {
        origins: this.getCorsOrigins()
      },
      
      // 日志配置
      logging: {
        level: this.environment === 'production' ? 'error' : 'debug',
        enableConsole: this.environment !== 'production'
      }
    }
    
    return baseConfig
  }
  
  /**
   * 获取CORS允许的源
   * @returns {Array} 允许的源列表
   */
  getCorsOrigins() {
    if (this.environment === 'production') {
      return (process.env.ALLOWED_ORIGINS || '').split(',').filter(Boolean)
    } else {
      return [
        'http://localhost:8080',  // Vue开发服务器
        'http://localhost:3000',  // 备用端口
        'http://127.0.0.1:8080',
        'http://127.0.0.1:3000'
      ]
    }
  }
  
  /**
   * 获取默认JWT密钥
   * @returns {string} JWT密钥
   */
  getDefaultJWTSecret() {
    if (this.environment === 'production') {
      throw new Error('JWT_SECRET must be set in production environment')
    }
    return 'dev_jwt_secret_key_not_for_production'
  }
}

// 创建环境管理器实例
const envManager = new EnvironmentManager()
module.exports = envManager.getConfig()
```

### 前端环境配置
```javascript
// client/src/api/config.js
/**
 * 前端API配置和环境检测
 * 自动适配开发和生产环境
 */
class ApiConfig {
  constructor() {
    this.environment = this.detectEnvironment()
    this.baseURL = this.getBaseURL()
    this.timeout = this.getTimeout()
  }
  
  /**
   * 检测前端运行环境
   * @returns {string} 环境类型
   */
  detectEnvironment() {
    // 1. 使用Vue CLI的环境变量
    if (process.env.NODE_ENV) {
      return process.env.NODE_ENV
    }
    
    // 2. 根据域名检测
    const hostname = window.location.hostname
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return 'development'
    }
    
    // 3. 根据协议检测
    if (window.location.protocol === 'file:') {
      return 'development'
    }
    
    return 'production'
  }
  
  /**
   * 获取API基础URL
   * @returns {string} API基础URL
   */
  getBaseURL() {
    if (this.environment === 'production') {
      return process.env.VUE_APP_API_BASE_URL || '/api'
    } else {
      return process.env.VUE_APP_API_BASE_URL || 'http://localhost:3000/api'
    }
  }
  
  /**
   * 获取请求超时时间
   * @returns {number} 超时时间(毫秒)
   */
  getTimeout() {
    return this.environment === 'production' ? 10000 : 30000
  }
  
  /**
   * 获取完整配置
   * @returns {Object} 配置对象
   */
  getConfig() {
    return {
      environment: this.environment,
      baseURL: this.baseURL,
      timeout: this.timeout,
      headers: {
        'Content-Type': 'application/json'
      }
    }
  }
}

// 创建配置实例
const apiConfig = new ApiConfig()

// 导出配置
export default apiConfig.getConfig()

// 导出环境检测工具
export const isProduction = () => apiConfig.environment === 'production'
export const isDevelopment = () => apiConfig.environment === 'development'
```

### Vue.js项目配置
```javascript
// client/vue.config.js
const { defineConfig } = require('@vue/cli-service')

/**
 * Vue CLI配置
 * 支持开发和生产环境自动适配
 */
module.exports = defineConfig({
  // 基础配置
  publicPath: process.env.NODE_ENV === 'production' ? './' : '/',
  outputDir: 'dist',
  assetsDir: 'static',
  
  // 开发服务器配置
  devServer: {
    port: 8080,
    host: '0.0.0.0',
    hot: true,
    open: true,
    
    // 代理配置 - 解决开发环境跨域问题
    proxy: {
      '/api': {
        target: process.env.VUE_APP_API_BASE_URL || 'http://localhost:3000',
        changeOrigin: true,
        secure: false,
        logLevel: 'debug'
      }
    }
  },
  
  // 生产环境配置
  productionSourceMap: false,
  
  // CSS配置
  css: {
    loaderOptions: {
      scss: {
        additionalData: `
          @import "@/styles/variables.scss";
          @import "@/styles/mixins.scss";
        `
      }
    }
  },
  
  // 构建配置
  configureWebpack: config => {
    if (process.env.NODE_ENV === 'production') {
      // 生产环境优化
      config.optimization = {
        ...config.optimization,
        splitChunks: {
          chunks: 'all',
          cacheGroups: {
            vendor: {
              name: 'vendor',
              test: /[\\/]node_modules[\\/]/,
              priority: 10,
              chunks: 'initial'
            }
          }
        }
      }
    }
  },
  
  // 链式配置
  chainWebpack: config => {
    // 环境变量替换
    config.plugin('define').tap(definitions => {
      Object.assign(definitions[0]['process.env'], {
        BUILD_TIME: JSON.stringify(new Date().toISOString()),
        BUILD_ENV: JSON.stringify(process.env.NODE_ENV)
      })
      return definitions
    })
  }
})
```

## 🔐 CORS和安全配置

### 增强的CORS配置
```javascript
// server/src/config/cors.js
/**
 * CORS配置 - 支持动态域名白名单
 * 完美支持开发和生产环境
 */
const corsConfig = {
  /**
   * 动态Origin检查
   * @param {string} origin - 请求来源
   * @param {Function} callback - 回调函数
   */
  origin: function (origin, callback) {
    const config = require('./index')
    const allowedOrigins = config.cors.origins
    
    // 开发环境允许无Origin的请求(如Postman)
    if (config.environment === 'development' && !origin) {
      return callback(null, true)
    }
    
    // 检查白名单
    if (allowedOrigins.includes(origin)) {
      callback(null, true)
    } else {
      console.warn(`🚫 CORS blocked origin: ${origin}`)
      callback(new Error('Not allowed by CORS policy'))
    }
  },
  
  // 允许携带凭证
  credentials: true,
  
  // 允许的HTTP方法
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
  
  // 允许的请求头
  allowedHeaders: [
    'Origin',
    'X-Requested-With', 
    'Content-Type',
    'Accept',
    'Authorization',
    'X-Auth-Token'
  ],
  
  // 暴露的响应头
  exposedHeaders: ['X-Total-Count', 'X-Page-Count'],
  
  // 预检请求缓存时间
  maxAge: 86400, // 24小时
  
  // 处理预检请求
  preflightContinue: false,
  optionsSuccessStatus: 200
}

module.exports = corsConfig
```

## 🔄 API服务层设计

### Vue.js API服务
```javascript
// client/src/api/modules/auth.js
import axios from '@/api/axios-instance'

/**
 * 认证相关API服务
 */
export const authApi = {
  /**
   * 用户登录
   * @param {Object} credentials - 登录凭证
   * @param {string} credentials.email - 邮箱
   * @param {string} credentials.password - 密码
   * @returns {Promise<Object>} 登录结果
   */
  async login(credentials) {
    const response = await axios.post('/auth/login', credentials)
    return response.data
  },
  
  /**
   * 用户注册
   * @param {Object} userData - 用户数据
   * @returns {Promise<Object>} 注册结果
   */
  async register(userData) {
    const response = await axios.post('/auth/register', userData)
    return response.data
  },
  
  /**
   * 获取用户信息
   * @returns {Promise<Object>} 用户信息
   */
  async getUserInfo() {
    const response = await axios.get('/auth/me')
    return response.data
  },
  
  /**
   * 刷新Token
   * @returns {Promise<Object>} 新Token
   */
  async refreshToken() {
    const response = await axios.post('/auth/refresh')
    return response.data
  },
  
  /**
   * 用户登出
   * @returns {Promise<void>}
   */
  async logout() {
    await axios.post('/auth/logout')
  }
}
```

### Axios实例配置
```javascript
// client/src/api/axios-instance.js
import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { useAuthStore } from '@/store/modules/auth'
import apiConfig from './config'

/**
 * 创建Axios实例
 * 支持环境自适应和自动错误处理
 */
const instance = axios.create({
  baseURL: apiConfig.baseURL,
  timeout: apiConfig.timeout,
  headers: apiConfig.headers
})

/**
 * 请求拦截器
 * 自动添加认证头和请求日志
 */
instance.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    
    // 添加认证令牌
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    
    // 开发环境请求日志
    if (process.env.NODE_ENV === 'development') {
      console.log('🚀 API Request:', {
        method: config.method?.toUpperCase(),
        url: config.url,
        data: config.data,
        params: config.params
      })
    }
    
    return config
  },
  (error) => {
    console.error('❌ Request Error:', error)
    return Promise.reject(error)
  }
)

/**
 * 响应拦截器
 * 统一错误处理和Token刷新
 */
instance.interceptors.response.use(
  (response) => {
    // 开发环境响应日志
    if (process.env.NODE_ENV === 'development') {
      console.log('✅ API Response:', {
        status: response.status,
        url: response.config.url,
        data: response.data
      })
    }
    
    return response
  },
  async (error) => {
    const authStore = useAuthStore()
    
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          // Token过期，尝试刷新
          if (data.error?.code === 'TOKEN_EXPIRED' && authStore.refreshToken) {
            try {
              await authStore.refresh()
              // 重新发送原请求
              return instance.request(error.config)
            } catch (refreshError) {
              authStore.logout()
              router.push('/login')
              ElMessage.error('登录已过期，请重新登录')
            }
          } else {
            authStore.logout()
            router.push('/login')
            ElMessage.error('认证失败，请重新登录')
          }
          break
          
        case 403:
          ElMessage.error('权限不足')
          break
          
        case 404:
          ElMessage.error('请求的资源不存在')
          break
          
        case 422:
          const validationErrors = data.error?.details || {}
          const errorMessages = Object.values(validationErrors).flat()
          ElMessage.error(errorMessages.join(', ') || '数据验证失败')
          break
          
        case 500:
          ElMessage.error('服务器内部错误')
          break
          
        default:
          ElMessage.error(data.error?.message || '请求失败')
      }
    } else if (error.request) {
      ElMessage.error('网络连接失败，请检查网络')
    } else {
      ElMessage.error('请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

export default instance
```

## 📦 Vuex/Pinia状态管理

### Pinia Store示例
```javascript
// client/src/store/modules/auth.js
import { defineStore } from 'pinia'
import { authApi } from '@/api/modules/auth'

/**
 * 认证状态管理
 * 支持Token自动刷新和持久化
 */
export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('auth_token'),
    refreshToken: localStorage.getItem('refresh_token'),
    isAuthenticated: false,
    permissions: []
  }),
  
  getters: {
    /**
     * 检查用户是否已认证
     * @param {Object} state - 状态对象
     * @returns {boolean} 认证状态
     */
    isLoggedIn: (state) => !!state.token && !!state.user,
    
    /**
     * 获取用户角色
     * @param {Object} state - 状态对象  
     * @returns {string} 用户角色
     */
    userRole: (state) => state.user?.role || 'guest',
    
    /**
     * 检查用户权限
     * @param {Object} state - 状态对象
     * @returns {Function} 权限检查函数
     */
    hasPermission: (state) => (permission) => {
      return state.permissions.includes(permission)
    }
  },
  
  actions: {
    /**
     * 用户登录
     * @param {Object} credentials - 登录凭证
     */
    async login(credentials) {
      try {
        const response = await authApi.login(credentials)
        
        if (response.success) {
          const { user, token, refreshToken } = response.data
          
          this.setAuthData(user, token, refreshToken)
          this.isAuthenticated = true
          
          return response
        } else {
          throw new Error(response.error?.message || '登录失败')
        }
      } catch (error) {
        this.clearAuthData()
        throw error
      }
    },
    
    /**
     * 用户登出
     */
    async logout() {
      try {
        await authApi.logout()
      } catch (error) {
        console.warn('Logout API call failed:', error)
      } finally {
        this.clearAuthData()
        this.isAuthenticated = false
      }
    },
    
    /**
     * 刷新Token
     */
    async refresh() {
      try {
        const response = await authApi.refreshToken()
        
        if (response.success) {
          const { token, refreshToken } = response.data
          this.setTokens(token, refreshToken)
          return response
        } else {
          throw new Error('Token刷新失败')
        }
      } catch (error) {
        this.clearAuthData()
        throw error
      }
    },
    
    /**
     * 获取用户信息
     */
    async fetchUserInfo() {
      try {
        const response = await authApi.getUserInfo()
        
        if (response.success) {
          this.user = response.data.user
          this.permissions = response.data.permissions || []
          this.isAuthenticated = true
        }
        
        return response
      } catch (error) {
        this.clearAuthData()
        throw error
      }
    },
    
    /**
     * 设置认证数据
     * @param {Object} user - 用户信息
     * @param {string} token - 访问令牌
     * @param {string} refreshToken - 刷新令牌
     */
    setAuthData(user, token, refreshToken) {
      this.user = user
      this.setTokens(token, refreshToken)
    },
    
    /**
     * 设置令牌
     * @param {string} token - 访问令牌
     * @param {string} refreshToken - 刷新令牌
     */
    setTokens(token, refreshToken) {
      this.token = token
      this.refreshToken = refreshToken
      
      // 持久化存储
      localStorage.setItem('auth_token', token)
      if (refreshToken) {
        localStorage.setItem('refresh_token', refreshToken)
      }
    },
    
    /**
     * 清除认证数据
     */
    clearAuthData() {
      this.user = null
      this.token = null
      this.refreshToken = null
      this.permissions = []
      
      // 清除本地存储
      localStorage.removeItem('auth_token')
      localStorage.removeItem('refresh_token')
    }
  }
})
```

## 🚀 部署和运行脚本

### Package.json脚本配置
```json
{
  "name": "vue-express-app",
  "version": "1.0.0",
  "scripts": {
    "dev": "concurrently \"npm run server:dev\" \"npm run client:dev\"",
    "dev:server": "cd server && npm run dev",
    "dev:client": "cd client && npm run serve",
    
    "build": "npm run build:client && npm run build:server",
    "build:client": "cd client && npm run build",
    "build:server": "cd server && npm run build",
    
    "start": "npm run start:production",
    "start:production": "cd server && npm run start:production",
    "start:development": "npm run dev",
    
    "test": "npm run test:server && npm run test:client",
    "test:server": "cd server && npm test",
    "test:client": "cd client && npm test",
    
    "install:all": "npm install && cd server && npm install && cd ../client && npm install",
    "clean": "rm -rf node_modules server/node_modules client/node_modules",
    
    "docker:build": "docker build -t vue-express-app .",
    "docker:run": "docker run -p 8080:8080 vue-express-app"
  }
}
```

### 服务器启动脚本
```javascript
// server/server.js
const app = require('./src/app')
const config = require('./src/config')
const connectDatabase = require('./src/config/database')
const logger = require('./src/utils/logger')

/**
 * 服务器启动函数
 * 支持环境自动检测和优雅关闭
 */
async function startServer() {
  try {
    // 连接数据库
    await connectDatabase()
    
    // 启动服务器
    const server = app.listen(config.port, () => {
      logger.info(`🚀 Server running in ${config.environment} mode`)
      logger.info(`📍 Server address: http://localhost:${config.port}`)
      logger.info(`💾 Database: ${config.database.uri}`)
      logger.info(`🌐 CORS origins: ${config.cors.origins.join(', ')}`)
    })
    
    // 优雅关闭处理
    const gracefulShutdown = (signal) => {
      logger.info(`${signal} received. Starting graceful shutdown...`)
      
      server.close(() => {
        logger.info('HTTP server closed.')
        
        // 关闭数据库连接
        require('mongoose').connection.close(() => {
          logger.info('Database connection closed.')
          process.exit(0)
        })
      })
    }
    
    // 监听进程信号
    process.on('SIGTERM', () => gracefulShutdown('SIGTERM'))
    process.on('SIGINT', () => gracefulShutdown('SIGINT'))
    
    return server
  } catch (error) {
    logger.error('Failed to start server:', error)
    process.exit(1)
  }
}

// 启动服务器
startServer()
```

## 📋 环境变量配置模板

### 开发环境配置
```bash
# server/.env.development
NODE_ENV=development
PORT=3000

# 数据库配置
MONGODB_URI_DEV=mongodb://localhost:27017/app_dev

# JWT配置
JWT_SECRET=dev_jwt_secret_key_not_for_production_use_only
JWT_EXPIRES_IN=7d

# CORS配置(开发环境自动设置)
ALLOWED_ORIGINS=http://localhost:8080,http://localhost:3000

# 日志配置
LOG_LEVEL=debug

# 文件上传配置
MAX_UPLOAD_SIZE=10485760
ALLOWED_FILE_TYPES=jpg,jpeg,png,pdf
```

### 生产环境配置
```bash
# server/.env.production
NODE_ENV=production
PORT=8080

# 数据库配置
MONGODB_URI_PROD=mongodb://your-production-db-url/app_prod

# JWT配置
JWT_SECRET=your_super_secure_jwt_secret_key_here
JWT_EXPIRES_IN=1d

# CORS配置
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# 日志配置
LOG_LEVEL=error

# 安全配置
ENABLE_RATE_LIMITING=true
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX=100
```

### Vue.js环境配置
```bash
# client/.env.development
NODE_ENV=development
VUE_APP_API_BASE_URL=http://localhost:3000/api
VUE_APP_TITLE=应用管理后台 - 开发环境

# client/.env.production  
NODE_ENV=production
VUE_APP_API_BASE_URL=/api
VUE_APP_TITLE=应用管理后台
```

## 🎯 代码提交和质量控制

### ESLint配置
```javascript
// .eslintrc.js (项目根目录)
module.exports = {
  root: true,
  env: {
    node: true,
    es2021: true,
    browser: true
  },
  extends: [
    'eslint:recommended',
    '@vue/eslint-config-prettier'
  ],
  parserOptions: {
    ecmaVersion: 12,
    sourceType: 'module'
  },
  rules: {
    // 通用规则
    'indent': ['error', 2],
    'quotes': ['error', 'single'],
    'semi': ['error', 'always'],
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'warn',
    'no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
    
    // Vue.js特定规则
    'vue/multi-word-component-names': 'off',
    'vue/no-unused-components': 'warn',
    'vue/order-in-components': 'error',
    'vue/component-definition-name-casing': ['error', 'PascalCase'],
    
    // 安全规则
    'no-eval': 'error',
    'no-implied-eval': 'error',
    'no-new-func': 'error'
  },
  overrides: [
    {
      files: ['**/*.vue'],
      rules: {
        'vue/script-setup-uses-vars': 'error'
      }
    }
  ]
}
```

## 📚 总结

这个更新后的规范专门针对**Vue.js + Express + MongoDB**技术栈，提供了：

1. **完整的Vue.js开发规范** - Composition API、组件设计、状态管理
2. **智能环境检测** - 自动识别开发/生产环境并切换配置
3. **双环境完美支持** - 前后端配置自动适配，无需手动切换
4. **增强的CORS配置** - 动态白名单，支持多域名和开发调试
5. **API服务层设计** - Axios自动错误处理和Token刷新
6. **Pinia状态管理** - 现代化的Vue状态管理方案
7. **完整的构建流程** - 支持开发、测试、生产环境的完整部署流程


这个规范可以直接用作`.cursorrules`文件，为您的Vue.js + Express项目提供全面的开发指导。