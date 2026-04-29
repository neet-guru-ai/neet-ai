from flask import Flask, request
import os

app = Flask(__name__)

# ---------------- NEET DATA ----------------
data = {
    "dna kya hai": "DNA genetic material hota hai jo hereditary info carry karta hai.",
    "cell kya hai": "Cell life ka basic unit hota hai.",
    "photosynthesis kya hai": "Plants sunlight se food banate hain."
}

# ---------------- HOME ----------------
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

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>NEET AI</title>

<style>

/* ===== BASE THEME ===== */
body {{
    margin:0;
    font-family: Arial;
    background:#0f0f0f;
    color:white;
    max-width:480px;
    margin:auto;
    transition:0.3s;
}}

/* LIGHT MODE */
.light {{
    background:white;
    color:black;
}}

/* HEADER */
.header {{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:15px;
    background:#1a1a1a;
}}

.light .header {{
    background:#f2f2f2;
}}

.title {{
    font-size:20px;
    font-weight:bold;
}}

/* SETTINGS ICON */
.settings {{
    cursor:pointer;
    font-size:22px;
}}

/* BOX */
.box {{
    text-align:center;
    margin-top:40px;
    padding:10px;
}}

/* INPUT NEON EFFECT */
input {{
    width:90%;
    padding:14px;
    font-size:16px;
    border-radius:10px;
    border:2px solid #00f7ff;
    outline:none;
    background:transparent;
    color:inherit;
    box-shadow:0 0 10px #00f7ff;
}}

/* BUTTON */
button {{
    margin-top:10px;
    padding:12px 18px;
    border:none;
    background:#007bff;
    color:white;
    border-radius:8px;
    font-size:16px;
    cursor:pointer;
}}

/* ANSWER */
.answer {{
    margin-top:20px;
    font-size:18px;
    padding:10px;
}}

/* SETTINGS PANEL */
.panel {{
    position:fixed;
    top:50px;
    right:10px;
    background:#222;
    padding:10px;
    border-radius:10px;
    display:none;
}}

.light .panel {{
    background:#eee;
    color:black;
}}

.panel button {{
    display:block;
    width:100%;
    margin:5px 0;
}}

</style>
</head>

<body>

<!-- HEADER -->
<div class="header">
    <div class="title">🧠 NEET AI</div>
    <div class="settings" onclick="togglePanel()">⚙️</div>
</div>

<!-- SETTINGS PANEL -->
<div class="panel" id="panel">
    <button onclick="toggleTheme()">🌗 Theme</button>
    <button onclick="alert('MCQ Mode Coming Soon 🔥')">📚 MCQ</button>
    <button onclick="alert('Search Upgrade Coming Soon 🔍')">🔍 Search</button>
</div>

<!-- MAIN -->
<div class="box">

    <form method="POST">
        <input name="question" placeholder="NEET question likho">
        <br>
        <button type="submit">Pucho</button>
    </form>

    <div class="answer">
        <b>Answer:</b> {answer}
    </div>

</div>

<script>

/* SETTINGS PANEL */
function togglePanel() {{
    let p = document.getElementById("panel");
    p.style.display = (p.style.display === "block") ? "none" : "block";
}}

/* THEME TOGGLE */
function toggleTheme() {{
    document.body.classList.toggle("light");
}}

/* CLICK SOUND (OPTIONAL SAFE) */
document.addEventListener("click", function() {{
    let a = new Audio("https://www.soundjay.com/buttons/sounds/button-16.mp3");
    a.play();
}});

</script>

</body>
</html>
"""

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
