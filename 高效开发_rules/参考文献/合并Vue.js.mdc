---
description: Vue.js best practices and patterns for modern web applications
globs: **/*.vue, **/*.ts, components/**/*
---

## 🎯 核心技术栈
- 使用 Vue 3.0 + Composition API 作为核心框架
- 使用 TypeScript 增强代码类型安全
- 使用 Pinia 进行状态管理
- 使用 Vue Router 进行路由管理
- 使用 ArcoDesign 作为UI组件库
- 使用 TailwindCSS 作为CSS框架
- 使用 Vite 作为构建工具
- 使用 Yarn 作为包管理器

## 🌍 环境配置规范
### 双环境架构原则
- 必须支持本地开发(development)和生产环境(production)自动切换
- 必须实现环境自动检测机制，避免手动配置
- 必须支持完整的CORS跨域处理
- 必须配置安全的域名白名单机制
- 所有环境相关配置必须统一管理

### 环境配置文件结构
project-root/
├── .env # 默认环境变量
├── .env.local # 本地私有变量（不提交到git）
├── .env.development # 开发环境变量
├── .env.production # 生产环境变量
├── config/
│ ├── env.ts # 环境配置管理
│ ├── api.ts # API配置管理
│ ├── cors.ts # CORS配置
│ └── security.ts # 安全配置
└── vite.config.ts # 构建工具配置

### 环境变量配置
```bash
# .env.development
NODE_ENV=development
VITE_APP_ENV=development
VITE_APP_TITLE=项目名称-开发环境
VITE_API_BASE_URL=http://localhost:3000/api
VITE_API_TIMEOUT=10000
VITE_ENABLE_MOCK=true
VITE_ENABLE_DEVTOOLS=true
VITE_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# .env.production
NODE_ENV=production
VITE_APP_ENV=production
VITE_APP_TITLE=项目名称
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_API_TIMEOUT=15000
VITE_ENABLE_MOCK=false
VITE_ENABLE_DEVTOOLS=false
VITE_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### 环境检测和配置管理
```typescript
// config/env.ts
/**
 * 环境配置管理器
 * @description 统一管理环境变量和配置，支持自动环境检测
 */
interface AppConfig {
  env: 'development' | 'production'
  title: string
  api: {
    baseURL: string
    timeout: number
  }
  features: {
    enableMock: boolean
    enableDevtools: boolean
  }
  security: {
    allowedOrigins: string[]
  }
}

/**
 * 自动检测当前运行环境
 * @returns 当前环境类型
 */
export const getCurrentEnvironment = (): 'development' | 'production' => {
  // 1. 优先检查 NODE_ENV
  if (import.meta.env.NODE_ENV === 'production') {
    return 'production'
  }
  
  // 2. 检查构建模式
  if (import.meta.env.PROD) {
    return 'production'
  }
  
  // 3. 检查域名
  if (typeof window !== 'undefined') {
    const hostname = window.location.hostname
    const productionDomains = ['yourdomain.com', 'www.yourdomain.com']
    if (productionDomains.includes(hostname)) {
      return 'production'
    }
  }
  
  // 4. 默认为开发环境
  return 'development'
}

/**
 * 获取应用配置
 * @returns 完整的应用配置对象
 */
export const getAppConfig = (): AppConfig => {
  const env = getCurrentEnvironment()
  
  return {
    env,
    title: import.meta.env.VITE_APP_TITLE || '项目名称',
    api: {
      baseURL: import.meta.env.VITE_API_BASE_URL || (
        env === 'production' 
          ? 'https://api.yourdomain.com' 
          : 'http://localhost:3000/api'
      ),
      timeout: Number(import.meta.env.VITE_API_TIMEOUT) || (
        env === 'production' ? 15000 : 10000
      )
    },
    features: {
      enableMock: import.meta.env.VITE_ENABLE_MOCK === 'true' && env === 'development',
      enableDevtools: import.meta.env.VITE_ENABLE_DEVTOOLS === 'true' || env === 'development'
    },
    security: {
      allowedOrigins: (import.meta.env.VITE_ALLOWED_ORIGINS || '').split(',').filter(Boolean)
    }
  }
}

// 导出配置实例
export const appConfig = getAppConfig()
```

### API配置管理
```typescript
// config/api.ts
import { appConfig } from './env'

