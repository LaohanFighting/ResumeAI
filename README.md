# ResumeAI - AI-Powered Resume & Cover Letter Generator

Tailor your resume and cover letter for each job application in minutes. Used by real job seekers who want better results.

## ✨ Features

- 🎯 **Tailored for each job** - Customizes resume based on specific job requirements
- 📝 **Resume + Cover Letter** - Generates both in one go
- ⚡ **Fast & Simple** - Get results in minutes
- 💰 **Free to try** - 1 free generation, no credit card required
- 🔒 **Privacy-focused** - Simple email login, no complex accounts

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure environment variables:**
Create `backend/.env`:
```env
OPENAI_API_KEY=sk-proj-your_openai_api_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret
```

3. **Start backend:**
```bash
python backend/main.py
```

4. **Start frontend:**
```bash
cd frontend
python -m http.server 8080
```

5. **Open browser:**
Visit `http://localhost:8080`

### Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed Railway deployment guide.

**Quick deploy to Railway:**
1. Push code to GitHub
2. Connect Railway to your repo
3. Add environment variables in Railway dashboard
4. Deploy!

## 📁 Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI app with routes
│   ├── ai.py                # OpenAI integration
│   ├── auth.py              # User authentication (in-memory)
│   ├── stripe_handler.py   # Stripe payment processing
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── landing.html         # Landing page
│   ├── index.html           # Main app page
│   ├── share.html           # Share page
│   ├── style.css            # Styles
│   └── script.js            # Frontend logic
├── Dockerfile               # Docker config for deployment
├── railway.toml            # Railway deployment config
└── DEPLOYMENT.md           # Deployment guide
```

## 🎯 How It Works

1. **Paste Job Description** - Copy the job posting
2. **Paste Your Background** - Share your experience and skills
3. **Get Tailored Resume & Cover Letter** - Receive customized documents ready to submit

## 💰 Pricing

- **Free**: 1 generation (no credit card)
- **Pro**: $9.9/month for 100 generations

## 🚀 Launch & Growth

### Reddit Launch

**Best Subreddits:**
- r/jobs
- r/resumes
- r/careeradvice

**Title Examples:**
1. "I built an AI tool that tailors your resume for each job application - free to try"
2. "Tired of sending the same resume everywhere? This AI customizes it for each job"
3. "I used AI to tailor my resume for job applications - sharing the tool I built"

**Post Template:**
```
Hey r/jobs,

I've been job searching and got tired of manually tailoring my resume for each application. So I built a simple AI tool that does it automatically.

**How it works:**
1. Paste the job description
2. Paste your background/experience
3. Get a tailored resume and cover letter

**Why I'm sharing:**
- It's free to try (1 generation)
- No signup required for the free version
- I've been using it myself and it's helped me get more interviews

Link: [your-domain.com]

Would love feedback if you try it!
```

See [LAUNCH_GUIDE.md](./LAUNCH_GUIDE.md) for complete launch strategy.

### Product Hunt Launch

**Best Time:** Tuesday-Thursday, 00:01 PST

**Key Info:**
- **Name:** ResumeAI - Tailor Your Resume for Every Job
- **Tagline:** AI-powered tool that customizes your resume and cover letter for each job application
- **Category:** Productivity / Developer Tools

See [LAUNCH_GUIDE.md](./LAUNCH_GUIDE.md) for Product Hunt launch details.

## 🔧 API Endpoints

- `GET /` - Landing page
- `GET /app` - Main application
- `GET /share` - Share page
- `POST /login` - User login
- `GET /auth/me` - Get user info
- `POST /generate` - Generate resume & cover letter
- `POST /create-checkout-session` - Create Stripe checkout
- `POST /stripe-webhook` - Stripe webhook handler

## 🛠️ Tech Stack

- **Backend:** Python + FastAPI
- **Frontend:** HTML + CSS + JavaScript (vanilla)
- **AI:** OpenAI GPT-4o-mini
- **Payments:** Stripe Checkout
- **Deployment:** Railway (Docker)

## 📚 Documentation

- [Deployment Guide](./DEPLOYMENT.md) - Deploy to Railway
- [Launch Guide](./LAUNCH_GUIDE.md) - Reddit & Product Hunt launch
- [Stripe Setup](./Stripe支付配置指南.md) - Payment configuration
- [Paid MVP Setup](./PAID_MVP_SETUP.md) - Complete setup guide

## 🎯 Roadmap

- [ ] Database integration (Supabase)
- [ ] Email notifications
- [ ] Resume templates
- [ ] Export to PDF
- [ ] Multi-language support

## 📝 License

MIT License

## 🙏 Credits

Built with ❤️ for job seekers who deserve better tools.

---

**Ready to launch? Check [DEPLOYMENT.md](./DEPLOYMENT.md) to deploy in 30 minutes!**
