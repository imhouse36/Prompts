# Trae API工作目标及步骤规划

## 项目概述
基于Node.js + Express.js构建RESTful API服务，为前端应用和移动端提供统一的数据接口，替代原uni-app的uniCloud云函数架构。

## 技术栈选型
- **运行环境**: Node.js 18+
- **Web框架**: Express.js
- **语言**: TypeScript
- **数据库**: MongoDB + Mongoose ODM
- **认证**: JWT + Passport.js
- **文档**: Swagger/OpenAPI 3.0
- **测试**: Jest + Supertest
- **日志**: Winston
- **缓存**: Redis
- **文件存储**: Multer + 云存储(阿里云OSS/AWS S3)
- **邮件服务**: Nodemailer
- **短信服务**: 阿里云短信/腾讯云短信
- **任务队列**: Bull Queue
- **监控**: PM2 + 健康检查

---

## 第一阶段：项目初始化与基础架构 (3-4天)

### 1.1 项目结构设计
**目标**: 建立标准化的Node.js API项目结构

```
ssj-api/
├── src/
│   ├── config/              # 配置文件
│   │   ├── database.ts      # 数据库配置
│   │   ├── redis.ts         # Redis配置
│   │   ├── jwt.ts           # JWT配置
│   │   ├── upload.ts        # 文件上传配置
│   │   └── index.ts         # 配置入口
│   ├── controllers/         # 控制器层
│   │   ├── auth.controller.ts    # 认证控制器
│   │   ├── user.controller.ts    # 用户控制器
│   │   ├── article.controller.ts # 文章控制器
│   │   ├── banner.controller.ts  # 轮播图控制器
│   │   ├── comment.controller.ts # 评论控制器
│   │   ├── category.controller.ts # 分类控制器
│   │   └── upload.controller.ts  # 文件上传控制器
│   ├── middleware/          # 中间件
│   │   ├── auth.middleware.ts    # 认证中间件
│   │   ├── permission.middleware.ts # 权限中间件
│   │   ├── validation.middleware.ts # 验证中间件
│   │   ├── rateLimit.middleware.ts  # 限流中间件
│   │   ├── cors.middleware.ts       # 跨域中间件
│   │   ├── logger.middleware.ts     # 日志中间件
│   │   └── error.middleware.ts      # 错误处理中间件
│   ├── models/              # 数据模型
│   │   ├── User.model.ts    # 用户模型
│   │   ├── Article.model.ts # 文章模型
│   │   ├── Comment.model.ts # 评论模型
│   │   ├── Category.model.ts # 分类模型
│   │   ├── Banner.model.ts  # 轮播图模型
│   │   ├── Tag.model.ts     # 标签模型
│   │   ├── Favorite.model.ts # 收藏模型
│   │   ├── ReadLog.model.ts # 阅读记录模型
│   │   ├── SearchLog.model.ts # 搜索记录模型
│   │   └── SignIn.model.ts  # 签到记录模型
│   ├── routes/              # 路由定义
│   │   ├── auth.routes.ts   # 认证路由
│   │   ├── user.routes.ts   # 用户路由
│   │   ├── article.routes.ts # 文章路由
│   │   ├── banner.routes.ts # 轮播图路由
│   │   ├── comment.routes.ts # 评论路由
│   │   ├── category.routes.ts # 分类路由
│   │   ├── upload.routes.ts # 文件上传路由
│   │   └── index.ts         # 路由入口
│   ├── services/            # 业务逻辑层
│   │   ├── auth.service.ts  # 认证服务
│   │   ├── user.service.ts  # 用户服务
│   │   ├── article.service.ts # 文章服务
│   │   ├── banner.service.ts # 轮播图服务
│   │   ├── comment.service.ts # 评论服务
│   │   ├── email.service.ts # 邮件服务
│   │   ├── sms.service.ts   # 短信服务
│   │   ├── upload.service.ts # 文件上传服务
│   │   ├── cache.service.ts # 缓存服务
│   │   └── search.service.ts # 搜索服务
│   ├── utils/               # 工具函数
│   │   ├── response.util.ts # 响应格式化
│   │   ├── validation.util.ts # 验证工具
│   │   ├── encryption.util.ts # 加密工具
│   │   ├── date.util.ts     # 日期工具
│   │   ├── file.util.ts     # 文件工具
│   │   └── logger.util.ts   # 日志工具
│   ├── types/               # TypeScript类型定义
│   │   ├── auth.types.ts    # 认证类型
│   │   ├── user.types.ts    # 用户类型
│   │   ├── article.types.ts # 文章类型
│   │   ├── common.types.ts  # 通用类型
│   │   └── api.types.ts     # API类型
│   ├── validators/          # 数据验证
│   │   ├── auth.validator.ts # 认证验证
│   │   ├── user.validator.ts # 用户验证
│   │   ├── article.validator.ts # 文章验证
│   │   └── common.validator.ts # 通用验证
│   ├── jobs/                # 定时任务
│   │   ├── cleanup.job.ts   # 清理任务
│   │   ├── statistics.job.ts # 统计任务
│   │   └── backup.job.ts    # 备份任务
│   ├── app.ts               # Express应用配置
│   └── server.ts            # 服务器启动文件
├── tests/                   # 测试文件
│   ├── unit/               # 单元测试
│   ├── integration/        # 集成测试
│   └── fixtures/           # 测试数据
├── docs/                   # 文档
│   ├── api.md              # API文档
│   └── deployment.md       # 部署文档
├── scripts/                # 脚本文件
│   ├── seed.ts             # 数据种子
│   └── migrate.ts          # 数据迁移
├── .env.example            # 环境变量示例
├── .gitignore
├── package.json
├── tsconfig.json
├── jest.config.js
├── docker-compose.yml
├── Dockerfile
└── README.md
```

