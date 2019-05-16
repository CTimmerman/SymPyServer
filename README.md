# SymPyServer

SymPy REST API server using Falcon framework.

# Installation

Run this in cmd.exe:

	mklink /J C:\Python36 C:\Users\name\AppData\Local\Programs\Python\Python36
	c:\Python36\python.exe -m venv SymPyServer
	cd SymPyServer
	Scripts\activate
	pip install -r requirements.txt
	py sympy_server.py

Venv keeps your project packages with the project.

# Usage

http://localhost:8000/sympy?q=Intersection(*[solveset(p,%20x,%20S.Reals)%20for%20p%20in%20[(x%20%3E%204.0000),%20(x%20%3C%2068.0000)]])