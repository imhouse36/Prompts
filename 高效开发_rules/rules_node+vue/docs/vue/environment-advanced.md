# Vue.js 环境配置详细指南

## 🌍 完整环境配置示例

### 高级环境检测机制
```typescript
// config/env.ts - 高级环境检测
interface EnvironmentConfig {
  name: 'development' | 'staging' | 'production'
  api: ApiConfig
  features: FeatureFlags
  security: SecurityConfig
  logging: LoggingConfig
}

class AdvancedEnvironmentManager {
  private static instance: AdvancedEnvironmentManager
  private config: EnvironmentConfig

  constructor() {
    this.config = this.initializeConfig()
  }

  /**
   * 多级环境检测
   * 支持 development, staging, production 三种环境
   */
  private detectEnvironment(): EnvironmentConfig['name'] {
    // 1. 优先检查环境变量
    const nodeEnv = import.meta.env.NODE_ENV
    const viteEnv = import.meta.env.VITE_APP_ENV
    
    if (viteEnv && ['development', 'staging', 'production'].includes(viteEnv)) {
      return viteEnv as EnvironmentConfig['name']
    }

    // 2. 根据构建标志检测
    if (import.meta.env.PROD) {
      return 'production'
    }

    // 3. 根据域名检测
    if (typeof window !== 'undefined') {
      const hostname = window.location.hostname
      
      // 生产域名检测
      const productionDomains = [
        'yourdomain.com',
        'www.yourdomain.com',
        'app.yourdomain.com'
      ]
      
      // 测试环境域名检测
      const stagingDomains = [
        'staging.yourdomain.com',
        'test.yourdomain.com',
        'dev.yourdomain.com'
      ]
      
      if (productionDomains.some(domain => hostname.includes(domain))) {
        return 'production'
      }
      
      if (stagingDomains.some(domain => hostname.includes(domain))) {
        return 'staging'
      }
    }

    // 4. 根据端口检测
    if (typeof window !== 'undefined') {
      const port = window.location.port
      if (port === '80' || port === '443' || !port) {
        return 'production'
      }
      if (port === '8080' || port === '3000') {
        return 'staging'
      }
    }

    return 'development'
  }

  /**
   * 初始化完整配置
   */
  private initializeConfig(): EnvironmentConfig {
    const env = this.detectEnvironment()
    
    const configs = {
      development: this.getDevelopmentConfig(),
      staging: this.getStagingConfig(),
      production: this.getProductionConfig()
    }

    return {
      name: env,
      ...configs[env]
    }
  }

  /**
   * 开发环境配置
   */
  private getDevelopmentConfig() {
    return {
      api: {
        baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api',
        timeout: 30000,
        retryAttempts: 3,
        retryDelay: 1000
      },
      features: {
        enableMock: true,
        enableDevtools: true,
        enableHotReload: true,
        enableDebugMode: true,
        enablePerformanceMonitor: false
      },
      security: {
        allowedOrigins: [
          'http://localhost:3000',
          'http://localhost:5173',
          'http://localhost:8080',
          'http://127.0.0.1:3000',
          'http://127.0.0.1:5173'
        ],
        enableCSRF: false,
        enableRateLimit: false,
        cookieSecure: false
      },
      logging: {
        level: 'debug',
        enableConsole: true,
        enableNetwork: true,
        enablePerformance: true
      }
    }
  }

  /**
   * 测试环境配置
   */
  private getStagingConfig() {
    return {
      api: {
        baseURL: import.meta.env.VITE_API_BASE_URL || 'https://staging-api.yourdomain.com',
        timeout: 20000,
        retryAttempts: 2,
        retryDelay: 1500
      },
      features: {
        enableMock: false,
        enableDevtools: true,
        enableHotReload: false,
        enableDebugMode: true,
        enablePerformanceMonitor: true
      },
      security: {
        allowedOrigins: [
          'https://staging.yourdomain.com',
          'https://test.yourdomain.com'
        ],
        enableCSRF: true,
        enableRateLimit: true,
        cookieSecure: true
      },
      logging: {
        level: 'info',
        enableConsole: true,
        enableNetwork: false,
        enablePerformance: true
      }
    }
  }

  /**
   * 生产环境配置
   */
  private getProductionConfig() {
    return {
      api: {
        baseURL: import.meta.env.VITE_API_BASE_URL || 'https://api.yourdomain.com',
        timeout: 15000,
        retryAttempts: 1,
        retryDelay: 2000
      },
      features: {
        enableMock: false,
        enableDevtools: false,
        enableHotReload: false,
        enableDebugMode: false,
        enablePerformanceMonitor: true
      },
      security: {
        allowedOrigins: [
          'https://yourdomain.com',
          'https://www.yourdomain.com',
          'https://app.yourdomain.com'
        ],
        enableCSRF: true,
        enableRateLimit: true,
        cookieSecure: true
      },
      logging: {
        level: 'error',
        enableConsole: false,
        enableNetwork: false,
        enablePerformance: false
      }
    }
  }

  public getConfig(): EnvironmentConfig {
    return this.config
  }

  public static getInstance(): AdvancedEnvironmentManager {
    if (!AdvancedEnvironmentManager.instance) {
      AdvancedEnvironmentManager.instance = new AdvancedEnvironmentManager()
    }
    return AdvancedEnvironmentManager.instance
  }
}

// 导出配置实例
export const envManager = AdvancedEnvironmentManager.getInstance()
export const appConfig = envManager.getConfig()
```

