# Trae后端工作目标及步骤规划

## 项目概述
构建基于MongoDB + Redis的数据存储层和服务器基础设施，替代原uni-app的uniCloud云服务架构，提供稳定、高性能的后端支撑。

## 技术栈选型
- **数据库**: MongoDB 5.0+ (主数据库)
- **缓存**: Redis 7.0+ (缓存 + 会话存储)
- **搜索引擎**: Elasticsearch 8.0+ (可选，全文搜索)
- **消息队列**: Redis Bull Queue (任务队列)
- **文件存储**: 本地存储 + 云存储(阿里云OSS/AWS S3)
- **监控**: Prometheus + Grafana
- **日志**: ELK Stack (Elasticsearch + Logstash + Kibana)
- **容器化**: Docker + Docker Compose
- **反向代理**: Nginx
- **进程管理**: PM2
- **备份**: MongoDB Backup + 定时任务

---

## 第一阶段：数据库设计与架构 (3-4天)

### 1.1 MongoDB数据库设计
**目标**: 设计完整的数据库架构，对应原uniCloud数据结构

#### 数据库结构规划
```
ssj_database/
├── users                    # 用户集合
├── articles                 # 文章集合
├── comments                 # 评论集合
├── categories              # 分类集合
├── tags                    # 标签集合
├── banners                 # 轮播图集合
├── favorites               # 收藏集合
├── read_logs               # 阅读记录集合
├── search_logs             # 搜索记录集合
├── sign_in_logs            # 签到记录集合
├── user_sessions           # 用户会话集合
├── system_configs          # 系统配置集合
├── notifications           # 通知消息集合
├── file_uploads            # 文件上传记录集合
├── audit_logs              # 审计日志集合
└── statistics              # 统计数据集合
```

#### 核心集合设计

**1. 用户集合 (users)**
```javascript
{
  _id: ObjectId,
  username: String,           // 用户名(唯一)
  email: String,             // 邮箱(唯一)
  mobile: String,            // 手机号(唯一)
  password: String,          // 加密密码
  salt: String,              // 密码盐值
  nickname: String,          // 昵称
  avatar: {
    url: String,             // 头像URL
    fileId: ObjectId         // 文件ID
  },
  profile: {
    gender: String,          // 性别: male/female/unknown
    birthday: Date,          // 生日
    bio: String,             // 个人简介
    location: String,        // 所在地
    website: String          // 个人网站
  },
  role: String,              // 角色: user/admin/moderator
  status: String,            // 状态: active/inactive/banned
  verification: {
    email: {
      verified: Boolean,     // 邮箱验证状态
      token: String,         // 验证令牌
      expiresAt: Date        // 过期时间
    },
    mobile: {
      verified: Boolean,     // 手机验证状态
      code: String,          // 验证码
      expiresAt: Date        // 过期时间
    }
  },
  security: {
    lastLoginAt: Date,       // 最后登录时间
    lastLoginIp: String,     // 最后登录IP
    loginCount: Number,      // 登录次数
    failedLoginAttempts: Number, // 失败登录次数
    lockedUntil: Date,       // 锁定到期时间
    passwordChangedAt: Date  // 密码修改时间
  },
  preferences: {
    theme: String,           // 主题: light/dark
    language: String,        // 语言: zh-CN/en-US
    timezone: String,        // 时区
    notifications: {
      email: Boolean,        // 邮件通知
      push: Boolean,         // 推送通知
      sms: Boolean           // 短信通知
    },
    privacy: {
      profileVisible: Boolean, // 资料可见性
      activityVisible: Boolean // 活动可见性
    }
  },
  statistics: {
    score: Number,           // 积分
    level: Number,           // 等级
    articlesCount: Number,   // 文章数量
    commentsCount: Number,   // 评论数量
    favoritesCount: Number,  // 收藏数量
    followersCount: Number,  // 粉丝数量
    followingCount: Number   // 关注数量
  },
  tags: [String],            // 用户标签
  createdAt: Date,
  updatedAt: Date,
  deletedAt: Date            // 软删除时间
}
```

