#!/usr/bin/env python3
"""
Test rate limiting specifically for contact endpoint
"""

import asyncio
import aiohttp

BASE_URL = "https://futuristic-dev-45.preview.emergentagent.com/api"

async def test_rate_limit():
    """Test rate limiting on contact endpoint"""
    print("Testing contact rate limiting...")
    
    contact_data = {
        "name": "Rate Test User",
        "email": "ratetest@example.com",
        "subject": "Rate Limit Test",
        "body": "Testing rate limiting functionality"
    }
    
    timeout = aiohttp.ClientTimeout(total=30)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        rate_limit_hit = False
        successful_requests = 0
        
        # Try 7 requests rapidly
        for i in range(7):
            try:
                async with session.post(f"{BASE_URL}/contact", json=contact_data) as resp:
                    print(f"Request {i+1}: Status {resp.status}")
                    if resp.status == 429:
                        print(f"Rate limit hit on request {i+1}")
                        rate_limit_hit = True
                        break
                    elif resp.status == 201:
                        successful_requests += 1
                    else:
                        print(f"Unexpected status: {resp.status}")
                        break
            except Exception as e:
                print(f"Request {i+1} failed: {e}")
                break
        
        print(f"Successful requests: {successful_requests}")
        print(f"Rate limit triggered: {rate_limit_hit}")
        
        return rate_limit_hit

if __name__ == "__main__":
    asyncio.run(test_rate_limit())