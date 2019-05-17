"""SymPy server by Cees Timmerman, 2019-05-16.
Inspired by https://stackoverflow.com/questions/56155624/speeding-up-python-c-call/
"""
import re

import falcon

def eval_sympy(q):
	"""
	Handle stuff like:
	>>> eval_sympy("Intersection(*[solveset(p, x, S.Reals) for p in [(x > 4.0000), (x < 6.0000), (((x) * 4.0000 + 5.0000) > 5.0000)]])")
	Interval.open(4.00000000000000, 6.00000000000000)
	>>> eval_sympy("Intersection(*[solveset(p, x, S.Reals) for p in [(x > 4.0000), (x < 6.0000), ((x * (Min(Max(x, 4.0000), 5.0000))) > 7.0000), ((Min(Max(x, 4.0000), 5.0000)) > 5.0000)]])")
	EmptySet()
	>>> eval_sympy("")
	'ERR: unexpected EOF while parsing (<string>, line 0)'
	>>> eval_sympy("Min(p)")
	"ERR: name 'p' is not defined"
	>>> eval_sympy("1/0")
	'ERR: division by zero'
	>>> eval_sympy("__import__('os').system('clear')")
	'Unauthorized string.'
	>>> eval_sympy("().__class__.__bases__[0]")
	'Unauthorized string.'
	
	https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
	"""
	from sympy import Intersection, solveset, S
	from sympy.abc import x
	from sympy.functions.elementary.miscellaneous import Min, Max

	# Whitelist allowed strings.
	if not re.match("^([ \d.,<>\[\]()*\/+-]|for|in|Intersection|solveset|S|x|Min|Max|p|Reals)*$", q):
		return "Unauthorized string."
	# Blacklist builtins.
	env = {k:v for (k,v) in locals().items() if not '_' in k}
	try:
		return eval(q, env)
	except Exception as err:
		return "ERR: {}".format(err)

class SymPyResource:
	def on_get(self, req, resp):
		q = req.params["q"]
		result = {"result": "%s" % eval_sympy(q)}
		resp.media = result

api = falcon.API()
api.add_route('/sympy', SymPyResource())

if __name__ == '__main__':
	import sys
	if "test" in sys.argv:
		import doctest
		print(doctest.testmod())
		sys.exit(2)

	from wsgiref import simple_server
	httpd = simple_server.make_server('127.0.0.1', 8000, api)
	httpd.serve_forever()