**2. 文章集合 (articles)**
```javascript
{
  _id: ObjectId,
  title: String,             // 标题
  slug: String,              // URL友好标识符
  content: String,           // 内容(Markdown)
  excerpt: String,           // 摘要
  cover: {
    url: String,             // 封面图URL
    fileId: ObjectId,        // 文件ID
    alt: String              // 图片描述
  },
  author: ObjectId,          // 作者ID(引用users)
  category: ObjectId,        // 分类ID(引用categories)
  tags: [ObjectId],          // 标签ID数组(引用tags)
  status: String,            // 状态: draft/published/archived
  visibility: String,        // 可见性: public/private/protected
  featured: Boolean,         // 是否推荐
  allowComments: Boolean,    // 允许评论
  seo: {
    metaTitle: String,       // SEO标题
    metaDescription: String, // SEO描述
    keywords: [String]       // 关键词
  },
  statistics: {
    viewCount: Number,       // 浏览次数
    likeCount: Number,       // 点赞次数
    commentCount: Number,    // 评论次数
    favoriteCount: Number,   // 收藏次数
    shareCount: Number       // 分享次数
  },
  publishedAt: Date,         // 发布时间
  createdAt: Date,
  updatedAt: Date,
  deletedAt: Date            // 软删除时间
}
```

**3. 评论集合 (comments)**
```javascript
{
  _id: ObjectId,
  content: String,           // 评论内容
  author: ObjectId,          // 评论者ID(引用users)
  article: ObjectId,         // 文章ID(引用articles)
  parent: ObjectId,          // 父评论ID(回复功能)
  status: String,            // 状态: approved/pending/rejected
  metadata: {
    ipAddress: String,       // IP地址
    userAgent: String,       // 用户代理
    location: String         // 地理位置
  },
  statistics: {
    likeCount: Number,       // 点赞次数
    replyCount: Number       // 回复次数
  },
  createdAt: Date,
  updatedAt: Date,
  deletedAt: Date            // 软删除时间
}
```

### 1.2 数据库索引设计
**性能优化索引**:

```javascript
// 用户集合索引
db.users.createIndex({ "username": 1 }, { unique: true });
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "mobile": 1 }, { unique: true, sparse: true });
db.users.createIndex({ "role": 1, "status": 1 });
db.users.createIndex({ "createdAt": -1 });
db.users.createIndex({ "security.lastLoginAt": -1 });

// 文章集合索引
db.articles.createIndex({ "title": "text", "content": "text", "excerpt": "text" });
db.articles.createIndex({ "author": 1, "createdAt": -1 });
db.articles.createIndex({ "category": 1, "status": 1 });
db.articles.createIndex({ "tags": 1 });
db.articles.createIndex({ "status": 1, "publishedAt": -1 });
db.articles.createIndex({ "featured": 1, "publishedAt": -1 });
db.articles.createIndex({ "statistics.viewCount": -1 });
db.articles.createIndex({ "slug": 1 }, { unique: true });

// 评论集合索引
db.comments.createIndex({ "article": 1, "createdAt": -1 });
db.comments.createIndex({ "author": 1, "createdAt": -1 });
db.comments.createIndex({ "parent": 1 });
db.comments.createIndex({ "status": 1 });

// 复合索引
db.articles.createIndex({ "status": 1, "visibility": 1, "publishedAt": -1 });
db.comments.createIndex({ "article": 1, "status": 1, "createdAt": -1 });
```

### 1.3 数据库配置优化
**MongoDB配置文件 (mongod.conf)**:
```yaml
# 存储配置
storage:
  dbPath: /data/db
  journal:
    enabled: true
  wiredTiger:
    engineConfig:
      cacheSizeGB: 2
    collectionConfig:
      blockCompressor: snappy
    indexConfig:
      prefixCompression: true

# 网络配置
net:
  port: 27017
  bindIp: 127.0.0.1
  maxIncomingConnections: 1000

# 安全配置
security:
  authorization: enabled
  keyFile: /etc/mongodb/keyfile

# 操作分析
operationProfiling:
  slowOpThresholdMs: 100
  mode: slowOp

# 日志配置
systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log
  logRotate: rename
```

