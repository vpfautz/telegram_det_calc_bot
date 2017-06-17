import re
import json


def parse_matrix_std(text, colsep, rowsep):
	rowreg = "\s*\d+(\s*%s\s*\d+)*\s*" % colsep
	reg = "^%s(%s%s)*$" % (rowreg, rowsep, rowreg)
	a = re.search(reg, text, re.DOTALL)
	if a is None:
		return None

	text = text.strip()
	while colsep*2 in text:
		text = text.replace(colsep*2, colsep)
	while rowsep*2 in text:
		text = text.replace(rowsep*2, rowsep)
	while "  " in text:
		text = text.replace("  ", " ")

	return map(lambda x:map(lambda y:int(y.strip()), x.strip().split(colsep)), text.split(rowsep))

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
	a = re.search("^\s*\[\s*\d+(\s*,\s*\d+)*\s*\](\s*,\s*\[\s*\d+(\s*,\s*\d+)*\s*\])*\s*$", text, re.DOTALL)
	if a is None:
		text = text.strip()
		if text[0] == "[" and text[-1] == "]":
			return parse_matrix_brackets(text[1:-1].strip())
		else:
			return None

	text = text.strip().replace(" ", "")
	return json.loads("[%s]" % text)

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


if __name__ == '__main__':
	test()
