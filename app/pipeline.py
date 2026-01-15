from app.openai_service import openai_service
from app.database import db_client
from app.models import StoryRequest, StoryResponse, GenerationMetrics
from datetime import datetime
from app.dalle_service import dalle_service
from app.prompt_generator import prompt_generator

async def generate_story_pipeline(request: StoryRequest) -> StoryResponse:
    try:
        content, metrics = await openai_service.generate_with_fallback(
            name=request.child_name,
            age_range=request.get_age_range().value,
            theme=request.theme
        )

                # Generate image with DALL-E 3
        image_url = None
        image_prompt = None
        try:
            image_prompt = prompt_generator.generate_image_prompt(
                child_name=request.child_name,
                age_range=request.get_age_range().value,
                story_content=content
            )
            image_url, image_metrics = await dalle_service.generate_image(image_prompt)
            # Merge image metrics into main metrics
            metrics.update(image_metrics)
        except Exception as img_error:
            # Image generation is optional - continue if it fails
            print(f"Image generation failed: {img_error}")
        story_data = {
            "child_name": request.child_name,
            "age_range": request.get_age_range().value,
            "content": content,
            "theme": request.theme,
            "custom_elements": request.custom_elements
                        "image_url": image_url,
            "image_prompt": image_prompt
        }
        story_id = await db_client.save_story(story_data)
        await db_client.save_metrics(story_id, metrics)
        return StoryResponse(
            story_id=story_id, content=content,
            child_name=request.child_name,
            age_range=request.get_age_range().value,
            metrics=GenerationMetrics(**metrics),
                        image_url=image_url,
            image_prompt=image_prompt,
            created_at=datetime.utcnow(), success=True
        )
    except Exception as e:
        return StoryResponse(
            story_id="", content="", child_name=request.child_name,
            age_range=request.get_age_range().value,
            metrics=GenerationMetrics(tokens_prompt=0, tokens_completion=0,
                tokens_total=0, latency_seconds=0, cost_usd=0, model_used=""),
            created_at=datetime.utcnow(), success=False, error=str(e)
        )
