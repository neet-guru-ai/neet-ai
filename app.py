from flask import Flask, request

app = Flask(__name__)

# Simple NEET AI answers
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
    if request.method == "POST":
        question = request.form.get("question").lower()
        answer = data.get(question, "Yeh topic abhi mere NEET database me nahi hai 😄")
        
       return f"""
        <h2>NEET AI 🤖</h2>
        <form method="POST">
            <input name="question" placeholder="Apna question likho">
            <button type="submit">Pucho</button>
        </form>
        <p><b>Answer:</b> {answer}</p>
        """
    
    return """
    <h2>NEET AI 🤖</h2>
    <form method="POST">
        <input name="question" placeholder="Apna question likho">
        <button type="submit">Pucho</button>
    </form>
    """
# FINAL FIX (Render ke liye)
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
