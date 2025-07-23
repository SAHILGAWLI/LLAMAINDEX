# CORS Configuration Guide for Next.js + FastAPI

## ✅ Current CORS Setup

Your `query_api.py` now has production-ready CORS configuration that's fully compatible with Next.js frontends.

## 🔧 Environment Variables

### Development (Default)
```bash
# .env file - Development settings
CORS_ALLOW_ALL=true  # Allows all origins (including localhost)
# CORS_ORIGINS is optional in dev mode
```

### Production (Secure)
```bash
# .env file - Production settings
CORS_ALLOW_ALL=false  # Disable wildcard origins
CORS_ORIGINS=https://your-nextjs-app.vercel.app,https://your-domain.com
```

## 🚀 Next.js Frontend Integration

### 1. API Client Setup (Next.js)
```javascript
// lib/api.js
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = {
  async post(endpoint, data) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      credentials: 'include', // Important for CORS with credentials
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }
    
    return response.json();
  }
};
```

### 2. Dashboard API Call Example
```javascript
// components/Dashboard.js
import { apiClient } from '../lib/api';

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(false);

  const populateDashboard = async () => {
    setLoading(true);
    try {
      const result = await apiClient.post('/dashboard/populate-hierarchical', {
        case_id: 'CASE-2024-001',
        case_context: 'Medical malpractice case involving surgical negligence',
        additional_context: 'Patient harm during surgery'
      });
      setDashboardData(result);
    } catch (error) {
      console.error('Dashboard API Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <button onClick={populateDashboard} disabled={loading}>
        {loading ? 'Loading...' : 'Populate Dashboard'}
      </button>
      {dashboardData && (
        <div>
          <h3>Grid 1: Compliance</h3>
          <pre>{JSON.stringify(dashboardData.grid_1_compliance, null, 2)}</pre>
          
          <h3>Grid 2: Laws</h3>
          <pre>{JSON.stringify(dashboardData.grid_2_laws, null, 2)}</pre>
          
          <h3>Grid 3: Documents</h3>
          <pre>{JSON.stringify(dashboardData.grid_3_documents, null, 2)}</pre>
          
          <h3>Grid 4: Cases</h3>
          <pre>{JSON.stringify(dashboardData.grid_4_cases, null, 2)}</pre>
          
          <h3>Grid 5: Live Cases</h3>
          <pre>{JSON.stringify(dashboardData.grid_5_live_cases, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
```

### 3. Environment Variables (Next.js)
```bash
# .env.local (Next.js)
NEXT_PUBLIC_API_URL=http://localhost:8000  # Development
# NEXT_PUBLIC_API_URL=https://your-api.render.com  # Production
```

## 🔍 Troubleshooting CORS Issues

### Common Issues & Solutions

1. **Preflight Request Failures**
   ```
   Error: Access to fetch at 'http://localhost:8000/dashboard/populate-hierarchical' 
   from origin 'http://localhost:3000' has been blocked by CORS policy
   ```
   **Solution**: Ensure `OPTIONS` method is allowed (already configured)

2. **Credentials Issues**
   ```
   Error: The value of the 'Access-Control-Allow-Credentials' header is '' 
   which must be 'true' when the request's credentials mode is 'include'
   ```
   **Solution**: Set `credentials: 'include'` in fetch and `allow_credentials=True` in FastAPI (already configured)

3. **Custom Headers Blocked**
   ```
   Error: Request header field 'x-custom-header' is not allowed by 
   Access-Control-Allow-Headers in preflight response
   ```
   **Solution**: Add custom headers to `allow_headers` list in CORS config

## 🛡️ Security Best Practices

### Development
- ✅ Use `CORS_ALLOW_ALL=true` for easy development
- ✅ Test with actual Next.js dev server (localhost:3000)

### Production
- ❌ Never use `allow_origins=["*"]` with `allow_credentials=True`
- ✅ Set specific domains in `CORS_ORIGINS`
- ✅ Set `CORS_ALLOW_ALL=false`
- ✅ Use HTTPS for production domains

### Example Production .env
```bash
# Production FastAPI .env
CORS_ALLOW_ALL=false
CORS_ORIGINS=https://legal-dashboard.vercel.app,https://yourdomain.com
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
INDIAN_KANOON_API_TOKEN=your_indian_kanoon_token
```

## 🧪 Testing CORS

### 1. Browser DevTools Test
```javascript
// Run in browser console on your Next.js app
fetch('http://localhost:8000/health', {
  method: 'GET',
  credentials: 'include'
})
.then(response => response.json())
.then(data => console.log('✅ CORS working:', data))
.catch(error => console.error('❌ CORS error:', error));
```

### 2. cURL Test
```bash
# Test preflight request
curl -X OPTIONS \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  http://localhost:8000/dashboard/populate-hierarchical

# Test actual request
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:3000" \
  -d '{"case_id":"TEST","case_context":"test case"}' \
  http://localhost:8000/dashboard/populate-hierarchical
```

## 📋 Checklist for Next.js Integration

- [ ] FastAPI server running on port 8000
- [ ] Next.js app running on port 3000
- [ ] Environment variables set correctly
- [ ] `credentials: 'include'` in fetch requests
- [ ] `Content-Type: application/json` header set
- [ ] API endpoints tested with browser DevTools
- [ ] Production domains added to CORS_ORIGINS
- [ ] CORS_ALLOW_ALL=false in production

## 🚀 Ready for Production!

Your FastAPI backend is now fully compatible with Next.js frontends and follows security best practices. The CORS configuration will automatically adapt based on your environment variables.
