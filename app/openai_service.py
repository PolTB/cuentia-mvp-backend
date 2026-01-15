from openai import AsyncOpenAI
from app.config import settings
from app.models import AgeRange
import time, asyncio

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    def get_prompt(self, age_range, name, theme=None):
        prompts = {
            "3-5": f"Cuento simple para {name}, frases cortas, 200 palabras.",
            "5-7": f"Cuento para {name}, lenguaje sencillo, 350 palabras.",
            "7-10": f"Cuento para {name}, tramas complejas, 500 palabras."
        }
        p = prompts.get(age_range, f"Cuento para {name}")
        if theme: p += f" Tema: {theme}."
        return p + " Educativo y positivo."
    
    async def moderate(self, text):
        try:
            r = await self.client.moderations.create(input=text)
            return r.results[0].flagged
        except: return False
    
    def calc_cost(self, p_tokens, c_tokens, model):
        if "gpt-4" in model:
            return p_tokens*0.00003 + c_tokens*0.00006
        return p_tokens*0.000001 + c_tokens*0.000002
    
    async def generate_with_fallback(self, name, age_range, theme=None):
        prompt = self.get_prompt(age_range, name, theme)
        if await self.moderate(prompt):
            raise Exception("Input flagged")
        
        for model in [settings.openai_model_primary, settings.openai_model_fallback]:
            try:
                start = time.time()
                r = await asyncio.wait_for(
                    self.client.chat.completions.create(
                        model=model, messages=[{"role":"user","content":prompt}],
                        temperature=0.8, max_tokens=600
                    ), timeout=settings.openai_timeout
                )
                content = r.choices[0].message.content
                metrics = {
                    "tokens_prompt": r.usage.prompt_tokens,
                    "tokens_completion": r.usage.completion_tokens,
                    "tokens_total": r.usage.total_tokens,
                    "latency_seconds": time.time()-start,
                    "model_used": model,
                    "cost_usd": self.calc_cost(r.usage.prompt_tokens, r.usage.completion_tokens, model),
                    "moderation_flagged": await self.moderate(content)
                }
                if metrics["moderation_flagged"]:
                    raise Exception("Output flagged")
                return content, metrics
            except: continue
        raise Exception("Both models failed")

openai_service = OpenAIService()
