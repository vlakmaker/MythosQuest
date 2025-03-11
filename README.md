# 📜 MythosQuest - AI Dungeon Master

**A dynamic AI-powered historical roleplaying game.**  
Built with **Flask, Ollama, and Mistral/Gemma**, MythosQuest allows you to immerse yourself in historical storytelling with an AI Dungeon Master.

---

## 🛠️ Features
- 🌍 **Historical RPG Experience** – Set in real historical periods.
- 🎭 **AI Dungeon Master** – Responds dynamically to player choices.
- ⚡ **Memory System** – Keeps track of past decisions for a consistent narrative.
- 💬 **Interactive Web Interface** – Play directly in your browser.
- 🔄 **Dockerized Deployment** – Easily run on any server.
- 🚀 **Streamed AI Responses** – Faster and more natural gameplay.

---

## 🖥️ Installation & Setup

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/MythosQuest.git
cd MythosQuest
```

### 2️⃣ Install Dependencies
#### (Local Setup - Without Docker)
```sh
pip install -r requirements.txt
```
#### (Docker Setup - Recommended)
```sh
docker-compose up --build -d
```

### ⚙️ Configuration
#### Environment Variables
MythosQuest runs with default settings, but you can modify the following variables:

| Variable         | Default                     | Description                         |
|-----------------|---------------------------|-------------------------------------|
| FLASK_APP       | ai_dm.py                   | Entry point for the Flask app      |
| OLLAMA_HOST     | http://ollama_server:11434 | Ollama model server address        |
| PYTHONUNBUFFERED | 1                          | Ensures real-time logs             |

---

## 🕹️ Usage

### 1️⃣ Running Locally
```sh
python ai_dm.py
```
Then, open your browser and go to:  
📌 [http://localhost:5000](http://localhost:5000)

### 2️⃣ Running in Docker
```sh
docker-compose up --build -d
```
Check logs if needed:
```sh
docker logs -f mythosquest_ai
```

### 3️⃣ Testing the API
You can test the API with cURL:
```sh
curl -X POST http://localhost:5000/generate -H "Content-Type: application/json" -d '{"prompt": "Describe a medieval market scene."}'
```

---

## 🔧 Deployment (Oracle Cloud)

### 1️⃣ Connect to your Oracle Cloud VM
```sh
ssh ubuntu@YOUR_ORACLE_CLOUD_IP
```

### 2️⃣ Install Docker & Git (if not installed)
```sh
sudo apt update && sudo apt install -y docker docker-compose git
```

### 3️⃣ Clone & Start the Server
```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/MythosQuest.git
cd MythosQuest
docker-compose up --build -d
```

### 4️⃣ Verify Running Containers
```sh
docker ps
```

### 5️⃣ Test the API
```sh
curl -X POST http://YOUR_ORACLE_CLOUD_IP:5000/generate -H "Content-Type: application/json" -d '{"prompt": "Describe a medieval market scene."}'
```

---

## 🛠️ Troubleshooting

| Issue                     | Solution                                                         |
|---------------------------|-----------------------------------------------------------------|
| Port 5000 not reachable   | Open firewall rules for port 5000 (`sudo ufw allow 5000/tcp`)  |
| Slow AI responses         | Consider upgrading hardware or using an API model instead      |
| Docker errors             | Run `docker-compose down && docker-compose up --build -d`      |
| Model not found           | Ensure Ollama has pulled mistral or gemma (`docker exec -it ollama_server ollama list`) |

---

## 📜 Roadmap

### ✅ Current Features
- Basic AI Dungeon Master roleplaying
- Persistent memory system
- Web interface & API support
- Oracle Cloud deployment

### 🚀 Future Plans
- Fine-tune AI for better roleplay
- Improve UI/UX for smoother gameplay
- Add multiplayer support

---

## 🤝 Contributing
Feel free to fork this repo and submit pull requests!

1. Fork the repository  
2. Create a new branch (`git checkout -b feature-new`)  
3. Commit your changes (`git commit -m "Added new feature"`)  
4. Push your branch (`git push origin feature-new`)  
5. Create a pull request  

---

## 📜 License
**MIT License** – Free to use, modify, and share!  
Check [LICENSE.md](LICENSE.md) for details.

---

## ✨ Credits
- **Flask** for the web interface
- **Ollama** for LLM serving
- **Mistral/Gemma** as AI models