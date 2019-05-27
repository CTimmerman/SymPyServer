"""SymPy server by Cees Timmerman, 2019-05-16.
Inspired by https://stackoverflow.com/questions/56155624/speeding-up-python-c-call/
"""
import re

import falcon


whitelist = re.compile("(?:[ \d.,<>\[\]()*\/+-]|for|in|Intersection|solveset|S|x|Min|Max|p|Reals)+")

def eval_sympy(q):
	"""
	Handle stuff like:
	>>> eval_sympy("Intersection(*[solveset(p, x, S.Reals) for p in [(x > 4.0000), (x < 6.0000), (((x) * 4.0000 + 5.0000) > 5.0000)]])")
	Interval.open(4.00000000000000, 6.00000000000000)
	>>> eval_sympy("Intersection(*[solveset(p, x, S.Reals) for p in [(x > 4.0000), (x < 6.0000), ((x * (Min(Max(x, 4.0000), 5.0000))) > 7.0000), ((Min(Max(x, 4.0000), 5.0000)) > 5.0000)]])")
	EmptySet()
	>>> eval_sympy("")
	"Unauthorized string(s): ''"
	>>> eval_sympy("Min(p)")
	"ERR: name 'p' is not defined"
	>>> eval_sympy("1/0")
	'ERR: division by zero'
	>>> eval_sympy("__import__('os').system('clear')")
	'Unauthorized string(s): "__im ort__ \\'os\\' system \\'clear\\' "'
	>>> eval_sympy("().__class__.__bases__[0]")
	"Unauthorized string(s): ' __class__ __bases__ '"
	>>> eval_sympy("Max(evil), Min(good)")
	"Unauthorized string(s): ' evil good '"
	
	https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
	"""
	from sympy import Intersection, solveset, S
	from sympy.abc import x
	from sympy.functions.elementary.miscellaneous import Min, Max
	# Whitelist allowed strings.
	if not re.fullmatch(whitelist, q):
		return "Unauthorized string(s): %r" % re.sub(whitelist, " ", q)
	# Blacklist builtins.
	env = {k:v for (k,v) in locals().items() if not '_' in k}
	try:
		return eval(q, env)
	except Exception as err:
		return "ERR: {}".format(err)

def test_performance():
	"""Best of 5:
	Python 3.7:
	local sympy imports: 9.31 s
	global sympy imports: 9.24 s
	PyPy 3.6-7.1.1-beta0:
	local sympy imports: 22.93 s
	global sympy imports: 23.55 s
	"""
	import timeit
	return timeit.timeit("""eval_sympy("Intersection(*[solveset(p, x, S.Reals) for p in [(x > 4.0000), (x < 6.0000), ((x * (Min(Max(x, 4.0000), 5.0000))) > 7.0000), ((Min(Max(x, 4.0000), 5.0000)) > 5.0000)]])")""", number=10, globals=globals())

class SymPyResource:
	def on_get(self, req, resp):
		"""
		>>> from falcon import testing; client = testing.TestClient(api)
		>>> r = client.simulate_get('/sympy'); r.status_code
		200
		>>> r.json
		{'result': "ERR: No 'q' parameter."}
		>>> client.simulate_get('/sympy?q=Max(1, 2)').json
		{'result': '2'}
		"""
		#q = req.get_param('q', required=True)  # Returns <error><title>Missing parameter</title><description>The "q" parameter is required.</description></error>
		if 'q' in req.params:
			q = str(req.params['q'])
			result = {"result": "%s" % eval_sympy(q)}
		else:
			result = {"result": "ERR: No 'q' parameter."}
		
		resp.media = result

api = falcon.API()
api.add_route('/sympy', SymPyResource())

if __name__ == '__main__':
	import sys
	if "test" in sys.argv:
		import doctest
		result = doctest.testmod(optionflags=doctest.FAIL_FAST if "fast" in sys.argv else 0)  # Optionally stop testing after a single failure.
		print(result)
		if "perf" in sys.argv:
			seconds = test_performance()
			print("%ss" % seconds)
			sys.exit(seconds > 1)
		
		sys.exit(1 if result.failed else 0)
		
	from wsgiref import simple_server
	httpd = simple_server.make_server('127.0.0.1', 8000, api)
	print("Serving on http://%s:%s/sympy" % httpd.socket.getsockname())
	httpd.serve_forever()