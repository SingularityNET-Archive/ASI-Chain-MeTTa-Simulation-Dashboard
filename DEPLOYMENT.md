# 🚀 Deployment Guide - Streamlit Community Cloud

This guide walks you through deploying the ASI Chain Agent Simulation Dashboard to **Streamlit Community Cloud** for free, persistent hosting.

## 📋 Prerequisites

1. **GitHub Account** - [Sign up here](https://github.com/signup) if you don't have one
2. **Streamlit Account** - [Sign up here](https://share.streamlit.io/signup) (can use GitHub to sign in)
3. **Your code in a GitHub repository** - Follow the steps below

## 🎯 Step 1: Push Your Code to GitHub

### Option A: Using the Command Line

```bash
# Navigate to your project directory
cd /Users/stephen/Documents/GitHub/ASI-Chain-MeTTa-Simulation-Dashboard

# Initialize git if not already done
git init

# Add all files
git add .

# Commit the files
git commit -m "Initial commit: ASI Chain Agent Simulation Dashboard"

# Create a new repository on GitHub (via browser)
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/ASI-Chain-MeTTa-Simulation-Dashboard.git
git branch -M main
git push -u origin main
```

### Option B: Using GitHub Desktop

1. Open GitHub Desktop
2. File → Add Local Repository
3. Select your project folder
4. Click "Publish repository"
5. Choose a name and make it public or private
6. Click "Publish Repository"

## 🌐 Step 2: Deploy to Streamlit Cloud

### Via Streamlit Website

1. Go to [share.streamlit.io](https://share.streamlit.io/)

2. Click **"New app"** or **"Deploy an app"**

3. Fill in the deployment form:
   - **Repository**: `YOUR_USERNAME/ASI-Chain-MeTTa-Simulation-Dashboard`
   - **Branch**: `main`
   - **Main file path**: `app.py`

4. Click **"Deploy!"**

5. Wait 2-5 minutes for deployment (watch the logs)

6. Your app will be live at: `https://YOUR_USERNAME-asi-chain-metta-simulation-dashboard.streamlit.app`

## ⚙️ Step 3: Configuration (Already Set Up!)

The following files are already configured for cloud deployment:

### ✅ `requirements.txt`
Contains all Python dependencies (NetworkX, PyVis, Streamlit, etc.)

### ✅ `.streamlit/config.toml`
Theme and server configuration for Streamlit Cloud

### ✅ `packages.txt`
System dependencies (empty for simplified version)

### ✅ Code automatically uses simplified version
The app will use `agent_sim_simple.py` (no hyperon compilation needed)

## 🔧 Advanced: Using Full Hyperon Version

If you want to use the full hyperon/MeTTa version in the cloud:

1. **Install Conan in cloud** - Add to `packages.txt`:
   ```
   build-essential
   cmake
   ```

2. **Uncomment hyperon in requirements.txt**:
   ```
   git+https://github.com/trueagi-io/hyperon-experimental.git#subdirectory=python
   ```

3. **Note**: This will increase deployment time to 10-15 minutes

## 📊 Managing Your Deployed App

### View Your App
- Go to [share.streamlit.io](https://share.streamlit.io/)
- Click on your app to see details
- View logs, usage, and settings

### Update Your App
Any time you push changes to GitHub, Streamlit will automatically redeploy:

```bash
git add .
git commit -m "Updated simulation logic"
git push
```

Streamlit detects the push and redeploys automatically!

### App Settings
In Streamlit Cloud dashboard:
- **Reboot app** - Restart the application
- **Delete app** - Remove the deployment
- **View logs** - Debug issues
- **Secrets** - Add environment variables (if needed)

## 🌟 Free Tier Limits

Streamlit Community Cloud free tier includes:
- ✅ Unlimited public apps
- ✅ 1 GB RAM per app
- ✅ CPU sharing (sufficient for this app)
- ✅ Automatic SSL (HTTPS)
- ✅ Custom subdomain
- ✅ GitHub integration

**This app fits well within free tier limits!**

## 🔗 Sharing Your App

Once deployed, share your app:
- **URL**: `https://your-app-name.streamlit.app`
- **Embed**: Use iframe in websites
- **Social**: Share on Twitter, LinkedIn, etc.

## 🐛 Troubleshooting

### Deployment Failed
- Check logs in Streamlit Cloud dashboard
- Ensure `requirements.txt` is correct
- Verify `app.py` runs locally first

### App is Slow
- Reduce default number of agents
- Increase step delay
- Consider optimizing PyVis rendering

### Import Errors
- Make sure all files are committed to GitHub
- Check that `agent_sim_simple.py` and `visualizer.py` are in repo
- Verify requirements.txt has all dependencies

### App Goes to Sleep
- Free tier apps sleep after inactivity
- They wake up when someone visits (takes a few seconds)
- This is normal for free hosting

## 🎉 Success Checklist

- [ ] Code pushed to GitHub repository
- [ ] App deployed on Streamlit Cloud
- [ ] App is accessible via public URL
- [ ] Simulation runs without errors
- [ ] Graph visualizations render correctly
- [ ] All controls work (Run, Stop, Reset)

## 📚 Additional Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Forum](https://discuss.streamlit.io/)

## 💡 Alternative Hosting Options

If you need more resources or features:

### Hugging Face Spaces
- Similar free tier
- Good for ML apps
- Easy GitHub integration

### Heroku
- More control
- Paid tier available
- Requires Procfile

### AWS/GCP/Azure
- Full cloud platforms
- More complex setup
- Pay-as-you-go pricing

### Self-Hosted
- Full control
- Use your own server
- Run: `streamlit run app.py --server.port 80`

---

**Need Help?** Open an issue on GitHub or check Streamlit's community forum!

**Good Luck with Your Deployment!** 🚀

