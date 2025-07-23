# 🚀 Render Deployment Guide

## ✅ Fixed Issues

### 1. **Requirements.txt Fixed**
- ❌ Removed `llama-index-tools-query-engine` (doesn't exist)
- ✅ Added proper version constraints
- ✅ Organized dependencies by category
- ✅ Added comments for clarity

### 2. **Docker Optimization**
- ✅ Added `.dockerignore` to reduce build context
- ✅ Dockerfile already optimized for Render
- ✅ Proper port configuration with `${PORT:-8000}`

## 🔧 Environment Variables for Render

Set these in your Render dashboard:

```bash
# Required API Keys
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=zhoop

# Optional: Indian Kanoon API (for Grid 5 live cases)
INDIAN_KANOON_API_TOKEN=your_indian_kanoon_token

# CORS Configuration (Production)
CORS_ALLOW_ALL=false
CORS_ORIGINS=https://your-nextjs-frontend.vercel.app,https://yourdomain.com

# Optional: Custom settings
PORT=8000
```

## 📦 Deployment Steps

### 1. **Push to GitHub**
```bash
git add .
git commit -m "Fix Docker build - remove invalid llama-index package"
git push origin main
```

### 2. **Render Configuration**
- **Build Command**: `docker build -t app .`
- **Start Command**: `docker run -p $PORT:$PORT app`
- **Environment**: Docker
- **Auto-Deploy**: Yes (from GitHub)

### 3. **Health Check**
Your API will be available at: `https://your-app-name.onrender.com`

Test endpoints:
- `GET /` - Health check
- `GET /health` - Detailed health status
- `POST /dashboard/populate-hierarchical` - Main dashboard endpoint

## 🧪 Testing After Deployment

### 1. **Basic Health Check**
```bash
curl https://your-app-name.onrender.com/health
```

### 2. **Dashboard Test**
```bash
curl -X POST https://your-app-name.onrender.com/dashboard/populate-hierarchical \
  -H "Content-Type: application/json" \
  -d '{
    "case_id": "TEST-001",
    "case_context": "Medical malpractice case involving surgical negligence",
    "additional_context": "Patient harm during surgery"
  }'
```

### 3. **CORS Test (from browser)**
```javascript
fetch('https://your-app-name.onrender.com/health', {
  method: 'GET',
  credentials: 'include'
})
.then(response => response.json())
.then(data => console.log('✅ CORS working:', data))
.catch(error => console.error('❌ CORS error:', error));
```

## 🔍 Troubleshooting

### Common Build Issues

1. **Package Not Found**
   - ✅ Fixed: Removed `llama-index-tools-query-engine`
   - Check requirements.txt for typos

2. **Memory Issues**
   - Render free tier has 512MB RAM limit
   - Consider upgrading to paid plan for production

3. **Build Timeout**
   - Docker builds can take 10-15 minutes
   - This is normal for first deployment

4. **Environment Variables**
   - Ensure all required API keys are set
   - Check for typos in variable names

### Runtime Issues

1. **API Key Errors**
   ```
   KeyError: 'OPENAI_API_KEY'
   ```
   - Set environment variables in Render dashboard

2. **Pinecone Connection**
   ```
   PineconeException: Index 'zhoop' not found
   ```
   - Verify index name and API key

3. **CORS Issues**
   ```
   Access to fetch blocked by CORS policy
   ```
   - Update CORS_ORIGINS with your frontend URL

## 📊 Performance Optimization

### 1. **Cold Start Reduction**
- Render free tier has cold starts (~30s)
- Keep app warm with periodic health checks
- Consider paid plan for instant scaling

### 2. **Memory Usage**
- LlamaIndex can be memory-intensive
- Monitor usage in Render dashboard
- Optimize queries if needed

### 3. **Response Times**
- Hierarchical dashboard: 30-60s (normal)
- Individual grids: 5-15s each
- Indian Kanoon API: 1-3s

## 🎯 Next Steps

1. **Deploy and Test**
   - Push code to GitHub
   - Deploy on Render
   - Test all endpoints

2. **Frontend Integration**
   - Update Next.js API_URL to Render URL
   - Test CORS with actual frontend
   - Monitor performance

3. **Production Hardening**
   - Set CORS_ALLOW_ALL=false
   - Add specific frontend domains
   - Monitor logs and errors

## 🆘 Support

If you encounter issues:
1. Check Render build logs
2. Test locally with Docker: `docker build -t test . && docker run -p 8000:8000 test`
3. Verify environment variables
4. Check API key permissions

Your deployment should now work perfectly! 🚀
