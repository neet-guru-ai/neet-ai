from flask import Flask, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# ===== GEMINI API SETUP =====
# Render dashboard me 'GEMINI_API_KEY' naam ka Environment Variable banana zaroori hai
API_KEY = os.environ.get("GEMINI_API_KEY", "apna_gemini_api_key_yahan_daalein_agar_env_me_nahi_hai")
genai.configure(api_key=API_KEY)

# Strict System Prompt taaki AI sirf NEET/NCERT ke scope me rahe
system_instruction = """
You are a highly advanced NEET Expert AI. 
Strictly answer questions related to NCERT Biology, Physics, and Chemistry for Class 11 and 12.
Provide clear, concise, and highly accurate answers suitable for a NEET aspirant.
If the user asks something completely outside of studies or science, politely decline and ask them to focus on NEET topics.
Use a mix of Hindi and English (Hinglish) if the user asks in Hinglish, otherwise reply in English.
"""

model = genai.GenerativeModel(
    'gemini-1.5-flash',
    system_instruction=system_instruction
)

# ===== ROUTES =====
@app.route("/")
def home():
    # Ye tumhara naya Fully Animated Professional UI hai
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEET AI | Advanced</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

        /* ===== BASE THEME ===== */
        body {
            margin: 0;
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            color: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* ===== HEADER ===== */
        .header {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 40px;
            box-sizing: border-box;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }

        .title {
            font-size: 24px;
            font-weight: 600;
            background: -webkit-linear-gradient(#00f7ff, #007bff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* ===== MAIN CONTAINER (GLASSMORPHISM) ===== */
        .container {
            margin-top: 50px;
            width: 90%;
            max-width: 600px;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            animation: fadeIn 1s ease-out;
        }

        /* ===== INPUT SECTION ===== */
        .input-group {
            position: relative;
            margin-bottom: 20px;
        }

        input {
            width: 100%;
            padding: 15px 20px;
            font-size: 16px;
            border-radius: 12px;
            border: 2px solid transparent;
            background: rgba(0, 0, 0, 0.3);
            color: white;
            box-sizing: border-box;
            transition: 0.3s all;
            font-family: 'Poppins', sans-serif;
        }

        input:focus {
            border: 2px solid #00f7ff;
            outline: none;
            box-shadow: 0 0 15px rgba(0, 247, 255, 0.5);
            background: rgba(0, 0, 0, 0.5);
        }

        /* ===== BUTTON ===== */
        button {
            width: 100%;
            padding: 15px;
            border: none;
            background: linear-gradient(90deg, #007bff, #00f7ff);
            color: white;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.3s;
            box-shadow: 0 5px 15px rgba(0, 123, 255, 0.4);
            font-family: 'Poppins', sans-serif;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0, 123, 255, 0.6);
        }

        button:active {
            transform: translateY(1px);
        }

        /* ===== ANSWER AREA ===== */
        .answer-box {
            margin-top: 30px;
            padding: 20px;
            background: rgba(0, 0, 0, 0.2);
            border-left: 4px solid #00f7ff;
            border-radius: 10px;
            font-size: 16px;
            line-height: 1.6;
            display: none; /* Hidden by default */
            animation: slideUp 0.5s ease-out;
        }

        /* ===== LOADING ANIMATION ===== */
        .loader {
            display: none;
            text-align: center;
            margin-top: 20px;
        }
        
        .dot {
            height: 12px;
            width: 12px;
            margin: 0 5px;
            background-color: #00f7ff;
            border-radius: 50%;
            display: inline-block;
            animation: bounce 1.4s infinite ease-in-out both;
        }

        .dot:nth-child(1) { animation-delay: -0.32s; }
        .dot:nth-child(2) { animation-delay: -0.16s; }

        /* ===== KEYFRAMES ===== */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes slideUp {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }

    </style>
</head>
<body>

    <div class="header">
        <div class="title">🧬 NEET AI</div>
    </div>

    <div class="container">
        <div class="input-group">
            <input type="text" id="questionInput" placeholder="Apna NEET/NCERT question pucho..." onkeypress="handleEnter(event)">
        </div>
        <button onclick="askQuestion()">Pucho AI Se 🚀</button>

        <!-- Loading Dots -->
        <div class="loader" id="loader">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>

        <!-- Answer Display -->
        <div class="answer-box" id="answerBox">
            <strong style="color: #00f7ff;">AI Response:</strong>
            <div id="answerText" style="margin-top: 10px;"></div>
        </div>
    </div>

    <script>
        function handleEnter(e) {
            if(e.key === 'Enter'){
                askQuestion();
            }
        }

        async function askQuestion() {
            const inputField = document.getElementById("questionInput");
            const question = inputField.value.trim();
            const answerBox = document.getElementById("answerBox");
            const answerText = document.getElementById("answerText");
            const loader = document.getElementById("loader");

            if(!question) {
                alert("Bhai, pehle koi question toh likho!");
                return;
            }

            // Play a soft click sound
            new Audio("https://www.soundjay.com/buttons/sounds/button-16.mp3").play().catch(e => {});

            // Show loader, hide previous answer
            loader.style.display = "block";
            answerBox.style.display = "none";
            
            try {
                // Bina page refresh kiye backend se connect kar rahe hain
                const response = await fetch("/ask", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ question: question })
                });

                const data = await response.json();
                
                // Hide loader, show answer
                loader.style.display = "none";
                answerText.innerHTML = data.answer.replace(/\\n/g, '<br>'); // Handle new lines
                answerBox.style.display = "block";

            } catch (error) {
                loader.style.display = "none";
                answerText.innerHTML = "Oops! Server se connect nahi ho paaya. Thodi der baad try karo.";
                answerBox.style.display = "block";
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
        user_question = data.get("question", "")
        
        if not user_question:
            return jsonify({"answer": "Empty question."})

        # Gemini API call
        response = model.generate_content(user_question)
        
        return jsonify({"answer": response.text})
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"answer": "Sorry bhai, API limit cross ho gayi ya network issue hai. Error logged."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
