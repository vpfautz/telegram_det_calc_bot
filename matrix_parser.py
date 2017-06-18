import re
import json
import re
import sympy


elem_reg = "-?(?:\d+\.\d+|\d+|\d+/\d+|pi|[a-zA-Z]+)"

def parse_element(s):
	s = s.strip()
	if s.startswith("-"):
		return -parse_element(s[1:])
	if s.lower() == "pi":
		return sympy.pi

	sym = re.search("^([a-zA-Z]+)$", s)
	if not sym is None:
		return sympy.Symbol(sym.group(1))

	frac = re.search("^(%s)/(%s)$" % (elem_reg, elem_reg), s)
	if not frac is None:
		return sympy.Rational(parse_element(frac.group(1)), parse_element(frac.group(2)))

	sym = re.search("^(\d+)$", s)
	if not sym is None:
		return int(sym.group(1))

	try:
		return sympy.Rational(s)
	except Exception as e:
		print "Can't parse element: '%s'" % s


def parse_matrix_std(text, colsep, rowsep):
	rowreg = "\s*%s+(\s*%s\s*%s+)*\s*" % (elem_reg, colsep, elem_reg)
	reg = "^%s(%s%s)*$" % (rowreg, rowsep, rowreg)
	a = re.search(reg, text, re.DOTALL|re.IGNORECASE)
	if a is None:
		return None

	text = text.strip()
	while colsep*2 in text:
		text = text.replace(colsep*2, colsep)
	while rowsep*2 in text:
		text = text.replace(rowsep*2, rowsep)
	while "  " in text:
		text = text.replace("  ", " ")

	return map(lambda x:map(parse_element, x.strip().split(colsep)), text.split(rowsep))

def parse_matrix_std_brute(text):
	seperators = [" ", "\n", "\t", ",", ";"]
	for colsep in seperators:
		for rowsep in seperators:
			if colsep == rowsep:
				continue

			r = parse_matrix_std(text, colsep, rowsep)
			if not r is None and check_dim(r):
				return r


# def parse_matrix_space_nl(text):
# 	return parse_matrix_std(text, " ", "\n")
	# a = re.search("^\s*\d+( +\d+ *)*(\n\s*\d+( +\d+)* *)*\s*$", text, re.DOTALL)
	# if a is None:
	# 	return None

	# text = text.strip()
	# while "  " in text:
	# 	text = text.replace("  ", " ")

	# return map(lambda x:map(lambda y:int(y.strip()), x.strip().split(" ")), text.split("\n"))

# def parse_matrix_space_coma(text):
# 	return parse_matrix_std(text, " ", ",")
	# a = re.search("^ *\d+( +\d+ *)*(, *\d+( +\d+)* *)* *$", text, re.DOTALL)
	# if a is None:
	# 	return None

	# text = text.strip()
	# while "  " in text:
	# 	text = text.replace("  ", " ")

	# return map(lambda x:map(lambda y:int(y.strip()), x.strip().split(" ")), text.split(","))

def parse_matrix_brackets(text):
	row_reg = "\s*\[\s*%s+(\s*,\s*%s+)*\s*\]\s*" % (elem_reg, elem_reg)
	a = re.search("^%s(,%s)*$" % (row_reg, row_reg), text, re.DOTALL|re.IGNORECASE)
	if a is None:
		text = text.strip()
		if text[0] == "[" and text[-1] == "]":
			return parse_matrix_brackets(text[1:-1].strip())
		else:
			return None

	text = text.strip().replace(" ", "").replace("\n", "")
	text = text.replace("\r", "").replace("\t", "")

	rowsep = "],["
	colsep = ","
	text = text[1:-1]
	return map(lambda x:map(parse_element, x.strip().split(colsep)), text.split(rowsep))

def parseMatrix(text):
	ops = [
		parse_matrix_brackets,
		parse_matrix_std_brute
	]

	for op in ops:
		r = op(text)
		if not r is None:
			return r

def check_dim(m):
	first_length = len(m[0])
	for l in m:
		if len(l) != first_length:
			return False

	return True


