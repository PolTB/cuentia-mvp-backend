from openai import AsyncOpenAI
from app.config import settings
import time
import asyncio
from typing import Tuple, Dict, Any

class DALLEService:
    """DALL-E 3 image generation service for story illustrations"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = "dall-e-3"
        self.size = "1024x1024"
        self.quality = "hd"
        self.timeout = settings.dalle_timeout
    
    async def generate_image(self, prompt: str) -> Tuple[str, Dict[str, Any]]:
        """Generate image with DALL-E 3
        
        Args:
            prompt: Image generation prompt
            
        Returns:
            Tuple of (image_url, metrics)
        """
        start_time = time.time()
        
        try:
            response = await asyncio.wait_for(
                self.client.images.generate(
                    model=self.model,
                    prompt=prompt,
                    size=self.size,
                    quality=self.quality,
                    n=1
                ),
                timeout=self.timeout
            )
            
            latency = time.time() - start_time
            image_url = response.data[0].url
            
            # DALL-E 3 HD 1024x1024 cost is $0.080
            cost = 0.080
            
            metrics = {
                "image_generation_time_seconds": round(latency, 2),
                "image_model_used": self.model,
                "image_cost_usd": cost,
                "image_size": self.size,
                "image_quality": self.quality
            }
            
            return image_url, metrics
            
        except asyncio.TimeoutError:
            raise Exception(f"Image generation timed out after {self.timeout}s")
        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")

dalle_service = DALLEService()
