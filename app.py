from flask import Flask, request
import os

app = Flask(__name__)

# ---------------- DATA ----------------
data = {
    "dna kya hai": "DNA genetic material hota hai jo hereditary information carry karta hai.",
    "cell kya hai": "Cell life ka basic unit hota hai.",
    "photosynthesis kya hai": "Plants sunlight se food banate hain."
}

mcq = {
    "dna": {
        "q": "DNA ka full form kya hai?",
        "options": ["A. Dynamic Network Analysis", "B. Deoxyribonucleic Acid", "C. Data Node Access", "D. None"],
        "answer": "B"
    }
}

# ---------------- ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    mcq_html = ""

    question = ""

    if request.method == "POST":
        question = request.form.get("question", "").lower()
        answer = data.get(question, "Topic not found in NEET AI 😄")

        # MCQ trigger
        if "mcq" in question:
            m = mcq["dna"]
            mcq_html = f"""
            <h3>📚 MCQ Practice</h3>
            <p>{m['q']}</p>
            <ul>
                <li>{m['options'][0]}</li>
                <li>{m['options'][1]}</li>
                <li>{m['options'][2]}</li>
                <li>{m['options'][3]}</li>
            </ul>
            <p><b>Answer:</b> {m['answer']}</p>
            """

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>NEET AI</title>

<style>
body {{
    margin:0;
    font-family: Arial;
    background: linear-gradient(to bottom, #87CEEB, #ffffff);
    transition: 0.5s;
}}

.dark-mode {{
    background: #121212;
    color: white;
}}

.header {{
    text-align:center;
    padding:20px;
    background: rgba(255,255,255,0.7);
}}

.title {{
    font-size:30px;
    font-weight:bold;
}}

.box {{
    text-align:center;
    margin-top:40px;
}}

input {{
    padding:10px;
    width:60%;
}}

button {{
    padding:10px 15px;
    background:#007bff;
    color:white;
    border:none;
}}

.clouds {{
    position:absolute;
    width:100%;
    height:100px;
    background:url('https://i.imgur.com/f6QbKQm.png');
    animation: move 20s linear infinite;
}}

@keyframes move {{
    from {{background-position:0;}}
    to {{background-position:1000px;}}
}}

footer {{
    text-align:center;
    margin-top:50px;
    font-size:12px;
}}

</style>
</head>

<body>

<div class="header">
    <div class="title">🧠 NEET AI</div>
    <button onclick="toggleDark()">🌙 Dark Mode</button>
    <button onclick="startVoice()">🎤 Voice</button>
</div>

<div class="clouds"></div>

<div class="box">
    <form method="POST">
        <input name="question" id="q" placeholder="Ask NEET question">
        <button type="submit">Pucho</button>
    </form>

    <h3>Answer:</h3>
    <p>{answer}</p>

    {mcq_html}
</div>

<footer>
    © 2026 NEET AI | DR.NIKHIL MBBS
</footer>

<script>

// DARK MODE
function toggleDark() {{
    document.body.classList.toggle("dark-mode");
}}

// VOICE INPUT
function startVoice() {{
    let recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.onresult = function(event) {{
        document.getElementById("q").value = event.results[0][0].transcript;
    }}
    recognition.start();
}}

</script>

</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
