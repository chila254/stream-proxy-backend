from fastapi import FastAPI, Query
import httpx
from bs4 import BeautifulSoup
import re
import asyncio

app = FastAPI(title="MaxStream Proxy API", description="Stream URL extractor for movies and TV series")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

BASE_URL = "https://vidsrc.to/embed"

@app.get("/")
async def root():
    return {"message": "MaxStream Proxy API is running", "endpoints": ["/stream", "/docs"]}

@app.get("/stream")
async def get_stream_url(
    type: str = Query(..., regex="^(movie|tv)$", description="Content type: movie or tv"),
    id: int = Query(..., description="TMDb ID of the content"),
    season: int = Query(None, description="Season number (required for TV series)"),
    episode: int = Query(None, description="Episode number (required for TV series)"),
):
    """
    Extract stream URL for movies and TV series
    
    - **type**: movie or tv
    - **id**: TMDb ID 
    - **season**: Season number (for TV series only)
    - **episode**: Episode number (for TV series only)
    """
    
    # Build URL based on content type
    if type == "movie":
        url = f"{BASE_URL}/movie/{id}"
    elif type == "tv":
        if season is None or episode is None:
            return {"error": "Season and episode are required for TV series"}
        url = f"{BASE_URL}/tv/{id}/{season}/{episode}"
    else:
        return {"error": "Invalid content type"}

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=HEADERS, follow_redirects=True)
            response.raise_for_status()
            
        html_content = response.text
        
        # Multiple extraction methods for different vidsrc formats
        stream_url = await extract_stream_url(html_content)
        
        if stream_url:
            return {
                "success": True,
                "stream_url": stream_url,
                "source": "vidsrc.to",
                "type": type,
                "id": id,
                "season": season if type == "tv" else None,
                "episode": episode if type == "tv" else None
            }
        else:
            return {"error": "Stream URL not found", "source_url": url}
            
    except httpx.TimeoutException:
        return {"error": "Request timeout"}
    except httpx.HTTPStatusError as e:
        return {"error": f"HTTP error: {e.response.status_code}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

async def extract_stream_url(html_content: str) -> str:
    """Extract stream URL using multiple methods"""
    
    # Method 1: Look for m3u8 URLs in script tags
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Find script tags containing m3u8
    script_tags = soup.find_all("script")
    for script in script_tags:
        if script.string:
            m3u8_match = re.search(r'https://[^"\']+\.m3u8[^"\']*', script.string)
            if m3u8_match:
                return m3u8_match.group(0)
    
    # Method 2: Look for mp4 URLs
    for script in script_tags:
        if script.string:
            mp4_match = re.search(r'https://[^"\']+\.mp4[^"\']*', script.string)
            if mp4_match:
                return mp4_match.group(0)
    
    # Method 3: Look in the full HTML content
    m3u8_pattern = re.compile(r'https://[^\s"\'<>]+\.m3u8[^\s"\'<>]*')
    m3u8_matches = m3u8_pattern.findall(html_content)
    if m3u8_matches:
        return m3u8_matches[0]
    
    # Method 4: Look for any video stream URLs
    video_pattern = re.compile(r'https://[^\s"\'<>]+\.(mp4|m3u8|webm)[^\s"\'<>]*')
    video_matches = video_pattern.findall(html_content)
    if video_matches:
        return f"https://{video_matches[0][0]}.{video_matches[0][1]}"
    
    return None

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment platforms"""
    return {"status": "healthy", "service": "MaxStream Proxy API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
