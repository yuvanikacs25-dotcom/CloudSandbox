from flask import Flask, render_template, request, jsonify
import subprocess
import sys
import tempfile
import os

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

	if not isinstance(code, str):
		return jsonify({"output": "Code must be a string."}), 400
	if not code.strip():
		return jsonify({"output": "Please enter some code."})

	filename = None
	try:
		with tempfile.NamedTemporaryFile(
			mode="w", suffix=".py", delete=False, encoding="utf-8"
		) as file:
			file.write(code)
			filename = file.name

		result = subprocess.run(
			[sys.executable, filename],
			capture_output=True,
			text=True,
			timeout=5,
		)
		return jsonify({"output": result.stdout + result.stderr})

	except subprocess.TimeoutExpired:
		return jsonify({"output": "Execution timed out."})
	except Exception as e:
		return jsonify({"output": str(e)})
	finally:
		if filename and os.path.exists(filename):
			os.remove(filename)


if __name__ == "__main__":
	app.run(debug=True)