### 1.2 基础配置
**工作内容**:

1. **项目初始化**
```bash
mkdir ssj-api && cd ssj-api
npm init -y
npm install express mongoose cors helmet morgan compression dotenv
npm install -D typescript @types/node @types/express ts-node nodemon
npm install -D jest @types/jest supertest @types/supertest
```

2. **TypeScript配置**
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

3. **环境变量配置**
```env
# .env.example
NODE_ENV=development
PORT=8000

# 数据库配置
MONGODB_URI=mongodb://localhost:27017/ssj
REDIS_URL=redis://localhost:6379

# JWT配置
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRE=7d
JWT_REFRESH_EXPIRE=30d

# 文件上传配置
UPLOAD_PATH=./uploads
MAX_FILE_SIZE=10485760
ALLOWED_FILE_TYPES=image/jpeg,image/png,image/gif

# 邮件配置
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password

# 短信配置
SMS_ACCESS_KEY=your-sms-access-key
SMS_SECRET_KEY=your-sms-secret-key

# 云存储配置
OSS_REGION=oss-cn-hangzhou
OSS_BUCKET=your-bucket-name
OSS_ACCESS_KEY=your-oss-access-key
OSS_SECRET_KEY=your-oss-secret-key
```

---

## 第二阶段：数据模型设计 (2-3天)

### 2.1 核心数据模型
**目标**: 设计完整的数据库模型，对应原uniCloud数据库结构

#### 用户模型 (User.model.ts)
```typescript
interface IUser {
  _id: ObjectId;
  username: string;           // 用户名
  email: string;             // 邮箱
  mobile?: string;           // 手机号
  password: string;          // 密码(加密)
  nickname?: string;         // 昵称
  avatar?: string;           // 头像URL
  gender?: 'male' | 'female' | 'unknown'; // 性别
  birthday?: Date;           // 生日
  bio?: string;              // 个人简介
  role: 'user' | 'admin' | 'moderator'; // 角色
  status: 'active' | 'inactive' | 'banned'; // 状态
  emailVerified: boolean;    // 邮箱验证状态
  mobileVerified: boolean;   // 手机验证状态
  lastLoginAt?: Date;        // 最后登录时间
  loginCount: number;        // 登录次数
  score: number;             // 积分
  level: number;             // 等级
  tags: string[];            // 用户标签
  preferences: {             // 用户偏好
    theme: 'light' | 'dark';
    language: 'zh-CN' | 'en-US';
    notifications: {
      email: boolean;
      push: boolean;
      sms: boolean;
    };
  };
  createdAt: Date;
  updatedAt: Date;
}
```

#### 文章模型 (Article.model.ts)
```typescript
interface IArticle {
  _id: ObjectId;
  title: string;             // 标题
  content: string;           // 内容
  excerpt?: string;          // 摘要
  cover?: string;            // 封面图
  author: ObjectId;          // 作者ID
  category: ObjectId;        // 分类ID
  tags: ObjectId[];          // 标签ID数组
  status: 'draft' | 'published' | 'archived'; // 状态
  visibility: 'public' | 'private' | 'protected'; // 可见性
  featured: boolean;         // 是否推荐
  allowComments: boolean;    // 允许评论
  viewCount: number;         // 浏览次数
  likeCount: number;         // 点赞次数
  commentCount: number;      // 评论次数
  favoriteCount: number;     // 收藏次数
  shareCount: number;        // 分享次数
  publishedAt?: Date;        // 发布时间
  createdAt: Date;
  updatedAt: Date;
}
```