---

## 第二阶段：Redis缓存架构 (2-3天)

### 2.1 Redis配置与优化
**Redis配置文件 (redis.conf)**:
```conf
# 内存配置
maxmemory 2gb
maxmemory-policy allkeys-lru

# 持久化配置
save 900 1
save 300 10
save 60 10000

# AOF配置
appendonly yes
appendfsync everysec
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# 网络配置
port 6379
bind 127.0.0.1
timeout 300
tcp-keepalive 300

# 安全配置
requirepass your-redis-password

# 日志配置
loglevel notice
logfile /var/log/redis/redis-server.log
```

### 2.2 缓存策略设计
**缓存键命名规范**:
```
# 用户相关
user:profile:{userId}           # 用户资料
user:session:{sessionId}        # 用户会话
user:permissions:{userId}       # 用户权限
user:statistics:{userId}        # 用户统计

# 文章相关
article:detail:{articleId}      # 文章详情
article:list:page:{page}        # 文章列表
article:hot:daily              # 热门文章(日)
article:hot:weekly             # 热门文章(周)
article:recommended:{userId}    # 推荐文章

# 搜索相关
search:result:{query}:{page}    # 搜索结果
search:suggestions:{prefix}     # 搜索建议
search:hot:keywords            # 热门搜索

# 系统相关
system:config                  # 系统配置
system:statistics:daily        # 日统计
system:online:users           # 在线用户

# 限流相关
ratelimit:api:{ip}:{endpoint}  # API限流
ratelimit:login:{ip}           # 登录限流
```

**缓存过期策略**:
```javascript
// 缓存时间配置
const CACHE_TTL = {
  USER_PROFILE: 3600,        // 1小时
  USER_SESSION: 86400 * 7,   // 7天
  ARTICLE_DETAIL: 1800,      // 30分钟
  ARTICLE_LIST: 300,         // 5分钟
  HOT_ARTICLES: 3600,        // 1小时
  SEARCH_RESULT: 600,        // 10分钟
  SYSTEM_CONFIG: 86400,      // 1天
  STATISTICS: 3600           // 1小时
};
```

### 2.3 会话管理
**会话存储结构**:
```javascript
// 会话数据结构
{
  sessionId: "sess_xxxxxxxxxx",
  userId: ObjectId,
  userAgent: String,
  ipAddress: String,
  loginAt: Date,
  lastActiveAt: Date,
  expiresAt: Date,
  data: {
    permissions: [String],
    preferences: Object,
    cart: Object,           // 购物车(如果有)
    temp: Object            // 临时数据
  }
}
```

---

## 第三阶段：文件存储系统 (2-3天)

### 3.1 本地文件存储
**目录结构设计**:
```
uploads/
├── images/                 # 图片文件
│   ├── avatars/           # 用户头像
│   ├── articles/          # 文章图片
│   ├── banners/           # 轮播图
│   └── temp/              # 临时文件
├── documents/             # 文档文件
├── videos/                # 视频文件
└── others/                # 其他文件
```

**文件命名规范**:
```javascript
// 文件命名格式
const generateFileName = (originalName, userId, type) => {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2);
  const ext = path.extname(originalName);
  return `${type}/${userId}/${timestamp}_${random}${ext}`;
};

// 示例: images/60f1b2b3c4d5e6f7g8h9i0j1/1640995200000_abc123.jpg
```

### 3.2 云存储集成
**阿里云OSS配置**:
```javascript
// OSS配置
const ossConfig = {
  region: 'oss-cn-hangzhou',
  accessKeyId: process.env.OSS_ACCESS_KEY,
  accessKeySecret: process.env.OSS_SECRET_KEY,
  bucket: 'ssj-uploads',
  secure: true,
  timeout: 60000
};

// 上传策略
const uploadPolicy = {
  maxSize: 10 * 1024 * 1024,    // 10MB
  allowedTypes: [
    'image/jpeg',
    'image/png', 
    'image/gif',
    'image/webp'
  ],
  imageProcess: {
    thumbnail: '?x-oss-process=image/resize,w_300,h_300',
    medium: '?x-oss-process=image/resize,w_800,h_600',
    watermark: '?x-oss-process=image/watermark,text_SSJ'
  }
};
```

