# Stripe支付功能配置指南

## 📋 前置准备

1. **Stripe账号**：注册一个Stripe账号（免费）
2. **测试环境**：使用Stripe测试模式（不会产生真实费用）
3. **Stripe CLI**：用于本地测试Webhook（可选但推荐）

---

## 🚀 快速开始（3步）

### 步骤1：获取Stripe测试密钥

1. 访问 [Stripe Dashboard](https://dashboard.stripe.com/test/apikeys)
2. 登录或注册账号（免费）
3. 复制 **Secret key**（格式：`sk_test_...`）
   - 注意：使用**测试模式**（Test mode），不是生产模式（Live mode）

### 步骤2：配置环境变量

编辑 `backend/.env` 文件，添加Stripe配置：

```env
# OpenAI API密钥（已有）
OPENAI_API_KEY=sk-proj-your_openai_api_key

# Stripe配置（新增）
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

**重要：**
- `STRIPE_SECRET_KEY`：从Stripe Dashboard复制
- `STRIPE_WEBHOOK_SECRET`：需要设置Webhook后获取（见步骤3）

### 步骤3：设置Stripe Webhook（本地测试）

#### 方法1：使用Stripe CLI（推荐）

**安装Stripe CLI：**
1. 下载：https://stripe.com/docs/stripe-cli
2. 安装后，在终端运行：
   ```bash
   stripe login
   ```

**转发Webhook到本地服务器：**
```bash
stripe listen --forward-to localhost:8000/stripe-webhook
```

**复制Webhook Secret：**
- 运行上述命令后，会显示类似：
  ```
  > Ready! Your webhook signing secret is whsec_xxxxxxxxxxxxx
  ```
- 复制这个 `whsec_...` 值
- 添加到 `.env` 文件的 `STRIPE_WEBHOOK_SECRET`

**保持这个终端窗口打开**，Webhook会实时转发到你的服务器。

#### 方法2：使用ngrok（生产环境）

1. 安装 [ngrok](https://ngrok.com/)
2. 启动隧道：
   ```bash
   ngrok http 8000
   ```
3. 复制ngrok提供的HTTPS URL（例如：`https://abc123.ngrok.io`）
4. 在Stripe Dashboard配置Webhook：
   - 访问：https://dashboard.stripe.com/test/webhooks
   - 点击 "Add endpoint"
   - Endpoint URL: `https://your-ngrok-url.ngrok.io/stripe-webhook`
   - Events to send: 选择 `checkout.session.completed` 和 `invoice.payment_succeeded`
   - 点击 "Add endpoint"
5. 复制Webhook signing secret到 `.env` 文件

---

## 🧪 测试支付流程

### 使用Stripe测试卡号

**测试卡号：**
- **卡号**：`4242 4242 4242 4242`
- **有效期**：任意未来日期（如：12/25）
- **CVC**：任意3位数字（如：123）
- **邮编**：任意5位数字（如：12345）

**其他测试卡号：**
- 需要3D验证：`4000 0025 0000 3155`
- 拒绝卡：`4000 0000 0000 0002`
- 更多测试卡：https://stripe.com/docs/testing

### 完整测试流程

1. **确保服务器运行**
   - 后端：`python backend\main.py`
   - 前端：`python -m http.server 8080`（在frontend目录）
   - Webhook：`stripe listen --forward-to localhost:8000/stripe-webhook`

2. **登录用户**
   - 访问：http://localhost:8080/index.html
   - 输入邮箱登录

3. **使用完免费次数**
   - 生成一次简历（消耗1次免费次数）
   - 剩余次数变为0

4. **点击升级**
   - 页面会显示 "Upgrade to Pro" 按钮
   - 点击按钮

5. **完成支付**
   - 跳转到Stripe Checkout页面
   - 使用测试卡号：`4242 4242 4242 4242`
   - 填写任意未来日期和CVC
   - 点击 "Subscribe"

6. **验证结果**
   - 支付成功后自动跳转回网站
   - 刷新页面
   - 应该看到剩余次数变为100

---

## 📊 支付配置说明

### 当前配置

- **产品名称**：Resume Pro
- **价格**：$9.90/月（订阅模式）
- **Pro用户次数**：100次/月
- **免费用户次数**：1次

### 修改价格或配置

编辑 `backend/stripe_handler.py`：

```python
# 产品配置
PRODUCT_NAME = "Resume Pro"  # 产品名称
PRODUCT_PRICE = 990  # $9.90，单位：分（cents）
CREDITS_PER_MONTH = 100  # Pro用户每月100次
```

**修改价格示例：**
- $19.90/月：`PRODUCT_PRICE = 1990`
- $4.99/月：`PRODUCT_PRICE = 499`

---

## 🔍 验证Webhook是否工作

### 检查Webhook事件

1. **Stripe CLI窗口**应该显示：
   ```
   --> checkout.session.completed [evt_xxxxx]
   <-- [200] POST http://localhost:8000/stripe-webhook
   ```

2. **后端服务器日志**应该显示：
   - Webhook接收成功
   - 用户次数已增加

### 手动测试Webhook

在Stripe CLI窗口运行：
```bash
stripe trigger checkout.session.completed
```

这会发送一个测试事件到你的服务器。

---

## 🚨 常见问题

### Q1: Webhook签名验证失败

**原因**：`STRIPE_WEBHOOK_SECRET` 不正确

**解决**：
1. 确保使用最新的webhook secret
2. 如果使用Stripe CLI，每次运行 `stripe listen` 都会生成新的secret
3. 更新 `.env` 文件中的 `STRIPE_WEBHOOK_SECRET`

### Q2: 支付后次数未增加

**检查清单：**
1. ✅ Webhook是否正在运行（Stripe CLI窗口）
2. ✅ `STRIPE_WEBHOOK_SECRET` 是否正确
3. ✅ 后端服务器是否正常运行
4. ✅ 查看后端服务器日志是否有错误

### Q3: Checkout页面无法打开

**原因**：`STRIPE_SECRET_KEY` 配置错误或未设置

**解决**：
1. 检查 `.env` 文件中的 `STRIPE_SECRET_KEY`
2. 确保使用测试模式的密钥（`sk_test_...`）
3. 重启后端服务器

### Q4: 如何查看支付记录

访问 [Stripe Dashboard - Payments](https://dashboard.stripe.com/test/payments)
- 可以看到所有测试支付记录
- 可以查看支付详情和状态

---

## 🔐 生产环境部署

### 切换到生产模式

1. **获取生产密钥**
   - 在Stripe Dashboard切换到 "Live mode"
   - 复制生产环境的 Secret key（格式：`sk_live_...`）

2. **更新环境变量**
   ```env
   STRIPE_SECRET_KEY=sk_live_your_production_key
   ```

3. **配置生产Webhook**
   - 使用真实的域名（不是localhost）
   - 在Stripe Dashboard配置Webhook URL
   - 获取生产环境的Webhook secret

4. **安全建议**
   - 使用HTTPS
   - 限制CORS域名
   - 设置使用限额
   - 监控支付异常

---

## 📝 检查清单

配置Stripe前，确保：

- [ ] Stripe账号已注册
- [ ] 已获取测试Secret key
- [ ] 已安装Stripe CLI（用于本地测试）
- [ ] `.env` 文件已配置 `STRIPE_SECRET_KEY`
- [ ] Webhook已设置并获取了 `STRIPE_WEBHOOK_SECRET`
- [ ] 后端服务器已重启（加载新环境变量）
- [ ] 测试支付流程成功

---

## 🎯 下一步

配置完成后：

1. **测试支付流程**：使用测试卡号完成一次支付
2. **验证次数增加**：确认用户次数从0变为100
3. **查看支付记录**：在Stripe Dashboard查看测试支付
4. **准备上线**：测试完成后，可以切换到生产模式

---

## 📚 相关资源

- [Stripe文档](https://stripe.com/docs)
- [Stripe测试卡号](https://stripe.com/docs/testing)
- [Stripe CLI文档](https://stripe.com/docs/stripe-cli)
- [Webhook最佳实践](https://stripe.com/docs/webhooks/best-practices)

---

**祝配置顺利！如有问题，请查看后端服务器日志或Stripe Dashboard。**