/**
 * API配置管理
 * @description 根据环境自动配置API请求参数
 */
export interface ApiConfig {
  baseURL: string
  timeout: number
  withCredentials: boolean
  headers: Record<string, string>
}

/**
 * 获取API配置
 * @returns API配置对象
 */
export const getApiConfig = (): ApiConfig => {
  const config: ApiConfig = {
    baseURL: appConfig.api.baseURL,
    timeout: appConfig.api.timeout,
    withCredentials: appConfig.env === 'production', // 生产环境启用凭证
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest'
    }
  }

  // 开发环境添加调试头
  if (appConfig.env === 'development') {
    config.headers['X-Debug-Mode'] = 'true'
  }

  // 生产环境添加安全头
  if (appConfig.env === 'production') {
    config.headers['X-Env'] = 'production'
  }

  return config
}
```

### CORS跨域配置
```typescript
// config/cors.ts
import { appConfig } from './env'

/**
 * CORS配置管理
 * @description 处理跨域请求配置
 */
export interface CorsConfig {
  allowedOrigins: string[]
  allowedMethods: string[]
  allowedHeaders: string[]
  exposedHeaders: string[]
  credentials: boolean
  maxAge: number
}

/**
 * 获取CORS配置
 * @returns CORS配置对象
 */
export const getCorsConfig = (): CorsConfig => {
  return {
    allowedOrigins: appConfig.security.allowedOrigins,
    allowedMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
    allowedHeaders: [
      'Content-Type',
      'Authorization',
      'X-Requested-With',
      'Accept',
      'Origin',
      'Access-Control-Request-Method',
      'Access-Control-Request-Headers'
    ],
    exposedHeaders: ['X-Total-Count', 'X-Page-Size'],
    credentials: true,
    maxAge: appConfig.env === 'production' ? 86400 : 0 // 生产环境缓存1天
  }
}

/**
 * 验证请求来源是否合法
 * @param origin 请求来源
 * @returns 是否允许该来源
 */
export const isOriginAllowed = (origin: string): boolean => {
  if (!origin) return false
  
  const config = getCorsConfig()
  
  // 开发环境允许localhost
  if (appConfig.env === 'development') {
    if (origin.includes('localhost') || origin.includes('127.0.0.1')) {
      return true
    }
  }
  
  return config.allowedOrigins.includes(origin)
}
```

### HTTP请求工具配置
```typescript
// utils/request.ts
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { getApiConfig } from '@/config/api'
import { appConfig } from '@/config/env'

/**
 * 创建HTTP请求实例
 * @description 根据环境自动配置请求参数
 */
class RequestManager {
  private instance: AxiosInstance
  
  constructor() {
    const config = getApiConfig()
    
    this.instance = axios.create(config)
    this.setupInterceptors()
  }
  
  /**
   * 设置请求拦截器
   */
  private setupInterceptors() {
    // 请求拦截器
    this.instance.interceptors.request.use(
      (config) => {
        // 开发环境日志
        if (appConfig.env === 'development') {
          console.log('🚀 API Request:', config)
        }
        
        // 添加认证token
        const token = this.getAuthToken()
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        
        return config
      },
      (error) => {
        if (appConfig.env === 'development') {
          console.error('❌ Request Error:', error)
        }
        return Promise.reject(error)
      }
    )
    
    // 响应拦截器
    this.instance.interceptors.response.use(
      (response: AxiosResponse) => {
        if (appConfig.env === 'development') {
          console.log('✅ API Response:', response)
        }
        return response
      },
      (error) => {
        this.handleResponseError(error)
        return Promise.reject(error)
      }
    )
  }
  
  /**
   * 处理响应错误
   */
  private handleResponseError(error: any) {
    if (appConfig.env === 'development') {
      console.error('❌ Response Error:', error)
    }
    
    // 处理跨域错误
    if (error.code === 'ERR_NETWORK') {
      console.error('🌐 网络错误或CORS问题，请检查API服务器配置')
    }
    
    // 处理认证错误
    if (error.response?.status === 401) {
      this.handleAuthError()
    }
  }
  
  /**
   * 获取认证token
   */
  private getAuthToken(): string | null {
    return localStorage.getItem('auth_token')
  }
  
