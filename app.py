from flask import Flask, request, render_template_string

app = Flask(__name__)

neet_data = {
    "dna": "DNA genetic material hota hai jo hereditary information carry karta hai.",
    "cell": "Cell jeev ka basic structural aur functional unit hota hai."
}

html = """
<h2>NEET AI Assistant 🤖</h2>
<form method="post">
<input name="question" placeholder="Apna question likho">
<button type="submit">Ask</button>
</form>

{% if answer %}
<p><b>Answer:</b> {{answer}}</p>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def home():
    answer = ""
    if request.method == "POST":
        q = request.form["question"].lower()
        for key in neet_data:
            if key in q:
                answer = neet_data[key]
    return render_template_string(html, answer=answer)

# IMPORTANT 🔥
if __name__ == "__main__":
    app.run()