### 3.3 文件管理数据模型
**文件记录集合 (file_uploads)**:
```javascript
{
  _id: ObjectId,
  filename: String,          // 原始文件名
  storedName: String,        // 存储文件名
  path: String,              // 文件路径
  url: String,               // 访问URL
  mimeType: String,          // MIME类型
  size: Number,              // 文件大小(字节)
  dimensions: {              // 图片尺寸(仅图片)
    width: Number,
    height: Number
  },
  uploader: ObjectId,        // 上传者ID
  uploadType: String,        // 上传类型: avatar/article/banner
  storage: String,           // 存储方式: local/oss/s3
  metadata: {
    alt: String,             // 图片描述
    title: String,           // 图片标题
    tags: [String]           // 标签
  },
  status: String,            // 状态: active/deleted
  createdAt: Date,
  deletedAt: Date
}
```

---

## 第四阶段：搜索引擎集成 (可选，2-3天)

### 4.1 Elasticsearch配置
**ES配置文件 (elasticsearch.yml)**:
```yaml
# 集群配置
cluster.name: ssj-search
node.name: node-1
path.data: /var/lib/elasticsearch
path.logs: /var/log/elasticsearch

# 网络配置
network.host: 127.0.0.1
http.port: 9200

# 内存配置
bootstrap.memory_lock: true

# 安全配置
xpack.security.enabled: false
```

### 4.2 索引设计
**文章索引映射**:
```javascript
// 文章索引映射
const articleMapping = {
  mappings: {
    properties: {
      title: {
        type: 'text',
        analyzer: 'ik_max_word',
        search_analyzer: 'ik_smart'
      },
      content: {
        type: 'text',
        analyzer: 'ik_max_word',
        search_analyzer: 'ik_smart'
      },
      excerpt: {
        type: 'text',
        analyzer: 'ik_max_word'
      },
      author: {
        type: 'keyword'
      },
      category: {
        type: 'keyword'
      },
      tags: {
        type: 'keyword'
      },
      status: {
        type: 'keyword'
      },
      publishedAt: {
        type: 'date'
      },
      statistics: {
        properties: {
          viewCount: { type: 'integer' },
          likeCount: { type: 'integer' },
          commentCount: { type: 'integer' }
        }
      }
    }
  }
};
```

### 4.3 搜索功能实现
**搜索查询构建**:
```javascript
// 多字段搜索
const buildSearchQuery = (keyword, filters = {}) => {
  const query = {
    bool: {
      must: [
        {
          multi_match: {
            query: keyword,
            fields: ['title^3', 'content^2', 'excerpt'],
            type: 'best_fields',
            fuzziness: 'AUTO'
          }
        }
      ],
      filter: []
    }
  };

  // 添加过滤条件
  if (filters.category) {
    query.bool.filter.push({ term: { category: filters.category } });
  }
  
  if (filters.tags) {
    query.bool.filter.push({ terms: { tags: filters.tags } });
  }

  return query;
};
```

---

## 第五阶段：监控与日志系统 (3-4天)

### 5.1 Prometheus监控配置
**监控指标定义**:
```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'ssj-api'
    static_configs:
      - targets: ['localhost:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'mongodb'
    static_configs:
      - targets: ['localhost:9216']

  - job_name: 'redis'
    static_configs:
      - targets: ['localhost:9121']

  - job_name: 'nginx'
    static_configs:
      - targets: ['localhost:9113']
```

**自定义监控指标**:
```javascript
// 应用监控指标
const promClient = require('prom-client');

// HTTP请求计数器
const httpRequestsTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code']
});

// HTTP请求持续时间
const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route'],
  buckets: [0.1, 0.5, 1, 2, 5]
});

// 数据库连接数
const dbConnections = new promClient.Gauge({
  name: 'mongodb_connections_current',
  help: 'Current number of MongoDB connections'
});

// 缓存命中率
const cacheHitRate = new promClient.Gauge({
  name: 'redis_cache_hit_rate',
  help: 'Redis cache hit rate'
});
```

