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
├── data
|    ├── datasets
|    ├── embeddings
|    └── sql
├── src
|    ├── services
|    └── storage
├── .env
└── README.md
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
</br>

## 📦 A. Setup Instructions
Open a terminal and follow these steps:
<br>

### 1. Clone the repository
```bash
git clone https://github.com/yusupwinata/Belle_Boutique_Chatbot
```
<br>

### 2. Open the cloned repository
```bash
cd Belle_Boutique_Chatbot
```
<br>

### 3. Create a virtual environment
In this tutorial I use **conda** to create a virtual environment named `specialist_env`.
```bash
conda create -n belle_boutique_chatbot python=3.11 -y
```
<br>

### 4. Activate the virtual environment
```bash
conda activate belle_boutique_chatbot
```
<br>

### 5. Install dependencies
```bash
pip install -r requirements.txt
```
<br>

---
<br>

## 🏃‍♂️ B. Run the API and Make Request Instructions
### 1. Running the API
```bash
uvicorn main:app --reload
```
The API will be available at:
http://127.0.0.1:8000
<br>
<br>

### 2. Making Requests
First, **Open a new terminal** in Belle_Boutique_Chatbot folder. Next, **test the /recommend endpoint**. You can test the endpoint using **curl**.
<br>
<br>

#### 3. Using curl
Make sure the API is running, then execute this command in your new terminal:
```bash
curl -X POST http://127.0.0.1:8000/route -H "Content-Type: application/json" -d "{\"user_message\":\"bagaimana cara klaim garansi?\"}"
```
**Note**: You can modify user_message in the command.
<br>
<br>

---
<br>

**Example Request Format:**
```json
{
  "user_message": "bagaimana cara klaim garansi?",
}
```
<br>

**Example output:**
```json
{
  "response": "Untuk mengklaim garansi produk, silakan:\n\n1. Hubungi layanan pelanggan kami dalam waktu maksimal 7 hari setelah barang diterima.\n2. Sertakan bukti foto/video dan nomor pesanan untuk memproses klaim garansi."
}
```

