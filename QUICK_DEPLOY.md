# 快速部署指南 - 30分钟上线

> 💡 **需要更详细的说明？** 查看 [DEPLOYMENT_DETAILED.md](./DEPLOYMENT_DETAILED.md) 获取完整步骤、截图说明和详细故障排查。

## 🎯 目标

30分钟内将ResumeAI部署到Railway，让网站可以在公网访问。

---

## 📋 前置检查清单

- [ ] Railway账号已注册（https://railway.app）
- [ ] GitHub账号（用于代码仓库）
- [ ] OpenAI API密钥已准备好
- [ ] Stripe测试密钥已准备好
- [ ] 代码已推送到GitHub（或准备推送）

---

## 🚀 部署步骤（30分钟）

### 步骤1：准备代码（5分钟）

**1.1 检查关键文件：**
- ✅ `Dockerfile` 存在
- ✅ `railway.toml` 存在
- ✅ `.gitignore` 包含 `.env`

**1.2 提交代码到GitHub：**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

**详细说明：** 查看 [DEPLOYMENT_DETAILED.md - 步骤1](./DEPLOYMENT_DETAILED.md#步骤1准备代码仓库)

---

### 步骤2：创建Railway项目（10分钟）

**2.1 登录Railway：**
1. 访问 https://railway.app
2. 点击 "Login with GitHub"
3. 授权Railway访问GitHub

**2.2 创建新项目：**
1. 点击 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 选择你的仓库（`resumeai`）
4. Railway自动检测Dockerfile并开始构建

**2.3 等待构建完成：**
- 通常需要2-5分钟
- 查看 "Deployments" 标签页的进度
- 构建完成后会显示域名

**详细说明：** 查看 [DEPLOYMENT_DETAILED.md - 步骤2](./DEPLOYMENT_DETAILED.md#步骤2创建railway账号和项目)

---

### 步骤3：配置环境变量（5分钟）

**3.1 添加环境变量：**
1. 在Railway项目页面，点击 "Variables" 标签
2. 添加以下变量：

```
OPENAI_API_KEY=sk-proj-your_actual_key
STRIPE_SECRET_KEY=sk_test_your_actual_key
```

**3.2 获取密钥：**
- OpenAI: https://platform.openai.com/api-keys
- Stripe: https://dashboard.stripe.com/test/apikeys

**详细说明：** 查看 [DEPLOYMENT_DETAILED.md - 步骤3](./DEPLOYMENT_DETAILED.md#步骤3配置环境变量)

---

### 步骤4：配置Stripe Webhook（5分钟）

**4.1 获取Railway域名：**
- 在Railway项目页面查看域名（如：`yourproject-production.up.railway.app`）

**4.2 配置Webhook：**
1. 访问：https://dashboard.stripe.com/webhooks
2. 点击 "Add endpoint"
3. Endpoint URL: `https://yourproject-production.up.railway.app/stripe-webhook`
4. 选择事件：`checkout.session.completed`, `invoice.payment_succeeded`
5. 点击 "Add endpoint"

**4.3 添加Webhook Secret：**
1. 复制Webhook signing secret（格式：`whsec_...`）
2. 在Railway添加环境变量：
   - Name: `STRIPE_WEBHOOK_SECRET`
   - Value: `whsec_your_secret`

**详细说明：** 查看 [DEPLOYMENT_DETAILED.md - 步骤4](./DEPLOYMENT_DETAILED.md#步骤4配置stripe-webhook)

---

### 步骤5：测试部署（5分钟）

**5.1 测试页面：**
- [ ] 访问 `/` 看到Landing Page
- [ ] 访问 `/app` 看到应用页面
- [ ] 访问 `/share` 看到分享页面

**5.2 测试功能：**
- [ ] 登录功能正常
- [ ] 生成功能正常
- [ ] 支付功能正常（测试卡号：`4242 4242 4242 4242`）
- [ ] 支付后次数增加

**详细说明：** 查看 [DEPLOYMENT_DETAILED.md - 步骤5](./DEPLOYMENT_DETAILED.md#步骤5测试部署)

---

## ✅ 部署后检查清单

- [ ] Landing Page (`/`) 可以访问
- [ ] 应用页面 (`/app`) 可以访问
- [ ] 分享页面 (`/share`) 可以访问
- [ ] 登录功能正常
- [ ] 生成功能正常
- [ ] 支付功能正常（使用测试卡号）
- [ ] Webhook配置正确
- [ ] 品牌标识显示正常

---

## 🔧 常见问题快速解决

### Q1: 部署失败
**解决：** 查看Railway日志，检查Dockerfile语法和环境变量

### Q2: 网站显示404
**解决：** 检查静态文件路径和路由配置

### Q3: API调用失败
**解决：** 检查环境变量和CORS配置

### Q4: 支付后次数未增加
**解决：** 检查Stripe Webhook配置和Railway日志

**详细故障排查：** 查看 [DEPLOYMENT_DETAILED.md - 故障排查](./DEPLOYMENT_DETAILED.md#故障排查)

---

## 📝 下一步

部署完成后：
1. ✅ 完成所有测试
2. ✅ 分享网站链接
3. ✅ 在Reddit/Product Hunt发布
4. ✅ 开始获客！

**详细发布指南：** [LAUNCH_GUIDE.md](./LAUNCH_GUIDE.md)

---

## 📚 相关文档

- **详细部署指南：** [DEPLOYMENT_DETAILED.md](./DEPLOYMENT_DETAILED.md) - 完整步骤、截图说明、详细故障排查
- **发布指南：** [LAUNCH_GUIDE.md](./LAUNCH_GUIDE.md) - Reddit和Product Hunt发布策略
- **上线检查清单：** [上线检查清单.md](./上线检查清单.md)

---

**现在就开始部署吧！30分钟后你的网站就可以上线了！** 🚀