### 5.2 Grafana仪表板
**仪表板配置**:
- API性能监控
- 数据库性能监控
- 缓存性能监控
- 系统资源监控
- 业务指标监控

### 5.3 日志管理
**日志配置 (winston)**:
```javascript
const winston = require('winston');
require('winston-daily-rotate-file');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'ssj-api' },
  transports: [
    // 错误日志
    new winston.transports.DailyRotateFile({
      filename: 'logs/error-%DATE%.log',
      datePattern: 'YYYY-MM-DD',
      level: 'error',
      maxSize: '20m',
      maxFiles: '14d'
    }),
    // 访问日志
    new winston.transports.DailyRotateFile({
      filename: 'logs/access-%DATE%.log',
      datePattern: 'YYYY-MM-DD',
      maxSize: '20m',
      maxFiles: '30d'
    }),
    // 控制台输出
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});
```

---

## 第六阶段：备份与恢复策略 (2-3天)

### 6.1 MongoDB备份策略
**自动备份脚本**:
```bash
#!/bin/bash
# mongodb-backup.sh

# 配置变量
DB_NAME="ssj_database"
BACKUP_DIR="/backup/mongodb"
DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${DB_NAME}_${DATE}.gz"

# 创建备份目录
mkdir -p $BACKUP_DIR

# 执行备份
mongodump --db $DB_NAME --gzip --archive=$BACKUP_DIR/$BACKUP_FILE

# 检查备份结果
if [ $? -eq 0 ]; then
    echo "Backup successful: $BACKUP_FILE"
    
    # 删除7天前的备份
    find $BACKUP_DIR -name "*.gz" -mtime +7 -delete
else
    echo "Backup failed"
    exit 1
fi

# 上传到云存储(可选)
# aws s3 cp $BACKUP_DIR/$BACKUP_FILE s3://ssj-backups/mongodb/
```

**定时任务配置 (crontab)**:
```bash
# 每天凌晨2点执行备份
0 2 * * * /scripts/mongodb-backup.sh

# 每周日凌晨3点执行完整备份
0 3 * * 0 /scripts/mongodb-full-backup.sh
```

### 6.2 Redis备份策略
**Redis备份脚本**:
```bash
#!/bin/bash
# redis-backup.sh

REDIS_CLI="redis-cli"
BACKUP_DIR="/backup/redis"
DATE=$(date +"%Y%m%d_%H%M%S")

# 创建备份目录
mkdir -p $BACKUP_DIR

# 执行BGSAVE
$REDIS_CLI BGSAVE

# 等待备份完成
while [ $($REDIS_CLI LASTSAVE) -eq $($REDIS_CLI LASTSAVE) ]; do
    sleep 1
done

# 复制RDB文件
cp /var/lib/redis/dump.rdb $BACKUP_DIR/dump_$DATE.rdb

# 压缩备份文件
gzip $BACKUP_DIR/dump_$DATE.rdb

echo "Redis backup completed: dump_$DATE.rdb.gz"
```

### 6.3 恢复策略
**MongoDB恢复脚本**:
```bash
#!/bin/bash
# mongodb-restore.sh

BACKUP_FILE=$1
DB_NAME="ssj_database"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

# 停止应用服务
sudo systemctl stop ssj-api

# 删除现有数据库
mongo --eval "db.dropDatabase()" $DB_NAME

# 恢复数据库
mongorestore --db $DB_NAME --gzip --archive=$BACKUP_FILE

# 重建索引
mongo $DB_NAME --eval "db.runCommand({reIndex: 'users'})"
mongo $DB_NAME --eval "db.runCommand({reIndex: 'articles'})"
mongo $DB_NAME --eval "db.runCommand({reIndex: 'comments'})"

# 启动应用服务
sudo systemctl start ssj-api

echo "Database restore completed"
```

---

## 第七阶段：容器化部署 (2-3天)

