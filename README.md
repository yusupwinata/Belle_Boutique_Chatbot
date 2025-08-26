# Belle Boutique Chatbot
 This is a simple FastAPI-based API that uses Llama3.2 language model, via Ollama and OpenAI API, to help answer customer questions about Belle Boutique (products, FAQ, shipment tracking, etc.).
<br>

## 🔑 Prerequisite
You must have a OpenAI API key, then add your Google API key to the `.env` file. Example:
```text
OPENAI_API_KEY=your_openai_api_key_here
```
<br>

## 📁 Project Structure
```text
Belle_Boutique_Chatbot/
├── main.py
├── src
|    ├──
|    ├──
|    └──
├── services
|    ├──
|    ├──
|    └──
├── .env                     # Contains your GOOGLE_API_KEY (empty)
└── README.md                # This tutorial
```
<br>

---
<br>

## 🗃️ Database Design
```text
erDiagram
    orders {
        TEXT order_id PK
        TEXT no_resi
        TEXT nama_pelanggan
        TEXT produk
        TEXT kota_asal
        TEXT kota_tujuan
        DATE tanggal_kirim
        DATE estimasi_sampai
        TEXT status
    }

    chat_history {
        INTEGER id PK
        TEXT user_message
        TEXT assistant_message
        DATETIME created_at
    }
```
