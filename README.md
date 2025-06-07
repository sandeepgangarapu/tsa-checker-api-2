# TSA Item Checker API with Supabase Integration

A FastAPI application that checks TSA regulations for items using OpenRouter AI and stores all API calls in a Supabase database for analytics and logging.

## Features

- 🛡️ **TSA Compliance Check**: Determine if items are allowed in carry-on and/or checked baggage
- 🤖 **AI-Powered**: Uses Mistral 7B via OpenRouter for intelligent responses
- 📊 **Complete Logging**: All API calls are stored in Supabase with metadata
- ⚡ **Fast & Reliable**: Built with FastAPI for high performance
- 🔒 **CORS Enabled**: Ready for web frontend integration

## Database Schema

The application automatically logs each API call to the `tsa_api_logs` table in Supabase:

```sql
CREATE TABLE tsa_api_logs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    item_name TEXT NOT NULL,
    carry_on BOOLEAN NOT NULL,
    checked_bag BOOLEAN NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    response_time_ms INTEGER,
    user_agent TEXT,
    ip_address INET
);
```

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables:**
   Create a `.env` file with:
   ```
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   ```

3. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

## API Usage

### Check an Item

```bash
curl -X POST "http://localhost:8000/check-item" \
     -H "Content-Type: application/json" \
     -d '{"item_name": "laptop"}'
```

**Response:**
```json
{
  "carry_on": true,
  "checked_bag": true,
  "description": "Laptops are allowed in both carry-on and checked bags. It is strongly recommended to keep them in your carry-on."
}
```

## Testing & Monitoring

### Test the API
```bash
python test_api.py
```

### View Logged Data
```bash
python view_logs.py
```

## Supabase Integration

- **Project**: `tastiest` (kyudboffpfipzxlkzxam)
- **Table**: `tsa_api_logs`
- **Features**: 
  - Automatic logging of all API calls
  - Response time tracking
  - User agent and IP logging
  - Row Level Security enabled

## API Endpoints

- `POST /check-item` - Check TSA regulations for an item
- `GET /` - API welcome message
- `GET /docs` - Swagger API documentation

## Error Handling

The API gracefully handles:
- Invalid JSON responses from AI
- Database connection issues (logs error but continues serving)
- Network timeouts
- Malformed requests

Database logging failures do not affect API responses - the service remains available even if logging fails.

## Performance Monitoring

Each API call records:
- Response time in milliseconds
- Client IP address
- User agent string
- Timestamp of request

Use `view_logs.py` to analyze API usage patterns and performance metrics. 