### 7.1 Docker配置
**MongoDB Dockerfile**:
```dockerfile
FROM mongo:5.0

# 复制配置文件
COPY mongod.conf /etc/mongod.conf

# 复制初始化脚本
COPY init-scripts/ /docker-entrypoint-initdb.d/

# 设置权限
RUN chmod +x /docker-entrypoint-initdb.d/*.sh

# 暴露端口
EXPOSE 27017

# 启动命令
CMD ["mongod", "--config", "/etc/mongod.conf"]
```

**Redis Dockerfile**:
```dockerfile
FROM redis:7-alpine

# 复制配置文件
COPY redis.conf /usr/local/etc/redis/redis.conf

# 创建数据目录
RUN mkdir -p /data

# 暴露端口
EXPOSE 6379

# 启动命令
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
```

### 7.2 Docker Compose配置
**完整的docker-compose.yml**:
```yaml
version: '3.8'

services:
  # MongoDB服务
  mongodb:
    build:
      context: ./docker/mongodb
      dockerfile: Dockerfile
    container_name: ssj-mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_ROOT_PASSWORD}
      MONGO_INITDB_DATABASE: ssj_database
    volumes:
      - mongodb_data:/data/db
      - mongodb_config:/data/configdb
      - ./backups/mongodb:/backup
    ports:
      - "27017:27017"
    networks:
      - ssj-network

  # Redis服务
  redis:
    build:
      context: ./docker/redis
      dockerfile: Dockerfile
    container_name: ssj-redis
    restart: unless-stopped
    environment:
      REDIS_PASSWORD: ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
      - ./backups/redis:/backup
    ports:
      - "6379:6379"
    networks:
      - ssj-network

  # Elasticsearch服务(可选)
  elasticsearch:
    image: elasticsearch:8.5.0
    container_name: ssj-elasticsearch
    restart: unless-stopped
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      - xpack.security.enabled=false
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - ssj-network

  # Nginx反向代理
  nginx:
    image: nginx:alpine
    container_name: ssj-nginx
    restart: unless-stopped
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./docker/nginx/conf.d:/etc/nginx/conf.d
      - ./uploads:/var/www/uploads
      - ./ssl:/etc/nginx/ssl
    ports:
      - "80:80"
      - "443:443"
    depends_on:
      - api
    networks:
      - ssj-network

  # API服务
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: ssj-api
    restart: unless-stopped
    environment:
      NODE_ENV: production
      MONGODB_URI: mongodb://admin:${MONGO_ROOT_PASSWORD}@mongodb:27017/ssj_database?authSource=admin
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379
      JWT_SECRET: ${JWT_SECRET}
    volumes:
      - ./uploads:/app/uploads
      - ./logs:/app/logs
    ports:
      - "8000:8000"
    depends_on:
      - mongodb
      - redis
    networks:
      - ssj-network

  # 监控服务
  prometheus:
    image: prom/prometheus:latest
    container_name: ssj-prometheus
    restart: unless-stopped
    volumes:
      - ./docker/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - ssj-network

  grafana:
    image: grafana/grafana:latest
    container_name: ssj-grafana
    restart: unless-stopped
    environment:
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./docker/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./docker/grafana/datasources:/etc/grafana/provisioning/datasources
    ports:
      - "3000:3000"
    networks:
      - ssj-network

volumes:
  mongodb_data:
  mongodb_config:
  redis_data:
  elasticsearch_data:
  prometheus_data:
  grafana_data:

networks:
  ssj-network:
    driver: bridge
```

---

## 第八阶段：Nginx配置与优化 (1-2天)

### 8.1 Nginx主配置
**nginx.conf**:
```nginx
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log warn;
pid /var/run/nginx.pid;

events {
    worker_connections 1024;
    use epoll;
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # 日志格式
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    '$request_time $upstream_response_time';

    access_log /var/log/nginx/access.log main;

    # 基础配置
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    client_max_body_size 10M;

    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/json
        application/javascript
        application/xml+rss
        application/atom+xml
        image/svg+xml;

    # 包含站点配置
    include /etc/nginx/conf.d/*.conf;
}
```