  /**
   * 处理认证错误
   */
  private handleAuthError() {
    localStorage.removeItem('auth_token')
    // 跳转到登录页面或触发重新登录
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  }
  
  /**
   * GET请求
   */
  get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.get(url, config).then(response => response.data)
  }
  
  /**
   * POST请求
   */
  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.post(url, data, config).then(response => response.data)
  }
  
  /**
   * PUT请求
   */
  put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.put(url, data, config).then(response => response.data)
  }
  
  /**
   * DELETE请求
   */
  delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.delete(url, config).then(response => response.data)
  }
}

// 导出请求实例
export const request = new RequestManager()
```

### Vite构建配置
```typescript
// vite.config.ts
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
import { getCorsConfig } from './config/cors'

export default defineConfig(({ command, mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd(), '')
  const corsConfig = getCorsConfig()
  
  return {
    plugins: [vue()],
    
    // 路径别名
    resolve: {
      alias: {
        '@': resolve(__dirname, 'src')
      }
    },
    
    // 开发服务器配置
    server: {
      host: '0.0.0.0',
      port: 5173,
      cors: {
        origin: (origin, callback) => {
          // 开发环境允许所有localhost请求
          if (!origin || origin.includes('localhost') || origin.includes('127.0.0.1')) {
            return callback(null, true)
          }
          
          // 检查白名单
          const allowed = corsConfig.allowedOrigins.includes(origin)
          callback(allowed ? null : new Error('Not allowed by CORS'), allowed)
        },
        credentials: corsConfig.credentials,
        methods: corsConfig.allowedMethods,
        allowedHeaders: corsConfig.allowedHeaders,
        exposedHeaders: corsConfig.exposedHeaders
      },
      
      // 开发环境代理配置
      proxy: mode === 'development' ? {
        '/api': {
          target: env.VITE_API_BASE_URL || 'http://localhost:3000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
        }
      } : undefined
    },
    
    // 构建配置
    build: {
      target: 'es2015',
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: mode === 'development',
      minify: mode === 'production',
      
      rollupOptions: {
        output: {
          // 分包策略
          manualChunks: {
            vendor: ['vue', 'vue-router', 'pinia'],
            ui: ['@arco-design/web-vue']
          }
        }
      }
    },
    
    // 环境变量前缀
    envPrefix: 'VITE_',
    
    // 定义全局变量
    define: {
      __APP_ENV__: JSON.stringify(mode),
      __BUILD_TIME__: JSON.stringify(new Date().toISOString())
    }
  }
})
```

### 安全域名白名单机制
```typescript
// config/security.ts
import { appConfig } from './env'

/**
 * 安全配置管理
 * @description 管理域名白名单和安全策略
 */
export interface SecurityConfig {
  allowedDomains: string[]
  allowedProtocols: string[]
  csrfProtection: boolean
  rateLimitConfig: {
    windowMs: number
    maxRequests: number
  }
}

/**
 * 获取安全配置
 */
export const getSecurityConfig = (): SecurityConfig => {
  return {
    allowedDomains: appConfig.security.allowedOrigins.map(origin => {
      try {
        return new URL(origin).hostname
      } catch {
        return origin
      }
    }),
    allowedProtocols: appConfig.env === 'production' ? ['https:'] : ['http:', 'https:'],
    csrfProtection: appConfig.env === 'production',
    rateLimitConfig: {
      windowMs: 15 * 60 * 1000, // 15分钟
      maxRequests: appConfig.env === 'production' ? 100 : 1000
    }
  }
}

/**
 * 验证域名是否在白名单中
 * @param domain 要验证的域名
 * @returns 是否允许该域名
 */
export const isDomainAllowed = (domain: string): boolean => {
  const config = getSecurityConfig()
  
  // 开发环境允许localhost
  if (appConfig.env === 'development') {
    if (domain === 'localhost' || domain === '127.0.0.1' || domain.endsWith('.local')) {
      return true
    }
  }
  
  return config.allowedDomains.includes(domain)
}

/**
 * 验证协议是否安全
 * @param protocol 协议类型
 * @returns 是否为安全协议
 */
