from transformers import pipeline
import httpx


class IntelligenceAnalyzer:
    LABELS = ["terrorism", "disaster", "protest", "medical"]
    SUPPORTED_LOCALES = ("en", "ru")

    def __init__(self, ollama_url: str, llm_model: str = "qwen2.5:7b"):
        self.classifier = pipeline(
            "zero-shot-classification",
            model="MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling",
        )
        self.ollama_url = ollama_url
        self.llm_model = llm_model

    async def analyze_text(self, text: str) -> dict:
        source_language = self.detect_language(text)
        scores = self.classifier(text, self.LABELS, multi_label=False)

        summary = await self.generate_llm_summary(text)
        localized = await self.localize_event(summary, self.SUPPORTED_LOCALES)

        return {
            "category": scores["labels"][0],
            "confidence": scores["scores"][0],
            "source_language": source_language,
            "summary": summary,
            "description_i18n": localized,
        }

    async def generate_llm_summary(self, content: str) -> str:
        prompt = (
            "Summarize this news in one short sentence: "
            f"{content[:1000]}"
        )
        payload = {
            "model": self.llm_model,
            "prompt": prompt,
            "stream": False,
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
            )
            response.raise_for_status()
            return response.json().get("response", "")

    async def localize_event(self, summary: str, locales) -> dict:
        return {locale: await self.translate_text(summary, locale)
                for locale in locales}

    def detect_language(self, text: str) -> str:
        return "en"

    async def translate_text(self, text: str, locale: str) -> str:
        return text
