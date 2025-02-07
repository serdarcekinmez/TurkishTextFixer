# TurkishTextAlpha - Advanced AI-Powered Turkish Text Corrector

TurkishTextAlpha is an AI-powered **text corrector, naturalizer, and summarizer** for Turkish text, leveraging **Anthropic Claude API** for **grammatical corrections, dialect detection, and summarization**.

---

## 🚀 Features
### ✅ **Text Correction**
- Fixes **spelling, grammar, punctuation,** and improves clarity.
- Ensures proper use of **Turkish characters** (ç, ğ, ı, ö, ş, ü).
- Transforms **slang or informal language** into **standard Turkish**.

### ✅ **Naturalization & Dialect Handling**
- Preserves **regional dialects** and **colloquial expressions**.
- Allows users to **keep specific words unchanged** ("Öyle Bırak" feature).
- Supports informal rewriting for **conversational Turkish**.

### ✅ **Summarization**
- Summarizes **long Turkish texts** using AI.
- Uses **Claude** for high-quality summarization.
- Supports **summarization of original or corrected text**.

---

## 🛠 Installation & Setup
### **1️⃣ Clone the Repository**
```sh
$ git clone https://github.com/your-repo/TurkishTextAlpha.git
$ cd TurkishTextAlpha
```

### **2️⃣ Install Dependencies**
```sh
$ pip install -r requirements.txt
```

### **3️⃣ Create a `.env` File**
This project requires an **Anthropic Claude API key**. Create a `.env` file in the project root and add:
```sh
ANTHROPIC_API_KEY=your_api_key_here
```

---

## ⚡ Usage
### **Run the API**
```sh
$ uvicorn main:app --reload
```

### **API Endpoints**
#### 📝 **Correct a Text**
**Endpoint:** `POST /correct`
```json
{
  "text": "Gardaşım sunu şöyle güzel düzeltecek bi program bulamadık...",
  "action": "correct",
  "summarize_original": false,
  "summarize_corrected": false
}
```
🔹 **Response:**
```json
{
  "corrected_text": "Kardeşim, şunu söyleyeyim: güzel düzeltecek bir program bulamadık..."
}
```

#### 🌍 **Naturalize a Text (Informal)**
**Endpoint:** `POST /correct`
```json
{
  "text": "Gardasim sunu soyle guzel duzeltecek bi program...",
  "action": "natural_output"
}
```
🔹 **Response:**
```json
{
  "corrected_text": "Gardaşım, şunu şöyle güzel düzeltecek bir program...",
  "uncertain_words": ["balcan"]
}
```

#### 📌 **Summarize a Text**
**Endpoint:** `POST /correct`
```json
{
  "text": "Bu metin çok uzun, özetlenmesi gerekiyor...",
  "action": "summarize"
}
```
🔹 **Response:**
```json
{
  "summary": "Metin özeti burada."
}
```

---

## 🎯 Roadmap
- [ ] **Improve dialect detection**
- [ ] **Optimize response time**
- [ ] **Allow user-selected dialects**
- [ ] **Expand test cases for different text types**

---

## 📜 License
This project is **open-source** and available under the **MIT License**.

---

## 🤝 Contributing
We welcome contributions! Feel free to **fork, create issues, or submit PRs** to improve TurkishTextAlpha. 🚀