### HTTP请求配置完整示例
```typescript
// utils/request.ts - 完整HTTP客户端
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { appConfig } from '@/config/env'

class HttpClient {
  private instance: AxiosInstance
  private requestQueue: Set<string> = new Set()

  constructor() {
    this.instance = this.createInstance()
    this.setupInterceptors()
  }

  /**
   * 创建axios实例
   */
  private createInstance(): AxiosInstance {
    const config = appConfig.api
    
    return axios.create({
      baseURL: config.baseURL,
      timeout: config.timeout,
      withCredentials: appConfig.security.cookieSecure,
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        ...(appConfig.name !== 'production' && { 'X-Debug-Mode': 'true' })
      }
    })
  }

  /**
   * 设置请求拦截器
   */
  private setupInterceptors() {
    // 请求拦截器
    this.instance.interceptors.request.use(
      (config) => {
        // 添加请求ID用于去重
        const requestId = this.generateRequestId(config)
        
        if (this.requestQueue.has(requestId)) {
          return Promise.reject(new Error('Duplicate request cancelled'))
        }
        
        this.requestQueue.add(requestId)
        config.metadata = { requestId }

        // 添加认证token
        const token = this.getAuthToken()
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }

        // 开发环境日志
        if (appConfig.logging.enableNetwork) {
          console.log('🚀 API Request:', {
            method: config.method?.toUpperCase(),
            url: config.url,
            params: config.params,
            data: config.data
          })
        }

        return config
      },
      (error) => {
        if (appConfig.logging.enableConsole) {
          console.error('❌ Request Error:', error)
        }
        return Promise.reject(error)
      }
    )

    // 响应拦截器
    this.instance.interceptors.response.use(
      (response: AxiosResponse) => {
        // 移除请求队列中的请求ID
        const requestId = response.config.metadata?.requestId
        if (requestId) {
          this.requestQueue.delete(requestId)
        }

        if (appConfig.logging.enableNetwork) {
          console.log('✅ API Response:', {
            status: response.status,
            url: response.config.url,
            data: response.data
          })
        }

        return response
      },
      (error) => {
        // 移除请求队列中的请求ID
        const requestId = error.config?.metadata?.requestId
        if (requestId) {
          this.requestQueue.delete(requestId)
        }

        return this.handleResponseError(error)
      }
    )
  }

  /**
   * 处理响应错误
   */
  private async handleResponseError(error: any) {
    const config = error.config
    const status = error.response?.status

    // 开发环境错误日志
    if (appConfig.logging.enableConsole) {
      console.error('❌ API Error:', {
        status,
        url: config?.url,
        method: config?.method,
        message: error.message,
        response: error.response?.data
      })
    }

    // 处理特定错误状态
    switch (status) {
      case 401:
        this.handleAuthError()
        break
      case 403:
        this.handleForbiddenError()
        break
      case 429:
        // 处理频率限制错误，实现指数退避重试
        if (config && config.retryCount < appConfig.api.retryAttempts) {
          return this.retryRequest(config)
        }
        break
      case 500:
      case 502:
      case 503:
      case 504:
        // 服务器错误重试
        if (config && config.retryCount < appConfig.api.retryAttempts) {
          return this.retryRequest(config)
        }
        break
    }

    return Promise.reject(error)
  }

  /**
   * 重试请求
   */
  private async retryRequest(config: any) {
    config.retryCount = (config.retryCount || 0) + 1
    
    const delay = appConfig.api.retryDelay * Math.pow(2, config.retryCount - 1)
    
    await new Promise(resolve => setTimeout(resolve, delay))
    
    return this.instance(config)
  }

  /**
   * 生成请求ID
   */
  private generateRequestId(config: AxiosRequestConfig): string {
    const { method, url, params, data } = config
    return `${method}_${url}_${JSON.stringify(params)}_${JSON.stringify(data)}`
  }

  /**
   * 获取认证token
   */
  private getAuthToken(): string | null {
    return localStorage.getItem('auth_token') || sessionStorage.getItem('auth_token')
  }

  /**
   * 处理认证错误
   */
  private handleAuthError() {
    // 清除token
    localStorage.removeItem('auth_token')
    sessionStorage.removeItem('auth_token')
    
    // 跳转到登录页
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  }

  /**
   * 处理权限错误
   */
  private handleForbiddenError() {
    // 显示权限不足提示
    console.warn('Access forbidden: Insufficient permissions')
  }

  // 公共方法
  get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.get(url, config).then(response => response.data)
  }

  post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.post(url, data, config).then(response => response.data)
  }

  put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.put(url, data, config).then(response => response.data)
  }

  delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    return this.instance.delete(url, config).then(response => response.data)
  }
}

export const httpClient = new HttpClient()
export const request = httpClient
```