export const isProtocolSecure = (protocol: string): boolean => {
  const config = getSecurityConfig()
  return config.allowedProtocols.includes(protocol)
}
```

### 环境感知的组合式API
```typescript
// composables/useEnvironment.ts
import { computed, readonly } from 'vue'
import { appConfig } from '@/config/env'

/**
 * 环境感知的组合式API
 * @description 提供环境相关的响应式状态和方法
 */
export function useEnvironment() {
  /**
   * 当前环境
   */
  const currentEnv = computed(() => appConfig.env)
  
  /**
   * 是否为开发环境
   */
  const isDevelopment = computed(() => appConfig.env === 'development')
  
  /**
   * 是否为生产环境
   */
  const isProduction = computed(() => appConfig.env === 'production')
  
  /**
   * 是否启用调试模式
   */
  const isDebugMode = computed(() => appConfig.features.enableDevtools)
  
  /**
   * 是否启用Mock数据
   */
  const isMockEnabled = computed(() => appConfig.features.enableMock)
  
  /**
   * 获取API基础URL
   */
  const getApiBaseUrl = () => appConfig.api.baseURL
  
  /**
   * 根据环境执行不同逻辑
   * @param handlers 环境处理器
   */
  const runByEnvironment = (handlers: {
    development?: () => void
    production?: () => void
  }) => {
    const handler = handlers[appConfig.env]
    if (handler) {
      handler()
    }
  }
  
  /**
   * 环境相关的日志输出
   * @param message 日志消息
   * @param type 日志类型
   */
  const envLog = (message: string, type: 'log' | 'warn' | 'error' = 'log') => {
    if (isDevelopment.value) {
      console[type](mdc:`[${appConfig.env.toUpperCase()}] ${message}`)
    }
  }
  
  return {
    // 状态
    currentEnv: readonly(currentEnv),
    isDevelopment: readonly(isDevelopment),
    isProduction: readonly(isProduction),
    isDebugMode: readonly(isDebugMode),
    isMockEnabled: readonly(isMockEnabled),
    
    // 方法
    getApiBaseUrl,
    runByEnvironment,
    envLog
  }
}
```

## 📁 目录结构规范
src/
├── assets/                 # 静态资源
│   ├── images/            # 图片资源
│   │   ├── icons/         # 图标文件
│   │   ├── logos/         # Logo文件
│   │   └── backgrounds/   # 背景图片
│   └── styles/            # 全局样式
│       ├── variables.css  # CSS变量定义
│       ├── base.css       # 基础样式
│       └── tailwind.css   # TailwindCSS配置
├── components/             # 公共组件
│   ├── base/              # 基础组件
│   │   ├── BaseButton.vue
│   │   ├── BaseInput.vue
│   │   ├── BaseForm.vue
│   │   └── BaseModal.vue
│   └── layout/            # 布局组件
│       ├── AppHeader.vue
│       ├── AppSidebar.vue
│       └── AppFooter.vue
├── composables/            # 组合式API/Hook函数
│   ├── useLoading.ts      # 加载状态管理
│   ├── useNotification.ts # 通知提示管理
│   ├── useAuth.ts         # 认证相关
│   ├── useApi.ts          # API调用封装
│   └── useEnvironment.ts  # 环境感知Hook
├── config/                 # 项目配置文件
│   ├── env.ts             # 环境变量配置
│   ├── api.ts             # API配置管理
│   ├── cors.ts            # CORS配置
│   ├── security.ts        # 安全配置
│   ├── constants.ts       # 常量定义
│   └── settings.ts        # 全局设置
├── layouts/                # 应用布局组件
│   ├── DefaultLayout.vue  # 默认布局
│   ├── AuthLayout.vue     # 认证页面布局
│   └── EmptyLayout.vue    # 空白布局
├── router/                 # 路由配置
│   ├── index.ts           # 主路由文件
│   ├── guards.ts          # 路由守卫
│   └── routes/            # 路由模块
│       ├── auth.ts        # 认证相关路由
│       ├── admin.ts       # 管理员路由
│       └── user.ts        # 用户路由
├── services/               # API调用和业务逻辑
│   ├── api/               # API接口定义
│   │   ├── auth.ts        # 认证API
│   │   ├── user.ts        # 用户API
│   │   └── common.ts      # 通用API
│   └── business/          # 业务逻辑服务
│       ├── userService.ts
│       └── authService.ts
├── stores/                 # Pinia状态管理
│   ├── index.ts           # Store入口文件
│   ├── auth.ts            # 认证状态
│   ├── user.ts            # 用户状态
│   └── app.ts             # 应用全局状态
├── types/                  # TypeScript类型声明
│   ├── index.d.ts         # 主类型声明文件
│   ├── auth.d.ts          # 认证类型声明
│   ├── user.d.ts          # 用户类型声明
│   ├── api.d.ts           # API类型声明
│   ├── env.d.ts           # 环境变量类型声明
│   └── common.d.ts        # 通用类型声明
├── utils/                  # 工具函数
│   ├── request.ts         # HTTP请求工具
│   ├── storage.ts         # 本地存储工具
│   ├── format.ts          # 格式化工具
│   ├── validate.ts        # 验证工具
│   └── helpers.ts         # 通用助手函数
├── views/                  # 页面组件
│   ├── auth/              # 认证相关页面
│   │   ├── Login.vue
│   │   ├── Register.vue
│   │   └── ForgotPassword.vue
│   ├── user/              # 用户相关页面
│   │   ├── Profile.vue
│   │   ├── Settings.vue
│   │   └── Dashboard.vue
│   ├── admin/             # 管理员页面
│   │   ├── UserManagement.vue
│   │   └── SystemSettings.vue
│   └── common/            # 通用页面
│       ├── Home.vue
│       ├── About.vue
│       └── NotFound.vue
├── App.vue                 # 根组件
└── main.ts                 # 入口文件

## 🏷️ 命名规范
### 组件命名
- 组件文件使用 PascalCase：`UserProfile.vue`
- 组件名必须是多单词，避免与HTML标签冲突
- 文件行数控制在200行以内，超出需拆分

### Props和事件
```vue
<script setup lang="ts">
// Props声明使用 camelCase
defineProps<{
  userName: string
  isActive: boolean
}>()