#### 评论模型 (Comment.model.ts)
```typescript
interface IComment {
  _id: ObjectId;
  content: string;           // 评论内容
  author: ObjectId;          // 评论者ID
  article: ObjectId;         // 文章ID
  parent?: ObjectId;         // 父评论ID(回复)
  status: 'approved' | 'pending' | 'rejected'; // 状态
  likeCount: number;         // 点赞次数
  replyCount: number;        // 回复次数
  ipAddress: string;         // IP地址
  userAgent: string;         // 用户代理
  createdAt: Date;
  updatedAt: Date;
}
```

### 2.2 辅助数据模型

#### 分类模型 (Category.model.ts)
#### 标签模型 (Tag.model.ts)
#### 轮播图模型 (Banner.model.ts)
#### 收藏模型 (Favorite.model.ts)
#### 阅读记录模型 (ReadLog.model.ts)
#### 搜索记录模型 (SearchLog.model.ts)
#### 签到记录模型 (SignIn.model.ts)

---

## 第三阶段：认证与权限系统 (3-4天)

### 3.1 JWT认证系统
**功能要求**:
- 用户注册/登录
- JWT Token生成与验证
- Refresh Token机制
- 密码加密与验证
- 邮箱/手机验证

**API端点设计**:
```
POST /api/auth/register          # 用户注册
POST /api/auth/login             # 用户登录
POST /api/auth/logout            # 用户登出
POST /api/auth/refresh           # 刷新Token
POST /api/auth/forgot-password   # 忘记密码
POST /api/auth/reset-password    # 重置密码
POST /api/auth/verify-email      # 验证邮箱
POST /api/auth/verify-mobile     # 验证手机
GET  /api/auth/me                # 获取当前用户信息
```

### 3.2 权限控制系统
**权限级别**:
- **游客**: 浏览公开内容
- **普通用户**: 发表评论、收藏文章
- **认证用户**: 发布文章、个人中心
- **管理员**: 内容管理、用户管理
- **超级管理员**: 系统配置、权限管理

**中间件设计**:
```typescript
// 认证中间件
export const authenticate = async (req: Request, res: Response, next: NextFunction) => {
  // JWT验证逻辑
};

// 权限中间件
export const authorize = (roles: string[]) => {
  return (req: Request, res: Response, next: NextFunction) => {
    // 权限验证逻辑
  };
};
```

---

## 第四阶段：核心业务API开发 (5-7天)

### 4.1 用户管理API
**功能模块**:
- 用户信息管理
- 用户偏好设置
- 用户统计信息
- 用户关系管理

**API端点**:
```
GET    /api/users/profile        # 获取用户资料
PUT    /api/users/profile        # 更新用户资料
POST   /api/users/avatar         # 上传头像
GET    /api/users/statistics     # 获取用户统计
GET    /api/users/preferences    # 获取用户偏好
PUT    /api/users/preferences    # 更新用户偏好
POST   /api/users/change-password # 修改密码
DELETE /api/users/account        # 删除账户
```

### 4.2 文章管理API
**功能模块**:
- 文章CRUD操作
- 文章搜索与筛选
- 文章统计与推荐
- 文章状态管理

**API端点**:
```
GET    /api/articles             # 获取文章列表
POST   /api/articles             # 创建文章
GET    /api/articles/:id         # 获取文章详情
PUT    /api/articles/:id         # 更新文章
DELETE /api/articles/:id         # 删除文章
POST   /api/articles/:id/like    # 点赞文章
POST   /api/articles/:id/favorite # 收藏文章
POST   /api/articles/:id/share   # 分享文章
GET    /api/articles/search      # 搜索文章
GET    /api/articles/trending    # 热门文章
GET    /api/articles/recommended # 推荐文章
```

### 4.3 评论管理API
**功能模块**:
- 评论CRUD操作
- 评论审核管理
- 评论统计分析
- 评论举报处理

**API端点**:
```
GET    /api/comments             # 获取评论列表
POST   /api/comments             # 发表评论
GET    /api/comments/:id         # 获取评论详情
PUT    /api/comments/:id         # 更新评论
DELETE /api/comments/:id         # 删除评论
POST   /api/comments/:id/like    # 点赞评论
POST   /api/comments/:id/reply   # 回复评论
POST   /api/comments/:id/report  # 举报评论
```

