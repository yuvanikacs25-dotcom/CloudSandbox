from flask import Flask, jsonify, render_template, request
from RestrictedPython import compile_restricted, safe_globals
from RestrictedPython.PrintCollector import PrintCollector

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

	if not isinstance(code, str) or not code.strip():
		return jsonify({"output": "Please enter some Python code."})

	try:
		compiled_code = compile_restricted(
			code,
			filename="<user_code>",
			mode="exec",
		)

		execution_globals = safe_globals.copy()
		execution_globals["_print_"] = PrintCollector
		execution_locals = {}

		exec(compiled_code, execution_globals, execution_locals)

		output = execution_locals.get("_print")
		if output is None:
			output = execution_globals.get("_print")
		if output is not None:
			output = output()

		if not output:
			output = "Code executed successfully."

		return jsonify({"output": output})

	except SyntaxError as e:
		return jsonify({"output": f"Syntax Error: {e}"})
	except Exception as e:
		return jsonify({"output": f"Error: {e}"})


if __name__ == "__main__":
	app.run(debug=True)
