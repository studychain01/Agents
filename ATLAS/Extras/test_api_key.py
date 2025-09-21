#!/usr/bin/env python3
"""
Test script to verify NVIDIA API key is working
"""
import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

async def test_api_key():
    """Test if the API key works"""
    load_dotenv()
    api_key = os.getenv("NEMOTRON_4_340B_INSTRUCT_KEY")
    
    if not api_key:
        print("❌ No API key found in environment")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    # Test with NVIDIA API
    client = AsyncOpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )
    
    try:
        print("🔄 Testing API connection...")
        response = await client.chat.completions.create(
            model="mistralai/mixtral-8x7b-instruct-v0.1",
            messages=[{"role": "user", "content": "Say 'API test successful'"}],
            max_tokens=10,
            temperature=0.1
        )
        
        print("✅ API Connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_api_key())
    print(f"\nResult: {'SUCCESS' if success else 'FAILED'}")

