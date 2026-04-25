# Deployment Guide - FRED Economic Dashboard

This guide explains different ways to share your FRED Economic Dashboard with others.

## Table of Contents
1. [Local Network Sharing (Quick & Easy)](#local-network-sharing)
2. [Streamlit Community Cloud (Free & Recommended)](#streamlit-community-cloud)
3. [Other Deployment Options](#other-deployment-options)
4. [API Key Management](#api-key-management)

---

## Local Network Sharing

**Best for:** Sharing with people on the same network (home, office, etc.)

### How it works:
When you run the dashboard, Streamlit provides three URLs:
- **Local URL:** `http://localhost:8501` (only you can access)
- **Network URL:** `http://10.0.0.246:8501` (anyone on your network)
- **External URL:** `http://73.231.5.236:8501` (if your router allows port forwarding)

### Steps:
1. Keep the dashboard running on your computer:
   ```bash
   streamlit run app.py
   ```

2. Share the **Network URL** with others on your network

3. They can access it by opening that URL in their browser

**Limitations:**
- Your computer must stay on and connected
- Only works for people on the same network
- External URL may not work if behind a firewall/NAT

---

## Streamlit Community Cloud

**Best for:** Free public sharing, most reliable, no server maintenance

### Why Streamlit Cloud?
- ✅ **100% Free** for public apps
- ✅ No server maintenance required
- ✅ Automatic updates when you push to GitHub
- ✅ HTTPS and secure by default
- ✅ No need to keep your computer running

### Steps to Deploy:

#### 1. Create a GitHub Account
- Go to [github.com](https://github.com) and sign up (if you don't have an account)

#### 2. Create a New Repository
```bash
# In your terminal, navigate to the dashboard folder
cd "/Users/audrey/Library/Mobile Documents/com~apple~CloudDocs/1. 爱学习/01. MCIT-iCloud/FRED Data Dashboard"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - FRED Economic Dashboard"

# Create a new repository on GitHub (via website)
# Then link it:
git remote add origin https://github.com/YOUR_USERNAME/fred-dashboard.git
git branch -M main
git push -u origin main
```

**IMPORTANT:** Before pushing to GitHub, make sure your API key is NOT in any committed files!

#### 3. Secure Your API Key

**Option A: Use Streamlit Secrets (Recommended for Streamlit Cloud)**

When deploying to Streamlit Cloud, you'll add your API key through their web interface:

1. Go to your app settings on Streamlit Cloud
2. Click "Secrets"
3. Add:
   ```toml
   FRED_API_KEY = "your_api_key_here"
   ```

**Option B: Keep .env.example (For Quick Deployment)**

If you want users to use your API key (be aware of rate limits):
- The `.env.example` file with your API key will work
- Everyone will share the same API key
- FRED allows 120 requests/minute (should be sufficient for most use cases)

#### 4. Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select:
   - **Repository:** your-username/fred-dashboard
   - **Branch:** main
   - **Main file path:** app.py
5. Click "Deploy"

Your dashboard will be live at: `https://your-app-name.streamlit.app`

---

## Other Deployment Options

### 1. Heroku (Free Tier Available)
- Good for: Custom domains, more control
- Requires: Heroku account, Procfile setup
- Guide: [Heroku + Streamlit](https://docs.streamlit.io/knowledge-base/tutorials/deploy/heroku)

### 2. AWS EC2 / Google Cloud / Azure
- Good for: Enterprise deployments, full control
- Requires: Cloud computing knowledge
- Cost: ~$5-20/month for small instance

### 3. Render.com
- Good for: Simple deployments, Docker support
- Free tier available
- Similar to Heroku but more modern

### 4. Docker Container
```dockerfile
# Dockerfile example
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

---

## API Key Management

### Current Setup
The dashboard now automatically loads the API key from `.env.example`:
```python
# In app.py
load_dotenv('.env.example')
api_key = os.getenv('FRED_API_KEY')
```

### Sharing Considerations

**Option 1: Share Your API Key (Easiest)**
- ✅ Pros: Users don't need to get their own key
- ❌ Cons: Shared rate limits (120 requests/minute total)
- Best for: Small teams, personal use

**Option 2: Require User API Keys**
- ✅ Pros: Each user has their own rate limits
- ✅ Pros: More secure, no shared credentials
- ❌ Cons: Users must register for FRED API key
- Best for: Public sharing, large user base

To switch to Option 2, modify `app.py`:
```python
# Remove or comment out:
# load_dotenv('.env.example')

# And keep the text input field always visible
api_key = st.text_input(
    "FRED API Key",
    type="password",
    help="Enter your FRED API key..."
)
```

### FRED API Rate Limits
- **120 requests per minute**
- **Unlimited daily requests**
- If shared with many users, consider having each user get their own key

### Security Best Practices

**DO:**
- ✅ Use environment variables for API keys
- ✅ Add `.env` to `.gitignore` (already done)
- ✅ Use Streamlit Secrets for cloud deployment
- ✅ Monitor API usage

**DON'T:**
- ❌ Commit API keys directly to GitHub
- ❌ Share API keys in public forums
- ❌ Hardcode API keys in source code

---

## Quick Deployment Checklist

For Streamlit Community Cloud (Recommended):

- [ ] Create GitHub account
- [ ] Create new repository
- [ ] Remove API key from `.env.example` (or use Streamlit Secrets)
- [ ] Push code to GitHub
- [ ] Go to [share.streamlit.io](https://share.streamlit.io)
- [ ] Connect GitHub repository
- [ ] Add API key to Streamlit Secrets
- [ ] Deploy!

---

## Monitoring & Maintenance

### Check Usage
Monitor your FRED API usage at: https://fred.stlouisfed.org/docs/api/

### Update Data
The dashboard automatically fetches fresh data on each load. Data is cached for 1 hour.

### Troubleshooting
- **Rate limit exceeded:** Either wait 1 minute or have users get their own API keys
- **App is slow:** Reduce the number of indicators loaded by default
- **Deployment fails:** Check logs in Streamlit Cloud dashboard

---

## Support & Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **FRED API Docs:** https://fred.stlouisfed.org/docs/api/
- **GitHub Help:** https://docs.github.com

---

**Recommended Approach:**

For most users, **Streamlit Community Cloud** is the best option:
1. Free and reliable
2. Easy to set up (5-10 minutes)
3. Automatic HTTPS
4. No maintenance required
5. Easy to update (just push to GitHub)

Share your dashboard URL with anyone, and they can access it instantly!