// Emit声明
defineEmits<{
  submit: [data: FormData]
  cancel: []
}>()
</script>

<template>
  <!-- 模板中使用 kebab-case -->
  <user-card 
    :user-name="userName" 
    :is-active="isActive"
    @submit="handleSubmit"
  />
</template>
```

### 变量和方法
- 变量/方法：camelCase + 动词前缀（`fetchUserData`、`handleSubmit`）
- 常量：UPPER_SNAKE_CASE（`MAX_RETRY_COUNT`）
- 私有方法：下划线前缀（`_validateForm`）

## 🔧 组件设计规范
### 基础要求
```vue
<script setup lang="ts">
/**
 * 用户信息卡片组件
 * @description 展示用户基本信息和操作按钮
 */

interface Props {
  userId: number
  showActions?: boolean
  size?: 'small' | 'medium' | 'large'
}

interface Emits {
  edit: [userId: number]
  delete: [userId: number]
}

// Props验证和默认值
const props = withDefaults(defineProps<Props>(), {
  showActions: true,
  size: 'medium'
})

const emit = defineEmits<Emits>()

// 使用环境感知Hook
const { isDevelopment, envLog } = useEnvironment()

// 使用组合式API
const { data: userInfo, loading } = useFetch(`/api/users/${props.userId}`)
const { loading: actionLoading, execute } = useAsyncAction()

// 计算属性
const cardClass = computed(() => [
  'user-card',
  `user-card--${props.size}`,
  { 'user-card--loading': loading.value }
])

// 方法
const handleEdit = () => {
  envLog(`编辑用户: ${props.userId}`)
  emit('edit', props.userId)
}
</script>

<template>
  <div :class="cardClass">
    <!-- 简洁的模板，复杂逻辑使用computed -->
    <div class="user-card__avatar">
      <img :src="userInfo?.avatar" :alt="userInfo?.name" />
    </div>
    <div class="user-card__content">
      <h3>{{ userInfo?.name }}</h3>
      <p>{{ userInfo?.email }}</p>
    </div>
    <div v-if="showActions" class="user-card__actions">
      <base-button @click="handleEdit">编辑</base-button>
    </div>
  </div>
</template>

<style scoped>
.user-card {
  @apply flex items-center p-4 bg-white rounded-lg shadow-sm;
}

.user-card--small {
  @apply p-2;
}

.user-card--large {
  @apply p-6;
}

