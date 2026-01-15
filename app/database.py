from supabase import create_client, Client
from app.config import settings
from typing import Optional, Dict, Any
import uuid
from datetime import datetime


class DatabaseClient:
    """Supabase database client for story and metrics operations"""
    
    def __init__(self):
        self.client: Client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
    
    async def save_story(self, story_data: Dict[str, Any]) -> str:
        """Save generated story to database"""
        story_id = str(uuid.uuid4())
        
        story_record = {
            "id": story_id,
            "child_name": story_data["child_name"],
            "age_range": story_data["age_range"],
            "content": story_data["content"],
            "theme": story_data.get("theme"),
            "custom_elements": story_data.get("custom_elements"),
            "created_at": datetime.utcnow().isoformat()
                        "image_url": story_data.get("image_url"),
            "image_prompt": story_data.get("image_prompt"),
        }
        
        self.client.table("stories").insert(story_record).execute()
        return story_id
    
    async def save_metrics(self, story_id: str, metrics: Dict[str, Any]) -> None:
        """Save generation metrics to database"""
        metrics_record = {
            "id": str(uuid.uuid4()),
            "story_id": story_id,
            "tokens_prompt": metrics["tokens_prompt"],
            "tokens_completion": metrics["tokens_completion"],
            "tokens_total": metrics["tokens_total"],
            "latency_seconds": metrics["latency_seconds"],
            "cost_usd": metrics["cost_usd"],
            "model_used": metrics["model_used"],
            "moderation_flagged": metrics.get("moderation_flagged", False),
                        # Image generation metrics (optional)
            "image_generation_time_seconds": metrics.get("image_generation_time_seconds"),
            "image_model_used": metrics.get("image_model_used"),
            "image_cost_usd": metrics.get("image_cost_usd"),
            "created_at": datetime.utcnow().isoformat()
        }
        
        self.client.table("metrics").insert(metrics_record).execute()
    
    async def get_story(self, story_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve story by ID"""
        response = self.client.table("stories").select("*").eq("id", story_id).execute()
        return response.data[0] if response.data else None


db_client = DatabaseClient()
