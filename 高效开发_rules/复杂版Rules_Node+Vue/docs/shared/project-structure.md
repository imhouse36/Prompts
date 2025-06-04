# 完整项目结构说明

## 🏗️ 推荐的前后端项目结构

### 前端项目结构 (Vue.js)
```
frontend/
├── public/                  # 静态资源
│   ├── index.html
│   ├── favicon.ico
│   └── manifest.json
├── src/
│   ├── assets/             # 资源文件
│   │   ├── images/
│   │   ├── styles/
│   │   │   ├── variables.scss
│   │   │   ├── mixins.scss
│   │   │   └── globals.scss
│   │   └── fonts/
│   ├── components/         # 组件
│   │   ├── base/          # 基础组件
│   │   │   ├── BaseButton.vue
│   │   │   ├── BaseInput.vue
│   │   │   └── BaseModal.vue
│   │   └── business/      # 业务组件
│   │       ├── UserProfile.vue
│   │       └── ProductCard.vue
│   ├── composables/       # 组合式API
│   │   ├── useAuth.ts
│   │   ├── useApi.ts
│   │   └── useEnvironment.ts
│   ├── config/            # 配置文件
│   │   ├── env.ts
│   │   ├── api.ts
│   │   └── constants.ts
│   ├── layouts/           # 布局组件
│   │   ├── DefaultLayout.vue
│   │   └── AuthLayout.vue
│   ├── router/            # 路由配置
│   │   ├── index.ts
│   │   └── guards.ts
│   ├── stores/            # Pinia状态管理
│   │   ├── auth.ts
│   │   ├── user.ts
│   │   └── app.ts
│   ├── utils/             # 工具函数
│   │   ├── request.ts
│   │   ├── helpers.ts
│   │   └── validators.ts
│   ├── views/             # 页面组件
│   │   ├── Home.vue
│   │   ├── Login.vue
│   │   └── Dashboard.vue
│   ├── types/             # TypeScript类型
│   │   ├── api.d.ts
│   │   ├── user.d.ts
│   │   └── env.d.ts
│   ├── App.vue
│   └── main.ts
├── tests/                 # 测试文件
│   ├── unit/
│   ├── e2e/
│   └── fixtures/
├── .env.development       # 环境变量
├── .env.staging
├── .env.production
├── vite.config.ts         # Vite配置
├── tailwind.config.js     # TailwindCSS配置
├── tsconfig.json          # TypeScript配置
├── package.json
└── README.md
```

### 后端项目结构 (Node.js)
```
backend/
├── src/
│   ├── config/            # 配置管理
│   │   ├── environment.js
│   │   ├── database.js
│   │   └── cors.js
│   ├── controllers/       # 控制器层
│   │   ├── authController.js
│   │   ├── userController.js
│   │   └── adminController.js
│   ├── middlewares/       # 中间件
│   │   ├── auth.js
│   │   ├── errorHandler.js
│   │   ├── validation.js
│   │   └── requestLogger.js
│   ├── models/            # 数据模型
│   │   ├── User.js
│   │   ├── Product.js
│   │   └── Order.js
│   ├── routes/            # 路由定义
│   │   ├── auth.js
│   │   ├── users.js
│   │   ├── admin.js
│   │   └── webhooks.js
│   ├── services/          # 业务逻辑层
│   │   ├── authService.js
│   │   ├── userService.js
│   │   ├── emailService.js
│   │   └── fileService.js
│   ├── utils/             # 工具函数
│   │   ├── validators.js
│   │   ├── helpers.js
│   │   ├── encryption.js
│   │   └── logger.js
│   ├── jobs/              # 后台任务
│   │   ├── emailQueue.js
│   │   └── cleanupJob.js
│   └── app.js            # Express应用配置
├── tests/                 # 测试文件
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── uploads/               # 文件上传目录
├── logs/                  # 日志文件
├── templates/             # 邮件模板等
│   └── emails/
├── .env.development       # 环境变量
├── .env.staging
├── .env.production
├── package.json
├── server.js             # 服务入口
└── README.md
```

## 🎯 核心设计原则

### 📁 目录命名规范
- **组件目录**: PascalCase (`UserProfile/`)
- **工具目录**: camelCase (`utils/`, `composables/`)
- **配置目录**: lowercase (`config/`, `routes/`)
- **文件名**: 与目录保持一致的命名风格

### 🔧 模块化原则
- **单一职责**: 每个文件只负责一个功能
- **分层清晰**: 控制器、服务、模型分离
- **可复用性**: 公共组件和工具函数提取
- **可测试性**: 每个模块都应该方便单元测试

### 📦 依赖管理
- **前端**: package.json + yarn.lock
- **后端**: package.json + yarn.lock
- **环境隔离**: 不同环境使用不同的依赖版本
- **安全更新**: 定期更新依赖包

## 🌍 环境配置文件说明

### 前端环境变量
```bash
# .env.development
VITE_APP_ENV=development
VITE_API_BASE_URL=http://localhost:3000/api
VITE_APP_TITLE=项目名称 - 开发环境

# .env.production  
VITE_APP_ENV=production
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_APP_TITLE=项目名称
```

### 后端环境变量
```bash
# .env.development
NODE_ENV=development
PORT=3000
MONGODB_URI=mongodb://localhost:27017/app_dev
JWT_SECRET=dev_secret_key

# .env.production
NODE_ENV=production
PORT=8080
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/app_prod
JWT_SECRET=production_secret_key
```

## 🔄 开发工作流程

### 📝 开发流程
1. **功能开发**: 在对应的功能目录下创建文件
2. **组件编写**: 遵循组件设计规范
3. **接口调用**: 使用统一的API客户端
4. **状态管理**: 合理使用Pinia进行状态管理
5. **测试编写**: 为关键功能编写测试用例

### 🚀 部署流程
1. **环境变量配置**: 确保生产环境变量正确
2. **代码构建**: 执行构建命令生成生产代码
3. **静态资源**: 配置CDN或静态文件服务
4. **服务启动**: 启动后端服务并配置进程管理
5. **监控配置**: 配置日志和性能监控

这个项目结构支持团队协作开发，便于维护和扩展。 