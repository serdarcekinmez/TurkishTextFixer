




import re
import anthropic
import os

# Load API key
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
client = anthropic.Anthropic(api_key=anthropic_api_key)

def correct_turkish_text(text: str):
    system_instructions = """
    You are an advanced AI specialized in the Turkish language. Your task is to correct and enhance the provided Turkish text while strictly maintaining its meaning.

    ## Görev Tanımı:
    - Yazım ve dilbilgisi hatalarını düzeltin.
    - Noktalama işaretlerini düzenleyin.
    - Türkçe karakterleri (ç, ğ, ı, ö, ş, ü) doğru kullanın.
    - Metni daha akıcı, doğal ve anlaşılır hale getirin.
    - Günlük konuşma dilini daha resmi ve akıcı bir formata çevirin.
    - İngilizce kelimeleri mümkünse Türkçeleştirin, ancak teknik terimler için koruyun.

    **Yanıt formatı şu şekilde olmalıdır:**

    <summary>
    [Yapılan değişikliklerin özeti]
    </summary>

    <corrected_text>
    [Düzeltilmiş metin]
    </corrected_text>
    """
    
    user_message_text = f"Lütfen bu Türkçe metni düzelt:\n<turkish_text>\n{text}\n</turkish_text>"
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        temperature=0.3,
        system=system_instructions,
        messages=[{"role": "user", "content": user_message_text}]
    )
    
    model_reply = response.content[0].text if response.content else ""
    corrected_match = re.search(r"<corrected_text>(.*?)</corrected_text>", model_reply, re.DOTALL | re.IGNORECASE)
    return corrected_match.group(1).strip() if corrected_match else model_reply.strip()
