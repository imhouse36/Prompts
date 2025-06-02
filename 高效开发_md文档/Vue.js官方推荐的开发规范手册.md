📁 一、项目结构规范 125
bash
src
├── assets              # 静态资源（图片、字体等）
├── components          # 公共组件
│   ├── base            # 基础组件（如Button、Input）
│   └── layout          # 布局组件（如Header、Footer）
├── composables         # 组合式函数（Vue 3推荐）
├── router              # 路由配置
├── store               # 状态管理（Pinia/Vuex）
├── views               # 页面级组件
├── utils               # 工具函数
├── styles              # 全局样式
└── App.vue             # 根组件
main.js                 # 入口文件
🏷️ 二、命名规范 147
组件名：

使用 PascalCase（如 UserProfile.vue）

多单词命名，避免与HTML标签冲突（如 ArticleList 而非 List）

Prop 属性：

声明用 camelCase，模板使用 kebab-case：

vue
<script setup>
defineProps({ userName: String })  // camelCase
</script>
<template>
  <user-card user-name="Alice" />  <!-- kebab-case -->
</template>
方法/变量：

方法名使用 camelCase + 动词前缀（如 fetchData、handleSubmit）

常量使用 UPPER_SNAKE_CASE（如 MAX_ITEMS = 10）

⚙️ 三、组件设计规范 38
单一职责原则：

每个组件只解决一个问题（如 SearchBar.vue 仅处理搜索逻辑）。

文件行数建议 ≤ 200 行，复杂组件拆分子组件。

Props 原子化：

使用原始类型（String/Number/Boolean），避免复杂对象38：

javascript
// Good
props: { userId: Number, isActive: Boolean }

// Bad
props: { user: Object }
Props 验证：

必须指定类型、默认值和校验规则：

javascript
props: {
  size: {
    type: String,
    default: 'medium',
    validator: (v) => ['small', 'medium', 'large'].includes(v)
  }
}
🖥️ 四、模板与样式规范
模板简洁化 38：

避免复杂表达式，用 computed 或 methods 替代：

vue
<!-- Bad -->
{{ user.firstName + ' ' + user.lastName }}

<!-- Good -->
{{ fullName }}  <!-- computed: { fullName() { ... } } -->
样式作用域：

组件样式添加 scoped，防止污染全局15：

vue
<style scoped>
.card { margin: 16px; }  /* 仅作用于当前组件 */
</style>
🔧 五、Vue 特性使用规范
组合式 API（Composition API）：

逻辑复用使用 composables（如 useFetch.js）：

javascript
// useFetch.js
export function useFetch(url) {
  const data = ref(null);
  onMounted(async () => { data.value = await fetch(url); });
  return { data };
}
状态管理：

全局状态用 Pinia（Vue 3推荐），模块化设计 store45。

🧩 六、代码风格与质量 57
ESLint 规则：

强制使用分号、尾逗号、箭头函数括号。

配置规则：

json
{
  "semi": ["error", "always"],
  "comma-dangle": ["error", "always-multiline"]
}
注释规范：

公共组件需写使用说明：

vue
/**
 * @desc 用户卡片组件
 * @prop {String} userName - 用户姓名
 * @example <user-card user-name="Alice" />
 */
🔒 七、安全性与性能
XSS 防御：

避免 v-html 渲染用户输入，必须使用时过滤（如 DOMPurify）。

性能优化：

路由懒加载：

javascript
const UserView = () => import('@/views/UserView.vue');
列表渲染添加 key：

vue
<li v-for="item in items" :key="item.id">{{ item.name }}</li>
✅ 八、提交与协作规范
Git 提交：

遵循 Conventional Commits：

bash
feat: 添加用户登录功能
fix(router): 修复页面跳转404问题
代码审查：

重点检查：

Props 是否原子化

组件是否超过200行

是否遗漏 scoped 样式