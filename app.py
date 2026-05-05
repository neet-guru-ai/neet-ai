from flask import Flask, request, jsonify
import os
from huggingface_hub import InferenceClient

app = Flask(__name__)

# ===== OFFICIAL HUGGING FACE ENGINE =====
API_KEY = os.environ.get("HUGGINGFACE_API_KEY")

# 🧠 BRAIN SURGERY: AI ko strict instructions taaki wo comedy na kare
system_instruction = """
You are a highly advanced NEET Expert AI. 
Strictly answer questions related to NCERT Biology, Physics, and Chemistry for Class 11 and 12.
CRITICAL RULE FOR LANGUAGE: When explaining in Hindi or Hinglish, DO NOT translate scientific or technical terms into pure Hindi (e.g., do NOT translate 'Genetics', 'Nucleus', 'DNA', 'Reproduction'). Always keep scientific terms in English. Explain concepts logically, scientifically, and accurately.
Provide clear, concise, and highly accurate answers suitable for a NEET aspirant.
If the user asks something completely outside of studies or science, politely decline.
"""

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dr. Nikhil MBBS AI</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        
        body { 
            margin: 0; font-family: 'Inter', sans-serif; background-color: #ffffff; 
            color: #333333; display: flex; flex-direction: column; height: 100vh; 
            transition: 0.3s;
        }

        body.dark-mode { background-color: #212121; color: #ececf1; }

        .header { 
            display: flex; justify-content: space-between; align-items: center; 
            padding: 15px 20px; border-bottom: 1px solid #e5e5e5;
            position: sticky; top: 0; background: inherit; z-index: 10;
        }
        body.dark-mode .header { border-bottom-color: #333; }

        .title { font-weight: 600; font-size: 18px; display: flex; align-items: center; gap: 8px; }
        .badge { background: #007bff; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; }

        .chat-container { 
            flex: 1; overflow-y: auto; padding: 20px 10%; 
            display: flex; flex-direction: column; gap: 24px; padding-bottom: 120px;
        }

        .message { max-width: 85%; padding: 12px 18px; border-radius: 15px; line-height: 1.6; font-size: 16px; }
        .user-message { background-color: #f3f3f3; align-self: flex-end; border-bottom-right-radius: 4px; }
        body.dark-mode .user-message { background-color: #2f2f2f; }
        .ai-message { background-color: transparent; align-self: flex-start; }

        .mystic-loader {
            display: none; align-self: flex-start; width: 40px; height: 40px;
            position: relative; margin-left: 20px;
        }
        .mystic-loader::before, .mystic-loader::after {
            content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            border-radius: 50%; border: 3px solid transparent;
            border-top-color: #007bff; border-bottom-color: #9d00ff;
            animation: mystic-spin 1s infinite linear;
        }
        .mystic-loader::after { border-top-color: transparent; border-bottom-color: transparent; border-left-color: #00f7ff; animation-duration: 1.5s; }
        @keyframes mystic-spin { 0% { transform: rotate(0deg) scale(1); } 50% { transform: rotate(180deg) scale(1.2); } 100% { transform: rotate(360deg) scale(1); } }

        /* 🎨 UI FIX: Input box aur disclaimer ko center karne ke liye */
        .input-wrapper {
            position: fixed; bottom: 0; width: 100%; padding: 15px 20px;
            box-sizing: border-box; display: flex; flex-direction: column; align-items: center;
            background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,1) 35%);
        }
        body.dark-mode .input-wrapper { background: linear-gradient(180deg, rgba(33,33,33,0) 0%, rgba(33,33,33,1) 35%); }

        .input-box {
            display: flex; align-items: center; background-color: #f4f4f4;
            border-radius: 30px; padding: 10px 20px; width: 100%; max-width: 800px;
            border: 1px solid #e5e5e5;
        }
        body.dark-mode .input-box { background-color: #2f2f2f; border-color: #444; }

        input { flex: 1; background: transparent; border: none; outline: none; font-size: 16px; color: inherit; padding: 10px; }
        .action-btn { background: none; border: none; font-size: 20px; cursor: pointer; color: #888; transition: 0.2s; }
        .send-btn { background: #000; color: #fff; border-radius: 50%; width: 35px; height: 35px; display: flex; justify-content: center; align-items: center; cursor: pointer; border: none; margin-left: 5px; }
        body.dark-mode .send-btn { background: #fff; color: #000; }
        #theme-btn { background: none; border: none; font-size: 24px; cursor: pointer; transition: 0.3s; }
        
        /* 📝 DISCLAIMER CSS */
        .disclaimer { font-size: 12px; color: #888; margin-top: 8px; text-align: center; }
        body.dark-mode .disclaimer { color: #aaa; }
    </style>
</head>
<body class="dark-mode">

    <div class="header">
        <div class="title">🩺 Dr. Nikhil MBBS <span class="badge">Official AI Engine</span></div>
        <button id="theme-btn" onclick="toggleDarkMode()" title="Toggle Theme">☀️</button>
    </div>

    <div class="chat-container" id="chatContainer">
        <div class="message ai-message">
            Swagat hai Dr. Nikhil! Main ek advanced NEET AI hoon. Sawaal puchiye! 🧬
        </div>
    </div>

    <div class="mystic-loader" id="loader"></div>

    <div class="input-wrapper">
        <div class="input-box">
            <button class="action-btn">➕</button>
            <input type="text" id="questionInput" placeholder="Message NEET AI (NCERT Topics)..." onkeypress="handleEnter(event)">
            <button class="send-btn" onclick="askQuestion()">➤</button>
        </div>
        <!-- DISCLAIMER TEXT ADDED HERE -->
        <div class="disclaimer">AI can make mistakes. Please verify important information from NCERT.</div>
    </div>

    <script>
        function toggleDarkMode() { 
            document.body.classList.toggle('dark-mode'); 
            const btn = document.getElementById('theme-btn');
            btn.innerText = document.body.classList.contains('dark-mode') ? '☀️' : '🌙';
        }
        
        function handleEnter(e) { if(e.key === 'Enter') askQuestion(); }

        function appendMessage(sender, text) {
            const chat = document.getElementById("chatContainer");
            const msgDiv = document.createElement("div");
            msgDiv.className = "message " + (sender === "user" ? "user-message" : "ai-message");
            msgDiv.innerHTML = text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>').replace(/\\n/g, '<br>');
            chat.appendChild(msgDiv);
            chat.scrollTop = chat.scrollHeight;
        }

        async function askQuestion() {
            const input = document.getElementById("questionInput");
            const question = input.value.trim();
            const loader = document.getElementById("loader");

            if(!question) return;

            input.value = "";
            appendMessage("user", question);
            loader.style.display = "block";
            document.getElementById("chatContainer").appendChild(loader);
            document.getElementById("chatContainer").scrollTop = document.getElementById("chatContainer").scrollHeight;

            try {
                const response = await fetch("/ask", {
                    method: "POST", headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: question })
                });
                const data = await response.json();
                loader.style.display = "none";
                appendMessage("ai", data.answer);
            } catch (error) {
                loader.style.display = "none";
                appendMessage("ai", "Network error. Phirse try karo.");
            }
        }
    </script>
</body>
</html>
"""

@app.route("/ask", methods=["POST"])
def ask():
    try:
        if not API_KEY:
            return jsonify({"answer": "Error: HUGGINGFACE_API_KEY nahi mili. Render Environment check karo."})

        data = request.get_json()
        question = data.get("question", "")

        client = InferenceClient("Qwen/Qwen2.5-7B-Instruct", token=API_KEY)
        
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": question}
        ]
        
        response = client.chat_completion(messages, max_tokens=800)
        answer = response.choices[0].message.content
        
        return jsonify({"answer": answer})

    except Exception as e:
        error_str = str(e)
        if "loading" in error_str.lower() or "cold" in error_str.lower():
            return jsonify({"answer": "Bhai, AI abhi neend se uth raha hai. 10-15 second baad same sawaal wapas pucho!"})
        return jsonify({"answer": f"API Error: {error_str}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
