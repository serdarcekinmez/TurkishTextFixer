




import anthropic
import os
from typing import List, Dict, Optional

class TurkishTextNaturalizer:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        
        # En popüler Türkçe ağız kelimeleri (maksimum 100, karışık)
        self.dialect_features: List[str] = [
            "gaci", "hele", "be", "abe", "ya", "uşak", "haçan", "düğün", "horon", "kemençe",
            "gari", "len", "çiğdem", "ağa", "lo", "billa", "hewal", "keko", "kurban",
            "kanka", "moruk", "abi", "abla", "reis", "hacı", "memo", "memoş", "panpa",
            "bilader", "xalo", "heval", "roj", "apo", "bavo", "daye", "bira", "xwişk", 
            "keçe", "lawo", "muhacir", "macır", "gardasım", "gız", "gadın", "baba", 
            "ana", "dede", "nine", "emmi", "dayı", "herif", "gelin"
        ]

    def detect_dialect_words(self, text: str) -> List[str]:
        """Tespit edilen ağız kelimelerini döndürür."""
        return [word for word in text.split() if word.lower() in self.dialect_features]

    def naturalize_text(self, text: str, preserve_dialect: bool = True) -> Dict[str, str]:
        dialect_words = self.detect_dialect_words(text) if preserve_dialect else []

        system_instructions = """
        Sen Türkçe'yi doğal ve akıcı hale getiren bir dil uzmanısın.
        - Metni düzenlerken anlamını bozma.
        - Türkçe karakterleri doğru kullan.
        - Eğer bir kelimenin ağız olduğu belirlenemezse, kullanıcıya bırak ("Öyle Bırak").
        """

        user_message = f"""
        Aşağıdaki metni doğal ve akıcı hale getir:
        <metin>
        {text}
        </metin>

        Önemli notlar:
        1. Eğer ağız özellikleri tespit edilirse, değiştirilmemesi için listele.
        2. Kullanıcı onayına sunulacak kelimeler: {', '.join(dialect_words) if dialect_words else 'Yok'}
        """

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            temperature=0.7,
            system=system_instructions,
            messages=[{"role": "user", "content": user_message}]
        )

        corrected_text = response.content[0].text.strip() if response.content else ""
        
        return {"corrected_text": corrected_text, "uncertain_words": dialect_words}
