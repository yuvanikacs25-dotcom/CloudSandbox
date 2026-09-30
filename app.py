from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
	return render_template("index.html")


@app.route("/login")
def login():
	return render_template("login.html")


@app.route("/editor")
def editor():
	return render_template("editor.html")


@app.route("/run", methods=["POST"])
def run_code():
	data = request.get_json(silent=True) or {}
	code = data.get("code", "")

	return jsonify({
        "output": "Code received successfully!"
    })

if __name__ == "__main__":
    app.run(debug=True)
