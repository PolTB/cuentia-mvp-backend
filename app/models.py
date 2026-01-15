from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class AgeRange(str, Enum):
    """Age ranges for story generation"""
    RANGE_3_5 = "3-5"
    RANGE_5_7 = "5-7"
    RANGE_7_10 = "7-10"
    DEFAULT = "default"


class StoryRequest(BaseModel):
    """Request model for story generation"""
    child_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=3, le=10)
    theme: Optional[str] = Field(None, max_length=100)
    custom_elements: Optional[str] = Field(None, max_length=500)
    
    def get_age_range(self) -> AgeRange:
        """Determine age range from age"""
        if 3 <= self.age <= 5:
            return AgeRange.RANGE_3_5
        elif 5 < self.age <= 7:
            return AgeRange.RANGE_5_7
        elif 7 < self.age <= 10:
            return AgeRange.RANGE_7_10
        return AgeRange.DEFAULT


class GenerationMetrics(BaseModel):
    """Metrics captured during story generation"""
    tokens_prompt: int
    tokens_completion: int
    tokens_total: int
    latency_seconds: float
    cost_usd: float
    model_used: str
    moderation_flagged: bool = False


class StoryResponse(BaseModel):
    """Response model for generated story"""
    story_id: str
    content: str
    child_name: str
    age_range: str
    metrics: GenerationMetrics
    created_at: datetime
    success: bool = True
    error: Optional[str] = None
