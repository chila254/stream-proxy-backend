# MaxStream Proxy Backend

A FastAPI-based proxy server for extracting stream URLs from vidsrc.to for movies and TV series.

## Features

- ✅ Movie streaming support
- ✅ TV series with season/episode support  
- ✅ Multiple stream URL extraction methods
- ✅ CORS bypass for Flutter apps
- ✅ Fast async processing
- ✅ Auto-generated API docs

## API Endpoints

### Get Stream URL
```
GET /stream?type={movie|tv}&id={tmdb_id}&season={season}&episode={episode}
```

**Parameters:**
- `type` (required): "movie" or "tv"
- `id` (required): TMDb ID of the content
- `season` (optional): Season number (required for TV)
- `episode` (optional): Episode number (required for TV)

**Examples:**
```bash
# Movie
GET /stream?type=movie&id=552095

# TV Series
GET /stream?type=tv&id=1412&season=2&episode=5
```

**Response:**
```json
{
  "success": true,
  "stream_url": "https://example.com/stream.m3u8",
  "source": "vidsrc.to",
  "type": "movie",
  "id": 552095
}
```

## Deployment

### 🚀 Deploy to Render (FREE)

1. Create account at https://render.com
2. Click "New Web Service"
3. Connect your GitHub repo or upload files
4. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment:** Python 3.11

### 🚄 Deploy to Railway (FREE)

1. Create account at https://railway.app
2. Click "Deploy from GitHub repo" or "Deploy from template"
3. Railway will auto-detect the configuration from `railway.json`
4. Your API will be live at: `https://your-app.up.railway.app`

### 🐳 Docker Deployment

```bash
# Build image
docker build -t maxstream-proxy .

# Run container
docker run -p 8000:8000 maxstream-proxy
```

### 🖥️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload

# API will be available at: http://localhost:8000
# API docs at: http://localhost:8000/docs
```

## Integration with Flutter

Update your `enhanced_stream_extractor.dart`:

```dart
Future<String?> extractStreamUrl(String type, String tmdbId, {int? season, int? episode}) async {
  String url = 'https://your-proxy.onrender.com/stream?type=$type&id=$tmdbId';
  
  if (type == 'tv' && season != null && episode != null) {
    url += '&season=$season&episode=$episode';
  }
  
  final response = await http.get(Uri.parse(url));
  
  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    if (data['success'] == true) {
      return data['stream_url'];
    }
  }
  
  return null;
}
```

## Endpoints

- `/` - Root endpoint with API info
- `/stream` - Main stream extraction endpoint  
- `/health` - Health check for monitoring
- `/docs` - Auto-generated API documentation
- `/redoc` - Alternative API documentation

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400` - Bad Request (missing parameters)
- `404` - Stream not found
- `500` - Server error
- `200` - Success

## Notes

- Free tier on Render/Railway may have some limitations
- vidsrc.to may occasionally change their structure
- The proxy handles CORS and scraping complexity
- Multiple extraction methods for better reliability