.user-card__avatar img {
  @apply w-10 h-10 rounded-full;
}
</style>
```

## 🎨 样式规范
### CSS组织
```vue
<style scoped>
/* 使用CSS变量 */
:root {
  --primary-color: #3b82f6;
  --spacing-md: 1rem;
}

/* 结合TailwindCSS和自定义样式 */
.custom-component {
  @apply flex items-center; /* TailwindCSS */
  border-radius: var(--border-radius); /* CSS变量 */
}

/* 响应式设计 - 移动优先 */
.grid-layout {
  @apply grid grid-cols-1 gap-4;
}

@media (min-width: 768px) {
  .grid-layout {
    @apply grid-cols-2;
  }
}

@media (min-width: 1024px) {
  .grid-layout {
    @apply grid-cols-3;
  }
}
</style>
```

### 样式文件拆分
- 单个组件样式超过50行，提取到独立的CSS文件
- 全局样式放在 `assets/styles/` 目录
- 组件专用样式使用 `scoped`

## 🔄 组合式API规范
### 自定义Hook优先级
```typescript
// 1. 优先使用项目自定义composables
import { useLoading } from '@/composables/useLoading'
import { useNotification } from '@/composables/useNotification'
import { useEnvironment } from '@/composables/useEnvironment'

// 2. 使用Vue核心API
import { ref, computed, onMounted } from 'vue'

// 3. 创建新的composables
export function useUserManagement() {
  const users = ref<User[]>([])
  const loading = useLoading()
  const { envLog, isDevelopment } = useEnvironment()
  
  const fetchUsers = async () => {
    loading.start()
    try {
      users.value = await userService.getUsers()
      envLog('用户数据获取成功')
    } finally {
      loading.stop()
    }
  }
  
  return {
    users: readonly(users),
    loading: loading.state,
    fetchUsers
  }
}
```

## 📡 状态管理规范
### Pinia Store设计
```typescript
// stores/userStore.ts
export const useUserStore = defineStore('user', () => {
  // State
  const currentUser = ref<User | null>(null)
  const users = ref<User[]>([])
  
  // 环境感知
  const { envLog, isProduction } = useEnvironment()
  
  // Getters
  const isLoggedIn = computed(() => !!currentUser.value)
  const userCount = computed(() => users.value.length)
  
  // Actions
  const login = async (credentials: LoginCredentials) => {
    try {
      const user = await authService.login(credentials)
      currentUser.value = user
      
      envLog('用户登录成功')
      
      // 生产环境记录登录日志
      if (isProduction.value) {
        analyticsService.track('user_login', { userId: user.id })
      }
    } catch (error) {
      envLog('用户登录失败', 'error')
      throw new Error('登录失败')
    }
  }
  
  const logout = () => {
    currentUser.value = null
    envLog('用户已退出登录')
  }
  
  return {
    // State
    currentUser: readonly(currentUser),
    users: readonly(users),
    // Getters
    isLoggedIn,
    userCount,
    // Actions
    login,
    logout
  }
})
```

## 🚀 性能优化规范
### 路由懒加载
```typescript
// router/index.ts
const routes = [
  {
    path: '/users',
    component: () => import('@/views/UserManagement.vue'),
    meta: { requiresAuth: true }
  }
]
```

### 组件懒加载
```vue
<script setup lang="ts">
// 动态导入大型组件
const AdvancedEditor = defineAsyncComponent(() => 
  import('@/components/AdvancedEditor.vue')
)

// 条件加载
const showAdvancedFeatures = ref(false)
</script>

<template>
  <div>
    <button @click="showAdvancedFeatures = true">
      显示高级功能
    </button>
    
    <Suspense v-if="showAdvancedFeatures">
      <AdvancedEditor />
      <template #fallback>
        <div>加载中...</div>
      </template>
    </Suspense>
  </div>
</template>
```

### 列表优化
```vue
<template>
  <!-- 必须添加key -->
  <div v-for="item in items" :key="item.id">
    {{ item.name }}
  </div>
  
  <!-- 大列表使用虚拟滚动 -->
  <virtual-list :items="largeList" item-height="50">
    <template #item="{ item }">
      <user-card :user="item" />
    </template>
  </virtual-list>
