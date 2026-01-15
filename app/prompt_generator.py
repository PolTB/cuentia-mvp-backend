from app.models import AgeRange

class PromptGenerator:
    """Generate age-appropriate DALL-E prompts for story illustrations"""
    
    @staticmethod
    def generate_image_prompt(child_name: str, age_range: str, story_content: str) -> str:
        """Generate DALL-E prompt based on story and age range
        
        Args:
            child_name: Name of the child
            age_range: Age range (3-5, 5-7, 7-10)
            story_content: Generated story text
            
        Returns:
            DALL-E prompt string
        """
        # Safety prefix for all prompts
        safety_prefix = "Safe for kids, child-friendly, colorful illustration: "
        
        # Extract key themes from story (simplified approach)
        # In production, could use NLP or LLM to extract better themes
        themes = PromptGenerator._extract_themes(story_content)
        
        # Age-appropriate style guidance
        style_guide = PromptGenerator._get_style_for_age(age_range)
        
        # Construct prompt
        prompt = f"{safety_prefix}{style_guide} Illustration of {child_name}'s story about {themes}. Warm, friendly, magical atmosphere."
        
        return prompt
    
    @staticmethod
    def _extract_themes(story: str) -> str:
        """Extract key themes from story (simplified)"""
        # Simple keyword extraction
        keywords = []
        story_lower = story.lower()
        
        theme_keywords = {
            'adventure': ['aventura', 'viaje', 'explorar', 'descubrir'],
            'friendship': ['amigo', 'amistad', 'juntos'],
            'magic': ['magia', 'mágico', 'hechizo', 'poder'],
            'nature': ['bosque', 'árbol', 'animal', 'naturaleza'],
            'fantasy': ['dragón', 'hada', 'castillo', 'príncipe', 'princesa']
        }
        
        for theme, words in theme_keywords.items():
            if any(word in story_lower for word in words):
                keywords.append(theme)
        
        return ', '.join(keywords[:3]) if keywords else 'a wonderful adventure'
    
    @staticmethod
    def _get_style_for_age(age_range: str) -> str:
        """Get art style appropriate for age range"""
        styles = {
            AgeRange.RANGE_3_5.value: "Simple shapes, bright primary colors, large friendly characters, minimal details",
            AgeRange.RANGE_5_7.value: "Colorful cartoon style, expressive characters, clear scenes, moderate detail",
            AgeRange.RANGE_7_10.value: "Rich illustration style, detailed characters, immersive scenes, fantasy elements"
        }
        return styles.get(age_range, styles[AgeRange.RANGE_5_7.value])

prompt_generator = PromptGenerator()
