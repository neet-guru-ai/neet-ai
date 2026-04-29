from flask import Flask, request
import os

app = Flask(__name__)

# ---------------- NEET DATA ----------------
data = {
    "dna kya hai": "DNA genetic material hota hai jo hereditary information carry karta hai.",
    "cell kya hai": "Cell life ka basic unit hota hai.",
    "photosynthesis kya hai": "Plants sunlight se food banate hain."
}

# ---------------- HOME PAGE ----------------
@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""

    if request.method == "POST":
        q = request.form.get("question", "").lower()
        answer = data.get(q, "Topic not found in NEET AI 😄")

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>NEET AI</title>

<style>
body {{
    margin:0;
    font-family: Arial;
    background: white;
    color: black;
    transition: 0.3s;
}}

.dark-mode {{
    background: black;
    color: white;
}}

.header {{
    text-align:center;
    padding:20px;
    background: #f2f2f2;
}}

.title {{
    font-size:28px;
    font-weight:bold;
}}

.box {{
    text-align:center;
    margin-top:50px;
}}

input {{
    padding:12px;
    width:60%;
    border:1px solid #ccc;
    border-radius:8px;
}}

button {{
    padding:12px 18px;
    border:none;
    background:#007bff;
    color:white;
    border-radius:8px;
    cursor:pointer;
}}

button:hover {{
    background:#0056b3;
}}

.answer {{
    margin-top:20px;
    font-size:18px;
}}

</style>
</head>

<body>

<div class="header">
    <div class="title">🧠 NEET AI</div>
    <p>DR.NIKHIL MBBS</p>

    <button onclick="toggleDark()">🌙 Dark Mode</button>
</div>

<div class="box">

    <form method="POST">
        <input name="question" placeholder="NEET question likho">
        <button type="submit">Pucho</button>
    </form>

    <h3>Answer:</h3>
    <p class="answer">{answer}</p>

</div>

<script>

// DARK MODE
function toggleDark() {{
    document.body.classList.toggle("dark-mode");
}}

// CLICK SOUND
document.addEventListener("click", function() {{
    let audio = new Audio("https://www.soundjay.com/buttons/sounds/button-16.mp3");
    audio.play();
}});

</script>

</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
