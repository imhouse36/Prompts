---
description: Vue.js best practices and patterns for modern web applications
globs: **/*.vue, **/*.ts, components/**/*
---

# Vue.js 核心开发规范

## 🎯 核心技术栈
- Vue 3.0 + Composition API + TypeScript
- Pinia (状态管理) + Vue Router (路由)
- ArcoDesign (UI组件) + TailwindCSS (样式)
- Vite (构建工具) + Yarn (包管理)

## 🌍 环境配置要求
### 双环境支持原则
- **自动环境检测**：开发/生产环境自动识别和切换
- **CORS跨域支持**：完整的跨域配置和域名白名单
- **配置统一管理**：环境变量集中管理和验证
- **安全机制**：生产环境安全策略自动启用

### 核心环境配置
```typescript
// config/env.ts - 环境自动检测
export const getCurrentEnvironment = () => {
  if (import.meta.env.NODE_ENV === 'production') return 'production'
  if (import.meta.env.PROD) return 'production'
  const hostname = window.location?.hostname
  if (hostname && !['localhost', '127.0.0.1'].includes(hostname)) {
    return 'production'
  }
  return 'development'
}

// 环境配置对象
export const appConfig = {
  env: getCurrentEnvironment(),
  api: {
    baseURL: import.meta.env.VITE_API_BASE_URL || 
      (getCurrentEnvironment() === 'production' 
        ? 'https://api.yourdomain.com' 
        : 'http://localhost:3000/api'),
    timeout: getCurrentEnvironment() === 'production' ? 15000 : 10000
  },
  cors: {
    allowedOrigins: (import.meta.env.VITE_ALLOWED_ORIGINS || '').split(',')
  }
}
```

### 环境变量文件
```bash
# .env.development
VITE_APP_ENV=development
VITE_API_BASE_URL=http://localhost:3000/api
VITE_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# .env.production  
VITE_APP_ENV=production
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_ALLOWED_ORIGINS=https://yourdomain.com
```

## 📁 项目结构（简化）
```
Vue/
├── src/
│    ├── components/          # 组件 (PascalCase命名)
│    │   ├── base/           # 基础组件
│    │   └── business/       # 业务组件
│    ├── composables/        # 组合式API (useXxx命名)
│    ├── config/            # 配置文件 (env.ts, api.ts)
│    ├── router/            # 路由配置
│    ├── stores/            # Pinia状态管理
│    ├── utils/             # 工具函数
│    ├── views/             # 页面组件
│    └── types/             # TypeScript类型
```

## 🔧 核心编码规范
### 组件设计
```vue
<script setup lang="ts">
/**
 * 组件功能描述
 * @description 详细说明组件用途
 */

// Props类型定义
interface Props {
  userId: number
  showActions?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showActions: true
})

// 组合式API使用
const { data, loading, error } = useFetch(`/api/users/${props.userId}`)
const { isDevelopment } = useEnvironment()

// 方法定义（动词+名词）
const handleEdit = () => {
  // 实现逻辑
}
</script>

<template>
  <div class="user-card">
    <!-- 简洁的模板结构 -->
    <div v-if="loading">加载中...</div>
    <div v-else-if="error">错误: {{ error }}</div>
    <div v-else>
      <h3>{{ data?.name }}</h3>
      <button v-if="showActions" @click="handleEdit">编辑</button>
    </div>
  </div>
</template>

<style scoped>
.user-card {
  @apply p-4 bg-white rounded-lg shadow-sm;
}
</style>
```

### 命名规范
- **组件文件**：PascalCase (`UserProfile.vue`)
- **变量/方法**：camelCase + 动词前缀 (`handleSubmit`, `fetchData`)
- **常量**：UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)
- **CSS类名**：kebab-case (`user-card`, `btn-primary`)

### Composables模式
```typescript
// composables/useEnvironment.ts
export function useEnvironment() {
  const currentEnv = computed(() => appConfig.env)
  const isDevelopment = computed(() => appConfig.env === 'development')
  const isProduction = computed(() => appConfig.env === 'production')
  
  const envLog = (message: string) => {
    if (isDevelopment.value) {
      console.log(`[${appConfig.env}] ${message}`)
    }
  }
  
  return { currentEnv, isDevelopment, isProduction, envLog }
}
```

## 🎨 样式规范
```vue
<style scoped>
/* 1. 使用TailwindCSS类名优先 */
.component {
  @apply flex items-center p-4;
}

/* 2. 自定义样式使用CSS变量 */
.custom-style {
  color: var(--color-primary);
  padding: var(--spacing-md);
}

/* 3. 响应式设计 - 移动优先 */
.grid {
  @apply grid grid-cols-1 gap-4;
}

@media (min-width: 768px) {
  .grid {
    @apply grid-cols-2;
  }
}
</style>
```

## 🚀 性能要求
- **组件懒加载**：大型组件使用 `defineAsyncComponent`
- **路由懒加载**：所有路由组件使用动态导入
- **列表优化**：长列表必须添加 `:key`，超过100项使用虚拟滚动
- **文件大小控制**：单文件不超过200行，超出需拆分

## 🛡️ 类型安全
```typescript
// types/env.d.ts
interface ImportMetaEnv {
  readonly VITE_APP_ENV: 'development' | 'production'
  readonly VITE_API_BASE_URL: string
  readonly VITE_ALLOWED_ORIGINS: string
}

// types/api.d.ts
interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
}
```

## ✅ 代码检查要点
开发时必须检查：
- [ ] 是否使用TypeScript类型声明
- [ ] 组件是否超过200行（需拆分）
- [ ] 列表渲染是否添加key
- [ ] 是否处理loading和error状态
- [ ] 是否使用环境感知逻辑
- [ ] 样式是否超过50行（需独立文件）
- [ ] 是否添加必要的函数注释
- [ ] Props是否添加类型验证

## 📚 详细文档引用
- 环境配置详细说明：`docs/vue/environment-advanced.md`
- 组件设计模式：`docs/vue/component-patterns.md`
- 性能优化指南：`docs/vue/performance-guide.md`
- 测试最佳实践：`docs/vue/testing-guide.md`

