# SymPyServer

SymPy REST API server using Falcon framework.

# Install and run

Run this in cmd.exe:

	python -m venv venv
	venv\Scripts\activate
	pip install -r requirements.txt
	py sympy_server.py

Ctrl+C to quit.

The virtual Python environment keeps your project packages with the project. To leave it, use:

	venv\Scripts\deactivate

# Use

Enter SymPy queries via your browser: http://localhost:8000/sympy?q=Intersection(*[solveset(p,%20x,%20S.Reals)%20for%20p%20in%20[(x%20%3E%204.0000),%20(x%20%3C%2068.0000)]])
