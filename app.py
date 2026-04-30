from flask import Flask, request, jsonify
import os
from google import genai
from google.genai import types

app = Flask(__name__)

# ===== GEMINI API SETUP =====
API_KEY = os.environ.get("GEMINI_API_KEY")
# Naye SDK mein connection ko bilkul simple rakhte hain
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
    # Tumhara wahi shaandaar Dark Mode UI jo tumne banaya tha
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dr. Nikhil MBBS AI</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
        body { margin: 0; font-family: 'Inter', sans-serif; background-color: #212121; color: #ececf1; display: flex; flex-direction: column; height: 100vh; }
        .header { display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; border-bottom: 1px solid #333; position: sticky; top: 0; background: #212121; z-index: 10; }
        .title { font-weight: 600; font-size: 18px; display: flex; align-items: center; gap: 8px; }
        .badge { background: #007bff; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; }
        .chat-container { flex: 1; overflow-y: auto; padding: 20px 10%; display: flex; flex-direction: column; gap: 24px; padding-bottom: 120px; }
        .message { max-width: 85%; padding: 12px 18px; border-radius: 15px; line-height: 1.6; font-size: 16px; }
        .user-message { background-color: #2f2f2f; align-self: flex-end; border-bottom-right-radius: 4px; }
        .ai-message { background-color: transparent; align-self: flex-start; }
        .mystic-loader { display: none; align-self: flex-start; width: 30px; height: 30px; position: relative; margin-left: 20px; }
        .mystic-loader::before { content: ''; position: absolute; width: 100%; height: 100%; border-radius: 50%; border: 2px solid transparent; border-top-color: #007bff; animation: spin 1s infinite linear; }
        @keyframes spin { 100% { transform: rotate(360deg); } }
        .input-wrapper { position: fixed; bottom: 0; width: 100%; padding: 20px; display: flex; justify-content: center; background: linear-gradient(180deg, rgba(33,33,33,0) 0%, rgba(33,33,33,1) 30%); }
        .input-box { display: flex; align-items: center; background-color: #2f2f2f; border-radius: 30px; padding: 8px 15px; width: 100%; max-width: 800px; box-shadow: 0 0 15px rgba(0,0,0,0.5); }
        input { flex: 1; background: transparent; border: none; outline: none; font-size: 16px; color: inherit; padding: 10px; }
        .send-btn { background-color: #fff; color: #000; border-radius: 50%; width: 35px; height: 35px; display: flex; justify-content: center; align-items: center; cursor: pointer; border: none; }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">🩺 Dr. Nikhil MBBS <span class="badge">NEET AI</span></div>
    </div>
    <div class="chat-container" id="chatContainer">
        <div class="message ai-message">Swagat hai Dr. Nikhil! Aaj kaunsa concept clear karna hai?</div>
    </div>
    <div class="mystic-loader" id="loader"></div>
    <div class="input-wrapper">
        <div class="input-box">
            <input type="text" id="questionInput" placeholder="Message NEET AI..." onkeypress="handleEnter(event)">
            <button class="send-btn" onclick="askQuestion()">➤</button>
        </div>
    </div>
    <script>
        function handleEnter(e) { if(e.key === 'Enter') askQuestion(); }
        async function askQuestion() {
            const inputField = document.getElementById("questionInput");
            const question = inputField.value.trim();
            if(!question) return;
            const chat = document.getElementById("chatContainer");
            const loader = document.getElementById("loader");
            
            const userDiv = document.createElement("div");
            userDiv.className = "message user-message";
            userDiv.innerText = question;
            chat.appendChild(userDiv);
            
            inputField.value = "";
            loader.style.display = "block";
            chat.appendChild(loader);
            chat.scrollTop = chat.scrollHeight;

            try {
                const response = await fetch("/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: question })
                });
                const data = await response.json();
                loader.style.display = "none";
                const aiDiv = document.createElement("div");
                aiDiv.className = "message ai-message";
                aiDiv.innerHTML = data.answer.replace(/\\n/g, '<br>').replace(/\\*\\*(.*?)\\*\\*/g, '<strong>$1</strong>');
                chat.appendChild(aiDiv);
                chat.scrollTop = chat.scrollHeight;
            } catch (error) {
                loader.style.display = "none";
                alert("Network error bhai!");
            }
        }
    </script>
</body>
</html>
    """

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "")

        # YAHAN HAI MAIN FIX: 
        # Hum bina kisi version ke seedha stable model use karenge
        response = client.models.generate_content(
            model='gemini-1.5-flash', 
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        )
        return jsonify({"answer": response.text})
        
    except Exception as e:
        # Agar wo fail ho, toh yeh loop saare available models try karega
        print(f"Primary Model Failed: {e}")
        try:
            # Fallback for some specific API regions
            response = client.models.generate_content(
                model='gemini-1.5-flash-8b', 
                contents=question,
                config=types.GenerateContentConfig(system_instruction=system_instruction)
            )
            return jsonify({"answer": response.text})
        except Exception as e2:
            return jsonify({"answer": f"Bhai, Google API model dhoond nahi paa rahi. Error: {str(e2)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