### 8.2 站点配置
**ssj.conf**:
```nginx
# API服务器配置
upstream api_backend {
    server api:8000;
    keepalive 32;
}

# 限流配置
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/s;

server {
    listen 80;
    server_name api.ssj.com;
    
    # 重定向到HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.ssj.com;

    # SSL配置
    ssl_certificate /etc/nginx/ssl/ssj.crt;
    ssl_certificate_key /etc/nginx/ssl/ssj.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # 安全头
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # API代理
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        
        proxy_pass http://api_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # 超时配置
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # 认证接口特殊限流
    location /api/auth/ {
        limit_req zone=auth_limit burst=10 nodelay;
        
        proxy_pass http://api_backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 文件上传
    location /api/upload/ {
        client_max_body_size 50M;
        proxy_pass http://api_backend;
        proxy_request_buffering off;
    }

    # 静态文件服务
    location /uploads/ {
        alias /var/www/uploads/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
        
        # 图片防盗链
        valid_referers none blocked server_names *.ssj.com;
        if ($invalid_referer) {
            return 403;
        }
    }

    # 健康检查
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

---

## 第九阶段：安全配置 (2-3天)

### 9.1 数据库安全
**MongoDB安全配置**:
```javascript
// 创建管理员用户
use admin
db.createUser({
  user: "admin",
  pwd: "strong_password",
  roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]
})

// 创建应用用户
use ssj_database
db.createUser({
  user: "ssj_app",
  pwd: "app_password",
  roles: ["readWrite"]
})

// 创建只读用户
db.createUser({
  user: "ssj_readonly",
  pwd: "readonly_password",
  roles: ["read"]
})
```

### 9.2 防火墙配置
**UFW防火墙规则**:
```bash
# 启用防火墙
sudo ufw enable

# 允许SSH
sudo ufw allow 22/tcp

# 允许HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 允许内部服务(仅本地)
sudo ufw allow from 127.0.0.1 to any port 27017  # MongoDB
sudo ufw allow from 127.0.0.1 to any port 6379   # Redis
sudo ufw allow from 127.0.0.1 to any port 9200   # Elasticsearch

# 拒绝其他连接
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### 9.3 SSL证书配置
**Let's Encrypt自动续期**:
```bash
#!/bin/bash
# ssl-renew.sh

# 续期证书
certbot renew --quiet

# 重载Nginx
if [ $? -eq 0 ]; then
    nginx -s reload
    echo "SSL certificate renewed successfully"
else
    echo "SSL certificate renewal failed"
fi
```

---

## 第十阶段：性能优化与调优 (2-3天)

### 10.1 数据库性能调优
**MongoDB性能优化**:
```javascript
// 查询性能分析
db.articles.explain("executionStats").find({status: "published"}).sort({publishedAt: -1})

// 索引使用分析
db.articles.getIndexes()
db.articles.stats().indexSizes

// 慢查询分析
db.setProfilingLevel(2, {slowms: 100})
db.system.profile.find().sort({ts: -1}).limit(5)
```

**Redis性能优化**:
```bash
# 内存使用分析
redis-cli info memory

# 慢查询分析
redis-cli slowlog get 10

# 键空间分析
redis-cli --bigkeys
```

### 10.2 系统性能监控
**系统资源监控脚本**:
```bash
#!/bin/bash
# system-monitor.sh

# CPU使用率
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')

# 内存使用率
MEM_USAGE=$(free | grep Mem | awk '{printf "%.2f", $3/$2 * 100.0}')

# 磁盘使用率
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')

# 网络连接数
NET_CONNECTIONS=$(netstat -an | grep ESTABLISHED | wc -l)

echo "CPU: ${CPU_USAGE}%, Memory: ${MEM_USAGE}%, Disk: ${DISK_USAGE}%, Connections: ${NET_CONNECTIONS}"

# 发送到监控系统
curl -X POST http://localhost:9090/api/v1/metrics \
  -d "cpu_usage=${CPU_USAGE}&mem_usage=${MEM_USAGE}&disk_usage=${DISK_USAGE}&net_connections=${NET_CONNECTIONS}"
```

