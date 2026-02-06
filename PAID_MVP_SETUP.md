# 付费MVP版本设置指南

本文档说明如何设置和运行升级后的AI简历生成网站（付费MVP版本）。

## 📋 新增功能

1. **用户登录系统**：使用邮箱登录（简化版）
2. **使用次数限制**：免费用户1次，Pro用户100次/月
3. **Stripe支付集成**：$9.9/月订阅

## 🚀 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

新增依赖：
- `stripe` - Stripe支付SDK
- `email-validator` - 邮箱验证

### 2. 配置环境变量

编辑 `backend/.env` 文件，添加以下配置：

```env
# OpenAI API密钥
OPENAI_API_KEY=sk-proj-your_openai_api_key

# Stripe配置（测试模式）
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# 可选：如果已在Stripe创建了Price，可以设置
# STRIPE_PRICE_ID=price_xxxxxxxxxxxxx
```

### 3. 获取Stripe测试密钥

1. 访问 [Stripe Dashboard](https://dashboard.stripe.com/test/apikeys)
2. 登录或注册账号（免费）
3. 复制 **Secret key**（格式：`sk_test_...`）
4. 保存到 `.env` 文件的 `STRIPE_SECRET_KEY`

### 4. 设置Stripe Webhook（本地测试）

#### 方法1：使用Stripe CLI（推荐）

1. 安装 [Stripe CLI](https://stripe.com/docs/stripe-cli)

2. 登录Stripe CLI：
```bash
stripe login
```

3. 转发webhook到本地服务器：
```bash
stripe listen --forward-to localhost:8000/stripe-webhook
```

4. 复制输出的 **webhook signing secret**（格式：`whsec_...`）
5. 保存到 `.env` 文件的 `STRIPE_WEBHOOK_SECRET`

#### 方法2：使用ngrok（生产环境）

1. 安装 [ngrok](https://ngrok.com/)
2. 启动隧道：
```bash
ngrok http 8000
```
3. 在Stripe Dashboard中配置Webhook：
   - URL: `https://your-ngrok-url.ngrok.io/stripe-webhook`
   - Events: `checkout.session.completed`, `invoice.payment_succeeded`
4. 复制Webhook signing secret到 `.env`

### 5. 启动后端服务器

```bash
python backend/main.py
```

服务器将在 `http://localhost:8000` 运行

### 6. 启动前端服务器

```bash
cd frontend
python -m http.server 8080
```

前端将在 `http://localhost:8080/index.html` 运行

## 🧪 测试流程

### 1. 测试登录

1. 打开前端页面
2. 输入邮箱（如：`test@example.com`）
3. 点击 "Continue"
4. 应该看到用户信息显示在顶部

### 2. 测试生成（免费用户）

1. 登录后，填写表单
2. 点击 "Generate Resume & Cover Letter"
3. 成功生成后，剩余次数应该变为 0
4. 再次尝试生成，应该看到升级提示

### 3. 测试支付流程

#### 使用Stripe测试卡号：

- **卡号**：`4242 4242 4242 4242`
- **有效期**：任意未来日期（如：12/25）
- **CVC**：任意3位数字（如：123）
- **邮编**：任意5位数字（如：12345）

#### 测试步骤：

1. 当剩余次数为0时，点击 "Upgrade to Pro"
2. 跳转到Stripe Checkout页面
3. 使用测试卡号完成支付
4. 支付成功后，自动跳转回网站
5. 刷新页面，应该看到剩余次数变为100

### 4. 测试Webhook

确保Stripe CLI正在运行：
```bash
stripe listen --forward-to localhost:8000/stripe-webhook
```

支付成功后，在CLI中应该看到webhook事件被转发。

## 📁 项目结构

```
.
├── backend/
│   ├── main.py              # FastAPI主文件（已更新）
│   ├── ai.py                # AI生成逻辑（未修改）
│   ├── auth.py              # 用户认证模块（新增）
│   ├── stripe_handler.py    # Stripe支付处理（新增）
│   ├── requirements.txt     # Python依赖（已更新）
│   └── .env                 # 环境变量配置
├── frontend/
│   ├── index.html           # 前端页面（已更新）
│   ├── style.css            # 样式文件（已更新）
│   └── script.js            # JavaScript逻辑（已重写）
└── PAID_MVP_SETUP.md        # 本文档
```

## 🔑 API端点说明

### 用户认证

- `POST /login` - 用户登录（仅需邮箱）
- `GET /auth/me` - 获取当前用户信息

### 生成功能

- `POST /generate` - 生成简历和求职信（需要登录）

### 支付功能

- `POST /create-checkout-session` - 创建Stripe支付会话
- `POST /stripe-webhook` - 处理Stripe Webhook事件

## 💡 关键逻辑说明

### 用户系统

- **存储方式**：内存字典（`backend/auth.py`）
- **免费用户**：默认1次使用
- **Pro用户**：支付后获得100次/月
- **Session管理**：使用token存储在内存中

### 次数限制

- 每次调用 `/generate` 前检查剩余次数
- 次数为0时返回402错误（Payment Required）
- 生成成功后扣除1次

### 支付流程

1. 用户点击 "Upgrade to Pro"
2. 前端调用 `/create-checkout-session`
3. 跳转到Stripe Checkout
4. 用户完成支付
5. Stripe发送webhook到 `/stripe-webhook`
6. 后端验证签名并给用户增加100次

## 🚨 注意事项

### 开发环境

1. **用户数据**：使用内存存储，重启服务器后数据会丢失
2. **Session**：同样存储在内存中，重启后需要重新登录
3. **Stripe**：使用测试模式，不会产生真实费用

### 生产环境建议

1. **数据库**：切换到Supabase或PostgreSQL存储用户数据
2. **Session**：使用Redis或数据库存储
3. **Stripe**：切换到生产模式，使用真实密钥
4. **Webhook**：配置真实的webhook URL
5. **CORS**：限制允许的域名
6. **错误处理**：添加更完善的错误日志和监控

## 🔧 故障排除

### 问题1：登录后无法生成

**原因**：Session token未正确传递

**解决**：检查浏览器控制台，确保请求头包含 `X-Session-Token`

### 问题2：支付后次数未增加

**原因**：Webhook未正确配置或签名验证失败

**解决**：
1. 检查Stripe CLI是否运行
2. 检查 `.env` 中的 `STRIPE_WEBHOOK_SECRET` 是否正确
3. 查看后端日志，检查webhook事件是否收到

### 问题3：Stripe Checkout页面无法打开

**原因**：Stripe密钥配置错误

**解决**：
1. 检查 `.env` 中的 `STRIPE_SECRET_KEY` 是否正确
2. 确保使用测试模式的密钥（`sk_test_...`）

## 📚 相关资源

- [Stripe文档](https://stripe.com/docs)
- [Stripe测试卡号](https://stripe.com/docs/testing)
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [OpenAI API文档](https://platform.openai.com/docs)

## ✅ 检查清单

- [ ] 安装所有依赖
- [ ] 配置 `.env` 文件（OpenAI + Stripe）
- [ ] 安装并配置Stripe CLI
- [ ] 启动后端服务器
- [ ] 启动前端服务器
- [ ] 测试登录功能
- [ ] 测试生成功能
- [ ] 测试支付流程
- [ ] 验证Webhook接收

## 🎯 下一步

1. **添加数据库**：替换内存存储
2. **邮件通知**：支付成功通知
3. **使用统计**：记录生成历史
4. **管理后台**：查看用户和订单
5. **订阅管理**：允许用户取消订阅

---

**祝使用愉快！如有问题，请查看代码注释或相关文档。**
