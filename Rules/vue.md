# Vue.js 高效开发指南

## 🎯 推荐技术栈
- **核心**: Vue 3 + Composition API + TypeScript
- **状态**: Pinia (小项目可用 ref/reactive)
- **样式**: TailwindCSS 或 原生CSS (根据项目规模选择)
- **构建**: Vite

## 📁 简洁项目结构
```
src/
├── components/     # 组件（按功能分组）
├── composables/    # 复用逻辑
├── views/         # 页面
├── router/        # 路由
├── stores/        # 状态管理
└── utils/         # 工具函数
```

## 🔧 核心开发原则

### 1. 组件设计原则
**保持简单、职责单一**

```vue
<script setup lang="ts">
// Props 定义
interface Props {
  title: string
  count?: number
}
const props = withDefaults(defineProps<Props>(), {
  count: 0
})

// 业务逻辑
const handleClick = () => {
  // 实现逻辑
}
</script>

<template>
  <div class="component">
    <h2>{{ props.title }}</h2>
    <span>{{ props.count }}</span>
    <button @click="handleClick">操作</button>
  </div>
</template>

<style scoped>
.component {
  /* 样式保持简洁 */
}
</style>
```

### 2. 环境配置 (简化版)
```typescript
// config/env.ts
export const config = {
  isDev: import.meta.env.DEV,
  apiBase: import.meta.env.VITE_API_BASE || 'http://localhost:3000'
}
```

```bash
# .env.development
VITE_API_BASE=http://localhost:3000

# .env.production  
VITE_API_BASE=https://api.yourdomain.com
```

### 3. 数据请求模式
```typescript
// composables/useApi.ts
export function useApi<T>(url: string) {
  const data = ref<T | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  const fetch = async () => {
    loading.value = true
    try {
      const response = await $fetch<T>(url)
      data.value = response
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }
  
  return { data, loading, error, fetch }
}
```

## 🚀 性能要点
- 大组件使用 `defineAsyncComponent` 懒加载
- 长列表添加 `:key`，超过100项考虑虚拟滚动
- 图片使用懒加载

## ✅ 开发检查清单 (3项核心)
开发完成后检查：
- [ ] **错误处理**: 是否处理了 loading/error 状态
- [ ] **类型安全**: 关键数据是否定义了类型
- [ ] **性能优化**: 列表是否有key，大组件是否懒加载

## 📚 常用代码片段

### 表单处理
```vue
<script setup lang="ts">
const form = reactive({
  name: '',
  email: ''
})

const errors = ref<Record<string, string>>({})

const validateForm = () => {
  errors.value = {}
  if (!form.name) errors.value.name = '姓名不能为空'
  if (!form.email) errors.value.email = '邮箱不能为空'
  return Object.keys(errors.value).length === 0
}

const handleSubmit = async () => {
  if (!validateForm()) return
  
  try {
    await submitForm(form)
    // 成功处理
  } catch (error) {
    // 错误处理
  }
}
</script>
```

### 列表渲染
```vue
<template>
  <div v-if="loading">加载中...</div>
  <div v-else-if="error">错误: {{ error }}</div>
  <div v-else>
    <div v-for="item in items" :key="item.id">
      {{ item.name }}
    </div>
  </div>
</template>
```

## 🎨 样式建议
- 优先使用 TailwindCSS 类名
- 自定义样式写在 `<style scoped>` 中
- 组件样式超过20行考虑提取到独立文件

---
**记住**: 规则是为了提高效率，不是为了限制创造力。根据项目实际情况灵活调整。 