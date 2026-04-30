from flask import Flask, request, jsonify
import os
from google import genai
from google.genai import types

app = Flask(__name__)

# ===== GEMINI API SETUP =====
API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

system_instruction = """
You are a highly advanced NEET Expert AI. 
Strictly answer questions related to NCERT Biology, Physics, and Chemistry for Class 11 and 12.
Provide clear, concise, and highly accurate answers suitable for a NEET aspirant.
If the user asks something completely outside of studies or science, politely decline and ask them to focus on NEET topics.
Use a mix of Hindi and English (Hinglish) if the user asks in Hinglish, otherwise reply in English.
"""

# ===== ROUTES =====
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
        
        /* Base Light Theme (ChatGPT style) */
        body { 
            margin: 0; 
            font-family: 'Inter', sans-serif; 
            background-color: #ffffff; 
            color: #333333; 
            display: flex; 
            flex-direction: column; 
            height: 100vh; 
            transition: background-color 0.3s, color 0.3s;
        }

        /* Dark Theme Variables */
        body.dark-mode {
            background-color: #212121;
            color: #ececf1;
        }

        /* Header */
        .header { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            padding: 15px 20px; 
            border-bottom: 1px solid #e5e5e5;
            position: sticky;
            top: 0;
            background: inherit;
            z-index: 10;
        }
        body.dark-mode .header { border-bottom-color: #333; }

        .menu-left { display: flex; align-items: center; gap: 15px; }
        .icon-btn { background: none; border: none; font-size: 22px; cursor: pointer; color: inherit; padding: 5px; }
        
        .title { font-weight: 600; font-size: 18px; display: flex; align-items: center; gap: 8px; }
        .badge { background: #007bff; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; }

        /* Settings Panel */
        .settings-panel {
            position: absolute;
            top: 60px;
            right: 20px;
            background: #f9f9f9;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            display: none;
            z-index: 100;
        }
        body.dark-mode .settings-panel { background: #2f2f2f; border-color: #444; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
        
        .toggle-btn {
            background: none; border: none; font-size: 16px; color: inherit; cursor: pointer; display: flex; align-items: center; gap: 10px; font-family: inherit;
        }

        /* Chat Area */
        .chat-container { 
            flex: 1; 
            overflow-y: auto; 
            padding: 20px 10%; 
            display: flex; 
            flex-direction: column; 
            gap: 24px; 
            padding-bottom: 120px;
        }

        .message { max-width: 85%; padding: 12px 18px; border-radius: 15px; line-height: 1.6; font-size: 16px; }
        .user-message { background-color: #f3f3f3; align-self: flex-end; border-bottom-right-radius: 4px; }
        body.dark-mode .user-message { background-color: #2f2f2f; }
        .ai-message { background-color: transparent; align-self: flex-start; }

        /* Mysterious Loader */
        .mystic-loader {
            display: none;
            align-self: flex-start;
            width: 30px;
            height: 30px;
            position: relative;
            margin-left: 20px;
        }
        .mystic-loader::before, .mystic-loader::after {
            content: '';
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            border-radius: 50%;
            border: 2px solid transparent;
            border-top-color: #007bff;
            border-bottom-color: #00f7ff;
            animation: spin 1.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
        }
        .mystic-loader::after {
            animation-delay: -0.5s;
            animation-duration: 2s;
            border-top-color: transparent;
            border-bottom-color: transparent;
            border-left-color: #9d00ff;
            border-right-color: #007bff;
        }
        @keyframes spin {
            0% { transform: rotate(0deg) scale(0.8); }
            50% { transform: rotate(180deg) scale(1.1); box-shadow: 0 0 10px rgba(0, 123, 255, 0.5); }
            100% { transform: rotate(360deg) scale(0.8); }
        }

        /* Bottom Input Area */
        .input-wrapper {
            position: fixed;
            bottom: 0;
            width: 100%;
            padding: 20px;
            box-sizing: border-box;
            background: linear-gradient(180deg, rgba(255,255,255,0) 0%, rgba(255,255,255,1) 30%);
            display: flex;
            justify-content: center;
        }
        body.dark-mode .input-wrapper { background: linear-gradient(180deg, rgba(33,33,33,0) 0%, rgba(33,33,33,1) 30%); }

        .input-box {
            display: flex;
            align-items: center;
            background-color: #f4f4f4;
            border-radius: 30px;
            padding: 8px 15px;
            width: 100%;
            max-width: 800px;
            box-shadow: 0 0 15px rgba(0,0,0,0.05);
            border: 1px solid #e5e5e5;
        }
        body.dark-mode .input-box { background-color: #2f2f2f; border-color: transparent; box-shadow: 0 0 15px rgba(0,0,0,0.5); }

        .input-box input {
            flex: 1;
            background: transparent;
            border: none;
            outline: none;
            font-size: 16px;
            color: inherit;
            font-family: inherit;
            padding: 10px;
        }
        
        .send-btn {
            background-color: #000;
            color: #fff;
            border-radius: 50%;
            width: 35px;
            height: 35px;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            border: none;
            margin-left: 5px;
        }
        body.dark-mode .send-btn { background-color: #fff; color: #000; }

        /* Scrollbar styling */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-thumb { background: #ccc; border-radius: 4px; }
        body.dark-mode ::-webkit-scrollbar-thumb { background: #555; }
    </style>
</head>
<body class="dark-mode"> <!-- Defaulting to Dark Mode as per screenshot -->

    <!-- Header -->
    <div class="header">
        <div class="menu-left">
            <button class="icon-btn">☰</button>
            <div class="title">🩺 Dr. Nikhil MBBS <span class="badge">NEET AI</span></div>
        </div>
        <button class="icon-btn" onclick="toggleSettings()">⚙️</button>
    </div>

    <!-- Settings Panel -->
    <div class="settings-panel" id="settingsPanel">
        <button class="toggle-btn" onclick="toggleDarkMode()">
            <span id="themeIcon">☀️</span> <span id="themeText">Light Mode</span>
        </button>
    </div>

    <!-- Chat Container -->
    <div class="chat-container" id="chatContainer">
        <div class="message ai-message">
            Hello Dr. Nikhil! Main aapki personal NEET AI hoon. Aaj Biology, Physics ya Chemistry mein kya padhna hai?
        </div>
    </div>

    <!-- Mysterious Loader -->
    <div class="mystic-loader" id="loader"></div>

    <!-- Input Area -->
    <div class="input-wrapper">
        <div class="input-box">
            <button class="icon-btn" title="Add Photo/Video (Coming Soon)">➕</button>
            <input type="text" id="questionInput" placeholder="Message NEET AI..." onkeypress="handleEnter(event)">
            <button class="send-btn" onclick="askQuestion()">➤</button>
        </div>
    </div>

    <script>
        function toggleSettings() {
            const panel = document.getElementById('settingsPanel');
            panel.style.display = panel.style.display === 'flex' ? 'none' : 'flex';
        }

        function toggleDarkMode() {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            document.getElementById('themeIcon').innerText = isDark ? '☀️' : '🌙';
            document.getElementById('themeText').innerText = isDark ? 'Light Mode' : 'Dark Mode';
            toggleSettings();
        }

        function handleEnter(e) {
            if(e.key === 'Enter') askQuestion();
        }

        function appendMessage(sender, text) {
            const chat = document.getElementById("chatContainer");
            const msgDiv = document.createElement("div");
            msgDiv.className = "message " + (sender === "user" ? "user-message" : "ai-message");
            
            // Format bold text from markdown (**text**)
            let formattedText = text.replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
            formattedText = formattedText.replace(/\\n/g, '<br>');
            
            msgDiv.innerHTML = formattedText;
            chat.appendChild(msgDiv);
            window.scrollTo(0, document.body.scrollHeight);
        }

        async function askQuestion() {
            const inputField = document.getElementById("questionInput");
            const question = inputField.value.trim();
            const loader = document.getElementById("loader");

            if(!question) return;

            inputField.value = "";
            appendMessage("user", question);

            document.getElementById("chatContainer").appendChild(loader);
            loader.style.display = "block";
            window.scrollTo(0, document.body.scrollHeight);

            try {
                const response = await fetch("/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: question })
                });
                const data = await response.json();
                
                loader.style.display = "none";
                appendMessage("ai", data.answer);
            } catch (error) {
                loader.style.display = "none";
                appendMessage("ai", "Oops! Network error. Please try again.");
            }
        }
    </script>
</body>
</html>
    """

@app.route("/ask", methods=["POST"])
def ask():
    try:
        if not client:
            return jsonify({"answer": "Error: API Key is missing in Render Environment."})

        data = request.get_json()
        user_question = data.get("question", "")
        
        if not user_question:
            return jsonify({"answer": "Empty question."})

        # PRO TRICK: Bulletproof Fallback Mechanism
        try:
            # Plan A: Try the absolute latest 2.0 model
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=user_question,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                )
            )
        except Exception as e1:
            try:
                # Plan B: Agar naya model nahi mila, toh universal fallback model
                response = client.models.generate_content(
                    model='gemini-1.5-flash-latest',
                    contents=user_question,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction
                    )
                )
            except Exception as e2:
                # Agar sab fail ho jaye, error print karo UI par
                return jsonify({"answer": f"API Error: Both models failed. Details: {str(e1)}"})
        
        return jsonify({"answer": response.text})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"answer": f"System Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
