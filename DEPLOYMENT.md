# 部署指南 - 30分钟上线

本指南将帮助你将ResumeAI部署到Railway，让网站可以在公网访问。

---

## 📋 前置准备

1. **Railway账号**：访问 https://railway.app 注册（免费）
2. **GitHub账号**：用于代码仓库（可选，Railway支持直接部署）
3. **Stripe账号**：已配置测试密钥
4. **OpenAI API密钥**：已准备好

---

## 🚀 部署步骤（Railway）

### 步骤1：准备代码仓库

**选项A：使用GitHub（推荐）**

1. 在GitHub创建新仓库
2. 推送代码：
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/resumeai.git
git push -u origin main
```

**选项B：直接部署（无需GitHub）**

- Railway支持直接从本地文件夹部署

### 步骤2：创建Railway项目

1. 访问 https://railway.app
2. 点击 "New Project"
3. 选择 "Deploy from GitHub repo"（如果使用GitHub）
   - 或选择 "Empty Project"（如果直接部署）

### 步骤3：配置部署

1. **如果使用GitHub**：
   - 连接GitHub账号
   - 选择你的仓库
   - Railway会自动检测Dockerfile

2. **如果直接部署**：
   - 点击 "Add Service" → "GitHub Repo"
   - 或使用Railway CLI：
   ```bash
   npm i -g @railway/cli
   railway login
   railway init
   railway up
   ```

### 步骤4：配置环境变量

在Railway项目设置中，添加以下环境变量：

1. 进入项目 → Settings → Variables
2. 添加以下变量：

```
OPENAI_API_KEY=sk-proj-your_openai_api_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

**重要：**
- 使用**生产环境**的Stripe密钥（如果已切换）
- 或继续使用测试密钥进行测试

### 步骤5：配置Webhook（生产环境）

1. **获取Railway域名**：
   - Railway会自动分配一个域名（如：`yourproject.railway.app`）
   - 或配置自定义域名

2. **在Stripe Dashboard配置Webhook**：
   - 访问：https://dashboard.stripe.com/webhooks
   - 点击 "Add endpoint"
   - Endpoint URL: `https://yourproject.railway.app/stripe-webhook`
   - Events: 选择 `checkout.session.completed` 和 `invoice.payment_succeeded`
   - 复制Webhook signing secret
   - 更新Railway环境变量：`STRIPE_WEBHOOK_SECRET`

### 步骤6：部署

1. Railway会自动开始构建和部署
2. 等待部署完成（通常2-5分钟）
3. 点击生成的域名访问网站

---

## ✅ 部署后检查清单

- [ ] 网站可以访问（打开Railway提供的域名）
- [ ] Landing Page显示正常（`/`）
- [ ] 应用页面可以访问（`/app`）
- [ ] 登录功能正常
- [ ] 生成功能正常
- [ ] 支付功能正常（使用测试卡号）
- [ ] Webhook正常工作（检查Stripe Dashboard）

---

## 🔧 故障排查

### 问题1：部署失败

**检查：**
- Dockerfile语法是否正确
- 环境变量是否都已设置
- Railway日志中的错误信息

### 问题2：网站无法访问

**检查：**
- Railway服务是否运行中
- 域名是否正确
- 端口配置是否正确

### 问题3：API调用失败

**检查：**
- 环境变量是否正确设置
- CORS配置是否正确
- 浏览器控制台错误信息

### 问题4：支付后次数未增加

**检查：**
- Stripe Webhook是否配置正确
- Webhook URL是否可访问
- Railway日志中是否有Webhook事件

---

## 🌐 自定义域名（可选）

1. 在Railway项目设置中，点击 "Settings" → "Domains"
2. 添加自定义域名
3. 按照提示配置DNS记录
4. 更新Stripe Webhook URL为新域名

---

## 📊 监控和日志

- **查看日志**：Railway Dashboard → Deployments → 点击最新部署 → Logs
- **监控指标**：Railway会自动显示CPU、内存使用情况
- **错误追踪**：查看日志中的错误信息

---

## 💰 成本估算

**Railway免费额度：**
- $5/月免费额度
- 足够支持小规模使用

**预计成本：**
- Railway：免费（小规模）
- OpenAI API：按使用量付费（约$0.01-0.02/次生成）
- Stripe：2.9% + $0.30/交易（仅成功交易收费）

---

## 🎯 下一步

部署完成后：
1. 测试所有功能
2. 分享网站链接
3. 在Reddit/Product Hunt发布
4. 开始获客！

---

**部署完成后，你的网站就可以在公网访问了！** 🎉
