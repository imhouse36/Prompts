markdown

请用Node.js + Express框架生成RESTful API代码，要求：  
1. **资源**：用户(User)  
   - 字段: id(自动生成), name(string), email(string), status(枚举: active/inactive)  
2. **端点**：  
   - `GET /users`：获取所有用户（分页参数: page, limit）  
   - `POST /users`：创建新用户（需邮箱格式验证）  
   - `PUT /users/:id`：更新用户信息  
   - `DELETE /users/:id`：软删除（标记status=inactive）  
3. **附加**：  
   - 数据存储：内存数组（无需数据库）  
   - 错误处理：返回标准HTTP状态码（如404/400）  
4. **请求/响应示例**：  
   - 创建用户请求：  
     ```json
     { "name": "张三", "email": "zhangsan@example.com" }
     ```
   - 成功响应：  
     ```json
     {
       "id": 1, 
       "name": "张三",
       "email": "zhangsan@example.com",
       "status": "active"
     }
     ```

请用Node.js + Express + Mongoose实现商品(Product)的RESTful API：
### 资源结构
- name: string [必填，最大长度100]
- price: number [最小值0.01]
- category: string [枚举: 电子/服饰/食品]
- stock: number [库存，默认0]
- createdAt: Date [自动生成]

### 端点列表
1. GET /products?category=电子&minPrice=100：分页查询商品（带过滤）
2. POST /products：创建新商品（需管理员权限）
3. GET /products/:id：获取单个商品详情
4. PUT /products/:id：更新商品信息（部分更新）
5. DELETE /products/:id：逻辑删除（标记isDeleted=true）

### 附加要求
- 数据存储：MongoDB（Mongoose模型）
- 价格单位：元（保留两位小数）
- 管理员验证：需Bearer Token鉴权（排除GET端点）
- 分页参数：page（默认1）, limit（默认10）

### 请求示例
```json
// 创建商品请求
{
  "name": "无线耳机",
  "price": 299.99,
  "category": "电子",
  "stock": 100
}

// 成功响应
{
  "_id": "65f1a2d8b3c8d9a7f4e3d2c1",
  "name": "无线耳机",
  "price": 299.99,
  "category": "电子",
  "stock": 100,
  "createdAt": "2025-09-15T08:30:00Z"
}


文本

请用Node.js + Express框架生成RESTful API代码，要求：

资源：用户(User)
字段: id(自动生成), name(string), email(string), status(枚举: active/inactive)
端点：
GET /users：获取所有用户（分页参数: page, limit）
POST /users：创建新用户（需邮箱格式验证）
PUT /users/:id：更新用户信息
DELETE /users/:id：软删除（标记status=inactive）
附加：
数据存储：内存数组（无需数据库）
错误处理：返回标准HTTP状态码（如404/400）
请求/响应示例：
创建用户请求：
{ "name": "张三", "email": "zhangsan@example.com" }
成功响应：
{
  "id": 1, 
  "name": "张三",
  "email": "zhangsan@example.com",
  "status": "active"
}


提示词框架

1. **框架选择**：指定Node.js框架（Express/Koa/NestJS）  
2. **资源定义**：清晰描述资源名称及字段（如用户User: id, name, email）  
3. **操作需求**：列出需实现的API端点（GET/POST/PUT/DELETE）  
4. **附加功能**：中间件/验证/数据库等集成要求  
5. **示例格式**：期望的请求/响应数据结构  

