markdown
# Node.js + Express 开发规范手册

## 目录
1. [项目结构规范](#项目结构规范)
2. [编码风格规范](#编码风格规范)
3. [路由设计规范](#路由设计规范)
4. [中间件使用规范](#中间件使用规范)
5. [错误处理规范](#错误处理规范)
6. [安全规范](#安全规范)
7. [日志规范](#日志规范)
8. [测试规范](#测试规范)
9. [性能优化建议](#性能优化建议)
10. [环境配置规范](#环境配置规范)
11. [代码提交规范](#代码提交规范)

---

## 项目结构规范
```bash
project-root/
├── src/                  # 主源代码目录
│   ├── config/           # 配置文件
│   ├── controllers/      # 控制器（业务逻辑）
│   ├── routes/           # 路由定义
│   ├── middlewares/      # 自定义中间件
│   ├── models/           # 数据模型（ORM定义）
│   ├── services/         # 业务逻辑层
│   ├── utils/            # 工具函数
│   └── app.js            # Express应用初始化
├── tests/                # 测试目录
├── .env                  # 环境变量（不提交到版本库）
├── .eslintrc.js          # ESLint配置
├── .gitignore            # Git忽略文件
├── package.json          # 项目依赖
└── server.js             # 服务入口文件

编码风格规范
变量命名：

使用 camelCase 命名变量和函数

类名使用 PascalCase

常量使用 UPPER_SNAKE_CASE

缩进与空格：

使用2个空格缩进

操作符两侧加空格：const sum = a + b;

分号：

语句末尾必须加分号

引号：

使用单引号 ，除非字符串中有单引号才用双引号

异步操作：

使用 async/await 替代回调函数

避免使用 Promise.then() 嵌套


javascript
// ✅ 推荐写法
const getUser = async (userId) => {
  try {
    const user = await User.findById(userId);
    return user;
  } catch (error) {
    throw new Error('User not found');
  }
};

// ❌ 避免写法
const getUser = (userId) => {
  return User.findById(userId)
    .then(user => user)
    .catch(error => {
      throw new Error('User not found');
    });
};
路由设计规范
RESTful 风格：

使用资源名称复数形式

HTTP方法对应CRUD操作：

GET /users - 获取用户列表

POST /users - 创建用户

GET /users/:id - 获取单个用户

PUT /users/:id - 更新用户

DELETE /users/:id - 删除用户

路由文件组织：

每个资源对应一个路由文件

在 app.js 中统一注册路由

javascript
// routes/users.js
const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');

router.get('/', userController.listUsers);
router.post('/', userController.createUser);
router.get('/:id', userController.getUser);
router.put('/:id', userController.updateUser);
router.delete('/:id', userController.deleteUser);

module.exports = router;
中间件使用规范
中间件顺序：

安全中间件（如helmet、cors）放在最前

然后是日志、body解析等中间件

最后是路由和错误处理中间件

javascript
// app.js
const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const morgan = require('morgan');

const app = express();

// 安全中间件
app.use(helmet());
app.use(cors());

// 日志和解析
app.use(morgan('combined'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 路由
app.use('/api/users', require('./routes/users'));

// 错误处理中间件（放最后）
app.use(errorHandler);
错误处理规范
统一错误处理中间件：

放在所有路由之后

捕获同步和异步错误

javascript
// middlewares/errorHandler.js
const errorHandler = (err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';
  
  // 开发环境返回堆栈信息
  const response = {
    error: {
      message,
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
    }
  };

  res.status(statusCode).json(response);
};

module.exports = errorHandler;
自定义错误类：

javascript
// utils/AppError.js
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.status = `${statusCode}`.startsWith('4') ? 'fail' : 'error';
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

module.exports = AppError;
安全规范
基础防护：

使用 helmet 设置安全头部

使用 cors 限制跨域请求

输入验证：

使用 express-validator 校验请求参数

javascript
const { body, validationResult } = require('express-validator');

router.post('/users', 
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 6 }),
  (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    // 处理请求
  }
);
防攻击：

使用 express-rate-limit 防止暴力攻击

使用 helmet 的 contentSecurityPolicy 防止XSS

日志规范
日志级别：

开发环境：debug

生产环境：info、warn、error

日志格式：

使用JSON格式，方便日志分析系统处理

包含关键信息：时间戳、请求ID、IP、方法、URL、响应状态、响应时间

日志库：

推荐使用 winston 或 pino

javascript
// utils/logger.js
const winston = require('winston');

const logger = winston.createLogger({
  level: process.env.NODE_ENV === 'production' ? 'info' : 'debug',
  format: winston.format.json(),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' })
  ]
});

module.exports = logger;
测试规范
测试框架：

使用 Jest 或 Mocha + Chai

接口测试使用 Supertest

测试目录结构：

单元测试：tests/unit/

集成测试：tests/integration/

E2E测试：tests/e2e/

测试覆盖率：

目标不低于80%

使用 Istanbul 或 Jest 自带的覆盖率工具

javascript
// tests/integration/user.test.js
const request = require('supertest');
const app = require('../../src/app');
const User = require('../../src/models/User');

describe('User API', () => {
  beforeEach(async () => {
    await User.deleteMany();
  });

  it('should create a new user', async () => {
    const res = await request(app)
      .post('/api/users')
      .send({ name: 'John', email: 'john@example.com' });
    
    expect(res.statusCode).toEqual(201);
    expect(res.body).toHaveProperty('id');
  });
});
性能优化建议
启用压缩：

javascript
const compression = require('compression');
app.use(compression());
使用ETag：

javascript
app.set('etag', 'strong');
避免同步方法：

禁止使用 fs.readFileSync 等同步方法

集群模式：

生产环境使用 cluster 模块或多进程管理（如PM2）

javascript
// 集群模式示例
const cluster = require('cluster');
const numCPUs = require('os').cpus().length;

if (cluster.isMaster) {
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork();
  }
} else {
  // 启动Express应用
  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`Worker ${process.pid} started on port ${PORT}`);
  });
}
环境配置规范
环境变量：

使用 dotenv 加载 .env 文件

敏感信息（如数据库密码）必须通过环境变量注入

javascript
// config/config.js
require('dotenv').config();

module.exports = {
  env: process.env.NODE_ENV || 'development',
  port: process.env.PORT || 3000,
  db: {
    uri: process.env.MONGODB_URI || 'mongodb://localhost:27017/myapp'
  },
  jwtSecret: process.env.JWT_SECRET || 'default_secret'
};
配置分离：

不同环境有不同配置（development, test, production）

代码提交规范
Git Commit 规范：

遵循 Conventional Commits

格式：<type>(<scope>): <description>

feat(auth): add JWT authentication
fix(users): correct user update validation
docs: update API documentation
refactor: reorganize middleware directory
Git 工作流：

使用 Git Flow 或 GitHub Flow

功能分支命名：feature/<feature-name>

修复分支命名：fix/<issue-name>

附：基础 .eslintrc.js 配置

javascript
module.exports = {
  env: {
    node: true,
    es2021: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:node/recommended',
  ],
  parserOptions: {
    ecmaVersion: 12,
  },
  rules: {
    'indent': ['error', 2],
    'quotes': ['error', 'single'],
    'semi': ['error', 'always'],
    'no-console': 'warn',
    'node/no-unpublished-require': 'off',
    'node/no-unsupported-features/es-syntax': 'off',
  },
};
本规范基于Express最佳实践和Node.js社区标准制定，团队应根据具体项目需求调整。定期复审和更新规范以保持技术时效性。