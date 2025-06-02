# JavaScript Frameworks
- 使用Vue 3.0作为基础核心框架。
- 使用Pinia进行跨页面数据状态管理。
- 使用Vue Router进行页面路由切换。

# UI Framework and Styling
- 使用ArcoDesign作为UI框架，简化组件开发。
- 使用TailwindCss作为CSS框架，以便简化CSS编写。

# Compilation and Build Tools
- 使用Yarn作为依赖包管理工具。
- 使用Vite作为Vue的构建工具。

# Other Tools
- 使用Fetch接口来实现前端请求。
- 使用Vue Flow库快捷构建流程图。
- 使用Vue Markdown将大模型输出的Markdown转为HTML。
- 使用ECharts将数据转换为统计图表。

# Directory Structure
- 根目录 `/vue-demo` 包含项目的基本结构。
- `/node_modules`: 项目依赖模块。
- `/public`: 包括公共文件，如 `favicon.ico` 和入口 HTML 文件 `index.html`。

## Source Directory (/src)
- `/assets`: 存放静态资源。
- `/assets/images`: 图片资源目录。
- `/assets/styles`: 全局样式配置，包括 `tailwind.css`。
- `/components`: 共享组件的存放目录（优先使用自己定义的组件）。
- `/composables`: 自定义 Hook 函数或组合式 API 的实现（优先使用自己定义的函数或者组合式API）。
- `/config`: 项目配置文件，如环境变量和全局设置。
- `/layouts`: 应用布局组件（如 `DefaultLayout.vue`）。
- `/router`: 路由配置文件目录（如 `index.ts`）。
- `/services`: 项目服务，例如API调用和业务逻辑实现。
- `/stores`: Pinia 状态管理设置目录（如 `index.ts`）。
- `/types`: 类型声明目录，用于声明全局自定义类型及 Vue 的类型补充（如 `custom-types.d.ts`）。
- `/types/auth.d.ts`: 认证类型声明。
- `/types/request.d.ts`: 公共请求类型声明。
- `/types/response.d.ts`: 公共响应类型声明(如 `BaseResponse` 类型)。
- `/utils`: 工具类目录。
- `/utils/request.ts`: 公共请求工具类。
- `/views`: 页面文件夹，包括认证页面、其他页面及主页面（如 `HomeView.vue`）。
- `App.vue`: 根组件。
- `main.ts`: 项目入口文件。

## Configuration Files
- `.editorconfig`: 定义代码风格的共享配置。
- `.eslintrc.js`: 用于代码质量的 ESLint 配置。
- `.gitignore`: Git 忽略文件列表。
- `package.json`: 项目配置和依赖配置文件。
- `yarn.lock`: Yarn 锁文件，用于锁定依赖包版本。
- `tailwind.config.js`: 配置 Tailwind CSS。
- `vite.config.ts`: 配置 Vite 项目构建工具。

# Project-wide Best Practices
- 遵循模块化和功能性的代码结构。
- 利用TypeScript增强代码的可读性和安全性。
- 实现响应式设计并采用移动优先策略。
- 在适当的地方使用动态加载以优化性能。
- 确保所有开发组件具有响应式支持，并为主要页面加载性能进行优化。

# Element Attributes Order
- `class`
- `id`, `ref`, `name`
- `data-*`
- `src`, `for`, `type`, `href`, `value`, `max-length`, `max`, `min`, `pattern`
- `title`, `alt`, `placeholder`, `aria-*`, `role`
- `required`, `readonly`, `disabled`
- `is`
- `v-for`, `key`
- `v-if`, `v-else-if`, `v-else`
- `v-show`
- `v-cloak`
- `v-pre`
- `v-once`
- `v-model`, `v-bind`, `:`, `v-on`, `@`
- `v-html`, `v-text`

# Comment Guidelines
1. 为公共组件使用提供说明。
2. 为组件中的重要函数或类添加说明。
3. 为复杂的业务逻辑处理添加说明。
4. 特殊情况的代码处理说明，包括特殊用途的变量、临界值、hack、算法等。
5. 多重 `if` 判断语句需添加注释。
6. 注释块必须以 `/**（至少两个星号）开头**/` 。
7. 单行注释使用 `//` 。

## 优先级规范

### 1. 基础组件优先级 (@components)
1. BaseButton - 标准按钮组件
   - 统一按钮样式和交互
   - 支持多种类型、状态和尺寸
   - 集成加载状态和禁用状态

2. BaseForm - 标准表单组件
   - 统一表单布局和验证
   - 集成模态框功能
   - 处理表单提交和重置

3. BaseList - 标准列表组件
   - 统一列表页面布局
   - 集成搜索、分页功能
   - 支持自定义工具栏和操作按钮

4. LoadingSpinner - 加载动画组件
   - 统一加载状态展示
   - 支持自定义加载文本

5. CaptchaVerify - 验证码组件
   - 统一验证码交互
   - 自动处理验证码刷新
   - 集成验证逻辑

6. UploadImage - 图片上传组件
   - 统一图片上传交互
   - 支持多种图片展示形状
   - 集成预览和删除功能

7. BaseIcon - 图标组件
   - 统一图标展示样式
   - 支持多种图标库
   - 简化图标调用

8. IconSelector - 图标选择器组件
   - 统一图标选择交互
   - 支持多种图标库
   - 简化图标选择调用

### 2. 组合式API优先级 (@composables)
1. useLoading - 加载状态管理
   - 统一管理加载状态
   - 提供加载文本控制
   - 简化异步操作的加载状态处理

2. useNotification - 通知提示管理
   - 统一消息通知样式
   - 支持多种通知类型
   - 简化消息提示调用

3. useIcons - 图标管理
   - 统一图标调用方式
   - 支持多种图标库
   - 简化图标调用

### 3. 工具函数优先级 (@utils)
1. request - HTTP请求工具
   - 统一请求配置和错误处理
   - 支持请求拦截和响应拦截
   - 集成认证token管理

2. debounce - 防抖函数
   - 优化频繁操作的性能
   - 支持立即执行选项
   - 简化事件处理

3. filterEmptyValue - 对象空值过滤
   - 优化请求参数处理
   - 移除对象中的空值
   - 简化数据清理操作

### 使用优先级规则
1. 组件使用优先级：
   - 第一优先级：使用项目自定义基础组件(@components)
   - 第二优先级：使用ArcoDesign组件库
   - 第三优先级：创建新的组件

2. 组合式API使用优先级：
   - 第一优先级：使用项目自定义组合式API(@composables)
   - 第二优先级：使用Vue核心组合式API
   - 第三优先级：创建新的组合式API

3. 工具函数使用优先级：
   - 第一优先级：使用项目自定义工具函数(@utils)
   - 第二优先级：使用第三方工具库
   - 第三优先级：创建新的工具函数

4. 请求处理规范：
   - 统一使用 @/utils/request 中的请求方法
   - API请求必须在 @/services 目录下定义
   - 请求响应提示统一使用 useNotification

5. 状态管理规范：
   - 组件内部状态优先使用 ref/reactive
   - 跨组件状态优先使用 Pinia store
   - 临时全局状态可使用 provide/inject

6. 类型定义规范：
   - 优先使用项目定义的类型(@types)
   - 其次扩展第三方库的类型
   - 最后定义新的类型



