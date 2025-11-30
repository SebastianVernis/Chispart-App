# Render Deployment - Chispart AI

## Quick Deploy to Render

### Method 1: Blueprint (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "feat: add Render deployment configuration"
   git push origin main
   ```

2. **Deploy via Render Dashboard**
   - Go to https://dashboard.render.com
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select branch: `main`
   - Render will read `render.yaml` automatically

3. **Set Environment Variable**
   - In Render dashboard, go to your service
   - Navigate to "Environment"
   - Add: `BLACKBOX_API_KEY` = `<your_api_key>`
   - Click "Save Changes"

### Method 2: Manual Setup

1. **Create Web Service**
   - Go to https://dashboard.render.com
   - Click "New" → "Web Service"
   - Connect repository

2. **Configure Service**
   - **Name**: `chispart-ai`
   - **Region**: Oregon (US West)
   - **Branch**: `main`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**
   ```
   PYTHON_VERSION=3.11.0
   BLACKBOX_API_KEY=<your_key>
   CONFIG_FILE=config/models.json
   LOG_LEVEL=INFO
   PYTHONUNBUFFERED=true
   APP_NAME=Chispart AI
   ```

4. **Advanced Settings**
   - **Health Check Path**: `/health`
   - **Auto-Deploy**: Yes

## Post-Deployment

### Verify Deployment
```bash
# Check health
curl https://your-app.onrender.com/health

# View API docs
open https://your-app.onrender.com/docs

# Test endpoint
curl https://your-app.onrender.com/
```

### Monitor Logs
- Go to Render dashboard → Your service → Logs
- Watch for any errors or warnings

### Test API
```bash
# Get models list
curl https://your-app.onrender.com/models

# Chat endpoint
curl -X POST https://your-app.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Hello, world!",
    "model": "blackboxai/google/gemma-2-9b-it:free"
  }'
```

## Troubleshooting

### Build Fails
- Check `requirements.txt` has all dependencies
- Verify Python version compatibility
- Check logs in Render dashboard

### Service Won't Start
- Ensure `BLACKBOX_API_KEY` is set
- Check port binding (use `$PORT` not hardcoded)
- Verify `uvicorn` is in requirements.txt

### API Errors
- Check logs for Python exceptions
- Verify API key is valid
- Check model names in `config/models.json`

## Performance Tips

1. **Keep Service Warm**: Free tier sleeps after 15 min
   - Use UptimeRobot to ping every 14 minutes
   - Or upgrade to paid plan

2. **Enable Caching**: Response caching configured in app

3. **Monitor Usage**: Check Render metrics dashboard

## Cost

- **Free Tier**: 750 hours/month, 512MB RAM
- **Starter**: $7/month, no sleep, more resources
- **Recommended**: Starter for production

## Support

- Render Docs: https://render.com/docs
- Project Docs: See `AGENTS.md` and `README.md`