### 4.4 内容管理API
**功能模块**:
- 分类管理
- 标签管理
- 轮播图管理
- 内容审核

**API端点**:
```
# 分类管理
GET    /api/categories           # 获取分类列表
POST   /api/categories           # 创建分类
PUT    /api/categories/:id       # 更新分类
DELETE /api/categories/:id       # 删除分类

# 标签管理
GET    /api/tags                 # 获取标签列表
POST   /api/tags                 # 创建标签
PUT    /api/tags/:id             # 更新标签
DELETE /api/tags/:id             # 删除标签

# 轮播图管理
GET    /api/banners              # 获取轮播图列表
POST   /api/banners              # 创建轮播图
PUT    /api/banners/:id          # 更新轮播图
DELETE /api/banners/:id          # 删除轮播图
```

---

## 第五阶段：文件上传与存储 (2-3天)

### 5.1 文件上传系统
**功能要求**:
- 多文件上传支持
- 文件类型验证
- 文件大小限制
- 图片压缩处理
- 云存储集成

**技术实现**:
```typescript
// 文件上传中间件
import multer from 'multer';
import { CloudStorage } from './cloud-storage';

const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 10 * 1024 * 1024, // 10MB
  },
  fileFilter: (req, file, cb) => {
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    if (allowedTypes.includes(file.mimetype)) {
      cb(null, true);
    } else {
      cb(new Error('Invalid file type'), false);
    }
  },
});
```

### 5.2 云存储集成
**支持平台**:
- 阿里云OSS
- 腾讯云COS
- AWS S3
- 本地存储(开发环境)

**API端点**:
```
POST   /api/upload/image         # 上传图片
POST   /api/upload/file          # 上传文件
DELETE /api/upload/:id           # 删除文件
GET    /api/upload/presigned     # 获取预签名URL
```

---

## 第六阶段：搜索与推荐系统 (3-4天)

### 6.1 全文搜索
**技术方案**:
- MongoDB文本索引
- Elasticsearch集成(可选)
- 搜索结果排序
- 搜索建议功能

**搜索功能**:
- 文章标题搜索
- 文章内容搜索
- 作者搜索
- 标签搜索
- 高级搜索

### 6.2 推荐系统
**推荐算法**:
- 基于内容的推荐
- 协同过滤推荐
- 热门内容推荐
- 个性化推荐

**API端点**:
```
GET /api/search?q=keyword        # 搜索内容
GET /api/search/suggestions      # 搜索建议
GET /api/search/hot              # 热门搜索
GET /api/recommendations/articles # 推荐文章
GET /api/recommendations/users   # 推荐用户
```

---

## 第七阶段：缓存与性能优化 (2-3天)

### 7.1 Redis缓存策略
**缓存场景**:
- 用户会话缓存
- 文章列表缓存
- 热门内容缓存
- 搜索结果缓存
- 统计数据缓存

**缓存实现**:
```typescript
// 缓存服务
export class CacheService {
  private redis: Redis;

  async get<T>(key: string): Promise<T | null> {
    const data = await this.redis.get(key);
    return data ? JSON.parse(data) : null;
  }

  async set(key: string, value: any, ttl: number = 3600): Promise<void> {
    await this.redis.setex(key, ttl, JSON.stringify(value));
  }

  async del(key: string): Promise<void> {
    await this.redis.del(key);
  }
}
```

### 7.2 数据库优化
**优化策略**:
- 索引优化
- 查询优化
- 分页优化
- 聚合查询优化

**索引设计**:
```typescript
// 用户模型索引
userSchema.index({ email: 1 }, { unique: true });
userSchema.index({ mobile: 1 }, { unique: true, sparse: true });
userSchema.index({ username: 1 }, { unique: true });

// 文章模型索引
articleSchema.index({ title: 'text', content: 'text' });
articleSchema.index({ author: 1, createdAt: -1 });
articleSchema.index({ category: 1, status: 1 });
articleSchema.index({ tags: 1 });
```

---

## 第八阶段：通知与消息系统 (2-3天)

### 8.1 邮件通知系统
**通知场景**:
- 用户注册验证
- 密码重置
- 文章发布通知
- 评论回复通知
- 系统公告

### 8.2 短信通知系统
**通知场景**:
- 手机验证码
- 登录异常提醒
- 重要操作确认

