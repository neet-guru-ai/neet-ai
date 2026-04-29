from flask import Flask, request
import os

app = Flask(__name__)

# NEET AI simple database
data = {
    "dna kya hai": "DNA genetic material hota hai jo hereditary information carry karta hai. Iska structure double helix hota hai.",
    "what is dna": "DNA is the genetic material that carries hereditary information. It has a double helix structure.",

    "cell kya hai": "Cell jeev ka basic structural aur functional unit hota hai.",
    "what is cell": "Cell is the basic structural and functional unit of life.",

    "photosynthesis kya hai": "Photosynthesis ek process hai jisme plants sunlight, CO2 aur water se glucose banate hain aur oxygen release karte hain.",
    "what is photosynthesis": "Photosynthesis is the process by which plants make food using sunlight, CO2, and water."
}


@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""

    if request.method == "POST":
        question = request.form.get("question")
        if question:
            question = question.lower()
            answer = data.get(question, "Yeh topic abhi mere NEET database me nahi hai 😄")

    return f"""
   return """
<!DOCTYPE html>
<html>
<head>
    <title>NEET AI - DR.NIKHIL MBBS</title>

    <style>
        body {
            margin: 0;
            font-family: Arial;
            background: linear-gradient(to bottom, #87CEEB, #ffffff);
        }

        .header {
            text-align: center;
            padding: 20px;
            background: rgba(255,255,255,0.6);
            backdrop-filter: blur(10px);
        }

        .title {
            font-size: 32px;
            font-weight: bold;
            margin: 0;
        }

        .subtitle {
            margin: 0;
            font-size: 14px;
            color: #333;
        }

        .box {
            text-align: center;
            margin-top: 40px;
        }

        input {
            padding: 12px;
            width: 60%;
            border-radius: 10px;
            border: 1px solid #ccc;
        }

        button {
            padding: 12px 20px;
            border: none;
            background: #007bff;
            color: white;
            border-radius: 10px;
            cursor: pointer;
        }

        button:hover {
            background: #0056b3;
        }

        .answer {
            margin-top: 20px;
            font-size: 18px;
        }
    </style>
</head>

<body>

<div class="header">
    <div class="title">🧠 NEET AI</div>
    <div class="subtitle">DR.NIKHIL MBBS</div>
</div>

<div class="box">
    <form method="POST">
        <input name="question" placeholder="Apna NEET question likho">
        <button type="submit">Pucho 🎤</button>
    </form>

    {% if answer %}
    <div class="answer">
        <b>Answer:</b> {{answer}}
    </div>
    {% endif %}
</div>

</body>
</html>
"""


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
