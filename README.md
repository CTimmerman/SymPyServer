# SymPyServer

SymPy REST API server using [Falcon](https://falconframework.org/).

## Install and run

In Ubuntu Bash:

	python3 -m venv venv
	source venv/bin/activate
	python3 -m pip install -r requirements.txt
	python3 sympy_server.py

In Windows Command Prompt:

	python -m venv venv
	venv\Scripts\activate
	pip install -r requirements.txt
	py sympy_server.py

Ctrl+C to quit.

The virtual Python environment keeps your project packages with the project. To leave it, use:

	deactivate
	
## Use

Enter SymPy queries via your browser, e.g.:

[http://localhost:8000/sympy?q=Intersection(*[solveset(p, x, S.Reals) for p in [(x > 4.0000), (x < 68.0000)]])](http://localhost:8000/sympy?q=Intersection(*[solveset(p,%20x,%20S.Reals)%20for%20p%20in%20[(x%20%3E%204.0000),%20(x%20%3C%2068.0000)]]))

Returns:

	{"result": "Interval.open(4.00000000000000, 68.0000000000000)"}