---

## 运维管理

### 1. 自动化部署脚本
**部署脚本 (deploy.sh)**:
```bash
#!/bin/bash
# deploy.sh

set -e

echo "Starting deployment..."

# 拉取最新代码
git pull origin main

# 构建Docker镜像
docker-compose build --no-cache

# 停止旧服务
docker-compose down

# 备份数据库
./scripts/mongodb-backup.sh

# 启动新服务
docker-compose up -d

# 等待服务启动
sleep 30

# 健康检查
if curl -f http://localhost:8000/health; then
    echo "Deployment successful!"
else
    echo "Deployment failed! Rolling back..."
    docker-compose down
    docker-compose up -d
    exit 1
fi
```

### 2. 数据迁移脚本
**从uniCloud迁移数据**:
```javascript
// migrate-from-unicloud.js
const mongoose = require('mongoose');
const fs = require('fs');

// 连接MongoDB
mongoose.connect('mongodb://localhost:27017/ssj_database');

// 迁移用户数据
const migrateUsers = async () => {
  const uniCloudUsers = JSON.parse(fs.readFileSync('./data/uni-id-users.json'));
  
  for (const user of uniCloudUsers) {
    const newUser = {
      username: user.username,
      email: user.email,
      mobile: user.mobile,
      nickname: user.nickname,
      avatar: user.avatar_file?.url,
      role: user.role?.[0] || 'user',
      status: 'active',
      createdAt: new Date(user.register_date),
      updatedAt: new Date(user.last_login_date)
    };
    
    await User.create(newUser);
  }
  
  console.log(`Migrated ${uniCloudUsers.length} users`);
};

// 迁移文章数据
const migrateArticles = async () => {
  const uniCloudArticles = JSON.parse(fs.readFileSync('./data/opendb-news-articles.json'));
  
  for (const article of uniCloudArticles) {
    const newArticle = {
      title: article.title,
      content: article.content,
      excerpt: article.excerpt,
      author: article.user_id,
      status: article.article_status === 1 ? 'published' : 'draft',
      publishedAt: new Date(article.publish_date),
      createdAt: new Date(article.publish_date),
      updatedAt: new Date(article.last_modify_date)
    };
    
    await Article.create(newArticle);
  }
  
  console.log(`Migrated ${uniCloudArticles.length} articles`);
};

// 执行迁移
const runMigration = async () => {
  try {
    await migrateUsers();
    await migrateArticles();
    console.log('Migration completed successfully!');
  } catch (error) {
    console.error('Migration failed:', error);
  } finally {
    mongoose.disconnect();
  }
};

runMigration();
```

---

## 项目里程碑

- **Week 1**: 数据库设计 + Redis配置 (25%)
- **Week 2**: 文件存储 + 搜索引擎 (50%)
- **Week 3**: 监控日志 + 备份恢复 (75%)
- **Week 4**: 容器化部署 + 性能优化 (100%)

## 性能指标

### 1. 数据库性能
- MongoDB查询响应时间 < 50ms
- Redis缓存命中率 > 90%
- 数据库连接池利用率 < 80%

### 2. 系统性能
- CPU使用率 < 70%
- 内存使用率 < 80%
- 磁盘I/O延迟 < 10ms
- 网络带宽利用率 < 60%

### 3. 可用性指标
- 系统可用性 > 99.9%
- 数据库可用性 > 99.95%
- 备份成功率 > 99%
- 恢复时间目标(RTO) < 1小时

## 安全要求

1. **数据安全**: 数据库加密、备份加密
2. **网络安全**: 防火墙、SSL/TLS、VPN
3. **访问安全**: 用户认证、权限控制、审计日志
4. **运维安全**: 安全更新、漏洞扫描、入侵检测

## 风险评估

1. **技术风险**: MongoDB集群配置复杂度 - 中等
2. **数据风险**: 数据迁移完整性验证 - 中等
3. **性能风险**: 高并发下的数据库性能 - 中等
4. **安全风险**: 数据库安全配置 - 高