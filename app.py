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
    <html>
    <head>
        <title>NEET AI</title>

        <meta name="google-site-verification" content="wybgsv_hqeY1D-qeSDFGhC-DBitKnWUqre9QoDi9CdU" />

    </head>
    <body style="text-align:center; font-family:Arial; margin-top:50px;">

        <h2>NEET AI 🤖</h2>

        <form method="POST">
            <input name="question" placeholder="Apna question likho" style="padding:10px; width:250px;">
            <button type="submit">Pucho</button>
        </form>

        <h3>Answer:</h3>
        <p>{answer}</p>

    </body>
    </html>
    """


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