### Vite配置完整示例
```typescript
// vite.config.ts - 完整Vite配置
import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig(({ command, mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd(), '')
  
  const isProduction = mode === 'production'
  const isStaging = mode === 'staging'
  const isDevelopment = mode === 'development'

  return {
    plugins: [
      vue(),
      // 其他插件根据环境条件加载
      ...(!isProduction ? [
        // 开发环境插件
      ] : [])
    ],

    resolve: {
      alias: {
        '@': resolve(__dirname, 'src'),
        '@components': resolve(__dirname, 'src/components'),
        '@utils': resolve(__dirname, 'src/utils'),
        '@config': resolve(__dirname, 'src/config'),
        '@assets': resolve(__dirname, 'src/assets'),
        '@stores': resolve(__dirname, 'src/stores'),
        '@views': resolve(__dirname, 'src/views')
      }
    },

    // 开发服务器配置
    server: {
      host: '0.0.0.0',
      port: parseInt(env.VITE_DEV_PORT) || 5173,
      cors: true,
      proxy: {
        '/api': {
          target: env.VITE_API_BASE_URL || 'http://localhost:3000',
          changeOrigin: true,
          secure: isProduction,
          rewrite: (path) => path.replace(/^\/api/, ''),
          configure: (proxy, _options) => {
            proxy.on('error', (err, _req, _res) => {
              console.log('proxy error', err)
            })
            proxy.on('proxyReq', (proxyReq, req, _res) => {
              console.log('Sending Request to the Target:', req.method, req.url)
            })
            proxy.on('proxyRes', (proxyRes, req, _res) => {
              console.log('Received Response from the Target:', proxyRes.statusCode, req.url)
            })
          }
        }
      }
    },

    // 构建配置
    build: {
      target: 'es2015',
      outDir: 'dist',
      assetsDir: 'assets',
      sourcemap: !isProduction,
      minify: isProduction ? 'esbuild' : false,
      
      rollupOptions: {
        output: {
          // 分包策略
          manualChunks: {
            vendor: ['vue', 'vue-router', 'pinia'],
            ui: ['@arco-design/web-vue'],
            utils: ['axios', 'lodash-es']
          },
          
          // 文件命名
          chunkFileNames: isProduction 
            ? 'assets/js/[name]-[hash].js'
            : 'assets/js/[name].js',
          entryFileNames: isProduction
            ? 'assets/js/[name]-[hash].js'
            : 'assets/js/[name].js',
          assetFileNames: isProduction
            ? 'assets/[ext]/[name]-[hash].[ext]'
            : 'assets/[ext]/[name].[ext]'
        }
      },

      // 构建优化
      terserOptions: isProduction ? {
        compress: {
          drop_console: true,
          drop_debugger: true
        }
      } : {}
    },

    // 环境变量前缀
    envPrefix: 'VITE_',

    // 定义全局变量
    define: {
      __APP_ENV__: JSON.stringify(mode),
      __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
      __VERSION__: JSON.stringify(process.env.npm_package_version),
      __IS_DEVELOPMENT__: isDevelopment,
      __IS_STAGING__: isStaging,
      __IS_PRODUCTION__: isProduction
    },

    // CSS配置
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `
            @import "@/assets/styles/variables.scss";
            @import "@/assets/styles/mixins.scss";
          `
        }
      },
      postcss: {
        plugins: [
          require('tailwindcss'),
          require('autoprefixer')
        ]
      }
    },

    // 优化依赖
    optimizeDeps: {
      include: ['vue', 'vue-router', 'pinia', '@arco-design/web-vue'],
      exclude: isDevelopment ? [] : ['some-dev-only-package']
    }
  }
})
```