def test():
	a = """1 2
	3 4"""
	# assert(parse_matrix_space_nl(a) == [[1,2],[3,4]])
	assert(parseMatrix(a) == [[1,2],[3,4]])
	a = """1 2 3
	4 5 6
	7 8 9"""
	# assert(parse_matrix_space_nl(a) == [[1,2,3],[4,5,6],[7,8,9]])
	assert(parseMatrix(a) == [[1,2,3],[4,5,6],[7,8,9]])
	a = """ 1 2 
	3   4 
	"""
	# assert(parse_matrix_space_nl(a) == [[1,2],[3,4]])
	assert(parse_matrix_std(a, " ", "\n") == [[1,2],[3,4]])
	assert(parseMatrix(a) == [[1,2],[3,4]])

	a = "1 2,3 4"
	# assert(parse_matrix_space_coma(a) == [[1,2],[3,4]])
	assert(parseMatrix(a) == [[1,2],[3,4]])
	a = "1 2 3,4 5 6, 7 8 9"
	# assert(parse_matrix_space_coma(a) == [[1,2,3],[4,5,6],[7,8,9]])
	assert(parseMatrix(a) == [[1,2,3],[4,5,6],[7,8,9]])
	a = " 1 2,3   4 "
	# assert(parse_matrix_space_coma(a) == [[1,2],[3,4]])
	assert(parseMatrix(a) == [[1,2],[3,4]])


	a = "[[1,2],[3,4]]"
	assert(parse_matrix_brackets(a) == [[1,2],[3,4]])
	assert(parseMatrix(a) == [[1,2],[3,4]])
	a = "[[1,2,3],[4,5,6],[7,8,9]]"
	assert(parse_matrix_brackets(a) == [[1,2,3],[4,5,6],[7,8,9]])
	assert(parseMatrix(a) == [[1,2,3],[4,5,6],[7,8,9]])
	a = """[
	     [ 1, 2 ] ,
	    [3 ,4 ] 
	]
	"""
	assert(parse_matrix_brackets(a) == [[1,2],[3,4]])
	assert(parseMatrix(a) == [[1,2],[3,4]])
	a = "[1,2],[3,4]"
	assert(parse_matrix_brackets(a) == [[1,2],[3,4]])
	assert(parseMatrix(a) == [[1,2],[3,4]])
	a = "[1,2,3],[4,5,6],[7,8,9]"
	assert(parse_matrix_brackets(a) == [[1,2,3],[4,5,6],[7,8,9]])
	assert(parseMatrix(a) == [[1,2,3],[4,5,6],[7,8,9]])
	a = """[1 , 2],
	[3 , 4 ] """
	assert(parse_matrix_brackets(a) == [[1,2],[3,4]])
	assert(parseMatrix(a) == [[1,2],[3,4]])

	assert(parseMatrix("1 2,3 4") == [[1,2],[3,4]])
	assert(parseMatrix("1 2;3 4") == [[1,2],[3,4]])
	assert(parseMatrix("1,2 3,4") == [[1,2],[3,4]])
	assert(parseMatrix("1,2;3,4") == [[1,2],[3,4]])


	assert(parse_element("1") == 1)
	assert(parse_element("1.5") == 1.5)
	assert(parse_element("1/2") == .5)
	assert(parse_element("pi") == sympy.pi)
	assert(parse_element("x") == sympy.Symbol("x"))
	assert(parse_element("-1") == -1)
	assert(parse_element("-1.5") == -1.5)
	assert(parse_element("-1/2") == -.5)
	assert(parse_element("-pi") == -sympy.pi)
	assert(parse_element("-x") == -sympy.Symbol("x"))

	a = "1/2 2,pi 4"
	assert(parseMatrix(a) == [[0.5,2],[sympy.pi,4]])
	a = "1/2 -x,pi -4"
	assert(parseMatrix(a) == [[0.5,-sympy.Symbol("x")],[sympy.pi,-4]])
	a = "[1/2,2],[pi,4]"
	assert(parse_matrix_brackets(a) == [[0.5,2],[sympy.pi,4]])
	a = "[1/2,0.5],[pi,x]"
	assert(parse_matrix_brackets(a) == [[0.5,0.5],[sympy.pi,sympy.Symbol("x")]])

if __name__ == '__main__':
	test()
