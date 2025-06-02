# CORS跨域问题解决方案

## 🚨 问题描述

在生产环境部署后，前端提交表单时出现CORS跨域错误：

```
Access to fetch at 'https://jmnode.13jue.com/api/feishu/add-record' from origin 'https://jiameng.13jue.com' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## 🔧 已实施的解决方案

### 1. 完善CORS配置

在 `app.js` 中增强了CORS配置：

```javascript
app.use(cors({
  origin: [
    'http://localhost:5173', 
    'http://127.0.0.1:5173',
    'https://jiameng.13jue.com' // 生产环境前端域名
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
  optionsSuccessStatus: 200 // 支持旧版浏览器
}));
```

### 2. 添加全局OPTIONS处理中间件

在 `app.js` 中添加了专门处理预检请求的中间件：

```javascript
// 全局OPTIONS处理中间件
app.use((req, res, next) => {
  if (req.method === 'OPTIONS') {
    res.header('Access-Control-Allow-Origin', req.headers.origin);
    res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');
    res.header('Access-Control-Allow-Credentials', 'true');
    return res.status(200).end();
  }
  next();
});
```

### 3. 路由级OPTIONS处理

在 `feishuRoutes.js` 中为特定路由添加了OPTIONS处理：

```javascript
// 处理预检请求
router.options('/add-record', (req, res) => {
  res.status(200).end();
});
```

## 📋 部署检查清单

### 后端服务器配置

1. **确保代码更新**：
   - [ ] 将更新后的 `app.js` 部署到生产服务器
   - [ ] 将更新后的 `feishuRoutes.js` 部署到生产服务器
   - [ ] 重启Node.js服务

2. **服务器环境检查**：
   - [ ] 确认Node.js服务正常运行
   - [ ] 检查防火墙设置，确保端口开放
   - [ ] 验证HTTPS证书配置正确

3. **反向代理配置**（如使用Nginx）：
   ```nginx
   location /api {
       proxy_pass http://localhost:3000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
       
       # CORS headers
       add_header Access-Control-Allow-Origin $http_origin always;
       add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
       add_header Access-Control-Allow-Headers "Content-Type, Authorization, X-Requested-With" always;
       add_header Access-Control-Allow-Credentials true always;
       
       if ($request_method = 'OPTIONS') {
           return 204;
       }
   }
   ```

## 🧪 测试验证

### 1. 手动测试CORS

使用curl测试预检请求：

```bash
# 测试OPTIONS预检请求
curl -X OPTIONS \
  -H "Origin: https://jiameng.13jue.com" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -v https://jmnode.13jue.com/api/feishu/add-record
```

期望响应包含：
- `Access-Control-Allow-Origin: https://jiameng.13jue.com`
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With`

### 2. 浏览器开发者工具检查

1. 打开 https://jiameng.13jue.com/
2. 打开浏览器开发者工具（F12）
3. 切换到Network标签
4. 提交表单
5. 检查是否有OPTIONS请求，以及响应头是否正确

## 🔍 常见问题排查

### 问题1：OPTIONS请求返回404
**原因**：服务器没有正确处理OPTIONS方法  
**解决**：确保全局OPTIONS中间件已部署

### 问题2：CORS头部缺失
**原因**：反向代理或CDN配置问题  
**解决**：检查Nginx/Apache/CDN的CORS配置

### 问题3：域名不匹配
**原因**：CORS配置中的域名与实际访问域名不一致  
**解决**：确认origin配置包含正确的生产域名

### 问题4：HTTPS混合内容
**原因**：HTTPS页面请求HTTP接口  
**解决**：确保前后端都使用HTTPS

## 📞 紧急处理方案

如果问题仍然存在，可以临时使用以下方案：

### 方案1：临时允许所有域名（仅用于测试）

```javascript
app.use(cors({
  origin: '*', // 临时允许所有域名
  credentials: false // 注意：使用通配符时必须设为false
}));
```

⚠️ **警告**：此方案存在安全风险，仅用于紧急测试，不可用于生产环境！

### 方案2：服务器端代理

在前端服务器配置代理，将API请求转发到后端：

```nginx
location /api {
    proxy_pass https://jmnode.13jue.com;
}
```

## 📝 部署后验证步骤

1. **重启服务**：确保所有代码更改生效
2. **清除缓存**：清除浏览器和CDN缓存
3. **功能测试**：完整测试表单提交流程
4. **日志检查**：查看服务器日志确认无错误
5. **监控告警**：设置CORS错误监控

---

**注意**：部署完成后，请立即测试表单提交功能，确保CORS问题已完全解决。