### 环境变量完整配置
```bash
# .env - 基础环境变量（所有环境共享）
VITE_APP_NAME=项目名称
VITE_APP_VERSION=1.0.0
VITE_APP_DESCRIPTION=项目描述

# .env.development - 开发环境
NODE_ENV=development
VITE_APP_ENV=development
VITE_APP_TITLE=项目名称 - 开发环境
VITE_DEV_PORT=5173

# API配置
VITE_API_BASE_URL=http://localhost:3000/api
VITE_API_TIMEOUT=30000
VITE_API_RETRY_ATTEMPTS=3
VITE_API_RETRY_DELAY=1000

# 跨域配置
VITE_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000

# 功能开关
VITE_ENABLE_MOCK=true
VITE_ENABLE_DEVTOOLS=true
VITE_ENABLE_HOT_RELOAD=true
VITE_ENABLE_DEBUG_MODE=true

# 安全配置
VITE_ENABLE_CSRF=false
VITE_ENABLE_RATE_LIMIT=false
VITE_COOKIE_SECURE=false

# 日志配置
VITE_LOG_LEVEL=debug
VITE_ENABLE_CONSOLE_LOG=true
VITE_ENABLE_NETWORK_LOG=true

# .env.staging - 测试环境
NODE_ENV=production
VITE_APP_ENV=staging
VITE_APP_TITLE=项目名称 - 测试环境

# API配置
VITE_API_BASE_URL=https://staging-api.yourdomain.com
VITE_API_TIMEOUT=20000
VITE_API_RETRY_ATTEMPTS=2
VITE_API_RETRY_DELAY=1500

# 跨域配置
VITE_ALLOWED_ORIGINS=https://staging.yourdomain.com,https://test.yourdomain.com

# 功能开关
VITE_ENABLE_MOCK=false
VITE_ENABLE_DEVTOOLS=true
VITE_ENABLE_DEBUG_MODE=true

# 安全配置
VITE_ENABLE_CSRF=true
VITE_ENABLE_RATE_LIMIT=true
VITE_COOKIE_SECURE=true

# 日志配置
VITE_LOG_LEVEL=info
VITE_ENABLE_CONSOLE_LOG=true
VITE_ENABLE_NETWORK_LOG=false

# .env.production - 生产环境
NODE_ENV=production
VITE_APP_ENV=production
VITE_APP_TITLE=项目名称

# API配置
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_API_TIMEOUT=15000
VITE_API_RETRY_ATTEMPTS=1
VITE_API_RETRY_DELAY=2000

# 跨域配置
VITE_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# 功能开关
VITE_ENABLE_MOCK=false
VITE_ENABLE_DEVTOOLS=false
VITE_ENABLE_DEBUG_MODE=false

# 安全配置
VITE_ENABLE_CSRF=true
VITE_ENABLE_RATE_LIMIT=true
VITE_COOKIE_SECURE=true

# 日志配置
VITE_LOG_LEVEL=error
VITE_ENABLE_CONSOLE_LOG=false
VITE_ENABLE_NETWORK_LOG=false

# 第三方服务配置（所有环境都需要配置对应的值）
VITE_GOOGLE_ANALYTICS_ID=
VITE_SENTRY_DSN=
VITE_CDN_BASE_URL=
```

### package.json 脚本配置
```json
{
  "scripts": {
    "dev": "vite --mode development",
    "dev:staging": "vite --mode staging",
    "build": "vue-tsc --noEmit && vite build --mode production",
    "build:staging": "vue-tsc --noEmit && vite build --mode staging",
    "build:dev": "vue-tsc --noEmit && vite build --mode development",
    "preview": "vite preview",
    "preview:staging": "vite preview --mode staging",
    "type-check": "vue-tsc --noEmit",
    "lint": "eslint . --ext .vue,.js,.jsx,.cjs,.mjs,.ts,.tsx,.cts,.mts --fix",
    "test": "vitest run",
    "test:dev": "vitest",
    "test:coverage": "vitest run --coverage",
    "analyze": "vite-bundle-analyzer"
  }
}
```

这个详细配置文档提供了完整的Vue.js环境配置方案，支持开发、测试、生产三种环境的自动检测和切换，包含了HTTP客户端、构建配置、环境变量等各个方面的详细实现。 