### 8.3 站内消息系统
**消息类型**:
- 系统消息
- 用户消息
- 评论通知
- 点赞通知
- 关注通知

---

## 第九阶段：统计与分析 (2-3天)

### 9.1 数据统计API
**统计维度**:
- 用户统计(注册、活跃、留存)
- 内容统计(文章、评论、浏览)
- 行为统计(搜索、分享、收藏)
- 性能统计(响应时间、错误率)

### 9.2 数据分析
**分析功能**:
- 用户行为分析
- 内容热度分析
- 搜索趋势分析
- 系统性能分析

**API端点**:
```
GET /api/analytics/overview      # 概览统计
GET /api/analytics/users         # 用户统计
GET /api/analytics/articles      # 文章统计
GET /api/analytics/performance   # 性能统计
```

---

## 第十阶段：API文档与测试 (2-3天)

### 10.1 Swagger API文档
**文档内容**:
- API端点说明
- 请求参数定义
- 响应格式说明
- 错误码定义
- 认证方式说明

**文档生成**:
```typescript
// swagger配置
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'SSJ API Documentation',
      version: '1.0.0',
      description: 'SSJ项目API接口文档',
    },
    servers: [
      {
        url: 'http://localhost:8000',
        description: '开发环境',
      },
    ],
  },
  apis: ['./src/routes/*.ts'],
};
```

### 10.2 API测试
**测试类型**:
- 单元测试
- 集成测试
- 端到端测试
- 性能测试

**测试框架**:
```typescript
// Jest + Supertest
import request from 'supertest';
import app from '../src/app';

describe('Auth API', () => {
  test('POST /api/auth/register', async () => {
    const response = await request(app)
      .post('/api/auth/register')
      .send({
        username: 'testuser',
        email: 'test@example.com',
        password: 'password123'
      });
    
    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
  });
});
```

---

## 第十一阶段：部署与监控 (2-3天)

### 11.1 Docker容器化
**Dockerfile配置**:
```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 8000

CMD ["npm", "start"]
```

**docker-compose配置**:
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - NODE_ENV=production
    depends_on:
      - mongodb
      - redis
  
  mongodb:
    image: mongo:5.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

### 11.2 监控与日志
**监控指标**:
- API响应时间
- 错误率统计
- 内存使用率
- CPU使用率
- 数据库连接数

**日志管理**:
- 访问日志
- 错误日志
- 性能日志
- 安全日志

---

## API设计规范

### 1. RESTful设计原则
- 使用HTTP动词(GET, POST, PUT, DELETE)
- 资源导向的URL设计
- 统一的响应格式
- 合理的HTTP状态码

### 2. 响应格式标准
```typescript
// 成功响应
{
  "success": true,
  "data": {},
  "message": "操作成功",
  "timestamp": "2024-01-01T00:00:00.000Z"
}

// 错误响应
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "参数验证失败",
    "details": []
  },
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

### 3. 分页格式标准
```typescript
{
  "success": true,
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "limit": 20,
      "total": 100,
      "pages": 5,
      "hasNext": true,
      "hasPrev": false
    }
  }
}
```

---

## 安全策略

### 1. 认证安全
- JWT Token过期机制
- Refresh Token轮换
- 密码强度验证
- 登录失败限制

### 2. 数据安全
- 输入数据验证
- SQL注入防护
- XSS攻击防护
- CSRF攻击防护

### 3. 接口安全
- API限流控制
- IP白名单机制
- HTTPS强制使用
- CORS跨域控制

---

## 性能指标

### 1. 响应时间目标
- 简单查询: < 100ms
- 复杂查询: < 500ms
- 文件上传: < 2s
- 批量操作: < 5s

### 2. 并发处理能力
- 支持1000+并发连接
- QPS > 500
- 99%请求响应时间 < 1s

### 3. 可用性目标
- 系统可用性 > 99.9%
- 数据库可用性 > 99.95%
- 缓存可用性 > 99.9%

---

## 项目里程碑

- **Week 1**: 基础架构 + 数据模型 (30%)
- **Week 2**: 认证系统 + 核心API (60%)
- **Week 3**: 文件上传 + 搜索推荐 (80%)
- **Week 4**: 优化测试 + 部署上线 (100%)

## 风险评估

1. **技术风险**: MongoDB性能优化 - 中等
2. **进度风险**: 复杂业务逻辑开发 - 中等
3. **质量风险**: API接口测试覆盖 - 低
4. **安全风险**: 认证授权机制 - 中等