</template>
```

## 🛡️ 类型安全规范
### TypeScript集成
```typescript
// types/env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_APP_ENV: 'development' | 'production'
  readonly VITE_APP_TITLE: string
  readonly VITE_API_BASE_URL: string
  readonly VITE_API_TIMEOUT: string
  readonly VITE_ENABLE_MOCK: string
  readonly VITE_ENABLE_DEVTOOLS: string
  readonly VITE_ALLOWED_ORIGINS: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

// types/user.d.ts
export interface User {
  id: number
  name: string
  email: string
  avatar?: string
  createdAt: Date
}

export interface CreateUserPayload {
  name: string
  email: string
}

// 组件props类型
export interface UserCardProps {
  user: User
  showActions?: boolean
  onEdit?: (user: User) => void
}

// API响应类型
export interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
}
```

## 🧪 测试规范
### 组件测试
```typescript
// tests/components/UserCard.test.ts
import { mount } from '@vue/test-utils'
import UserCard from '@/components/UserCard.vue'

describe('UserCard', () => {
  const mockUser = {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com'
  }
  
  it('应该正确显示用户信息', () => {
    const wrapper = mount(UserCard, {
      props: { user: mockUser }
    })
    
    expect(wrapper.text()).toContain('John Doe')
    expect(wrapper.text()).toContain('john@example.com')
  })
  
  it('应该触发编辑事件', async () => {
    const wrapper = mount(UserCard, {
      props: { user: mockUser, showActions: true }
    })
    
    await wrapper.find('[data-testid="edit-button"]').trigger('click')
    expect(wrapper.emitted('edit')).toBeTruthy()
  })
})
```

## 📝 代码质量规范
### ESLint配置
```json
{
  "extends": [
    "@vue/typescript/recommended",
    "@vue/prettier"
  ],
  "rules": {
    "semi": ["error", "never"],
    "comma-dangle": ["error", "never"],
    "vue/component-name-in-template-casing": ["error", "kebab-case"],
    "vue/prop-name-casing": ["error", "camelCase"],
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

### 注释规范
```vue
<script setup lang="ts">
/**
 * 用户管理页面组件
 * @description 提供用户列表展示、搜索、编辑、删除功能
 * @author 开发者姓名
 * @since 2024-01-01
 */

// 复杂业务逻辑需要注释
const validateUserForm = (formData: CreateUserPayload) => {
  // 验证邮箱格式是否正确
  if (!isValidEmail(formData.email)) {
    throw new Error('邮箱格式不正确')
  }
  
  // 验证用户名长度（特殊业务要求：2-20字符）
  if (formData.name.length < 2 || formData.name.length > 20) {
    throw new Error('用户名长度必须在2-20字符之间')
  }
}
</script>
```

## 🔄 开发流程规范
### Git提交规范
```bash
# 遵循 Conventional Commits
feat: 新增用户管理功能
fix: 修复登录页面跳转问题
docs: 更新API文档
style: 调整按钮样式
refactor: 重构用户服务代码
test: 添加用户组件测试
chore: 更新依赖版本
perf: 优化环境配置加载性能
```

### 代码审查要点
- [ ] 组件是否超过200行
- [ ] 是否使用了TypeScript类型声明
- [ ] Props是否添加了验证
- [ ] 是否使用了scoped样式
- [ ] 是否添加了必要的注释
- [ ] 是否遵循命名规范
- [ ] 列表渲染是否添加了key
- [ ] 是否处理了错误状态
- [ ] 是否添加了loading状态
- [ ] 是否优化了性能（懒加载等）
- [ ] 是否正确配置了环境变量
- [ ] 是否处理了跨域问题
- [ ] 是否使用了环境感知的逻辑
- [ ] 是否配置了安全域名白名单

## 🎯 优先级规则
1. **组件使用优先级**：项目自定义组件 > ArcoDesign > 新建组件
2. **Composables优先级**：项目自定义Hook > Vue核心API > 新建Hook
3. **工具函数优先级**：项目utils > 第三方库 > 新建工具
4. **状态管理优先级**：组件内状态(ref/reactive) > Pinia Store > provide/inject5. **环境配置优先级**：环境变量 > 配置文件 > 硬编码值
6. **安全策略优先级**：域名白名单验证 > CORS配置 > 请求拦截
