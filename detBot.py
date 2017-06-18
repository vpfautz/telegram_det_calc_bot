import telepot
from telepot.loop import MessageLoop
import time
import numpy as np
from matrix_parser import parseMatrix,check_dim
import sys
import sympy
from sympy.matrices import Matrix

"""
$ python detBot.py <token>

calculate the determinante of a given matrix.
"""

start_message = """Give me some Matrix and I calculate the determinante. For example:
1 2
3 4
will return -2.0. You also could use the Format '1 2,3 4' and many more :)
Another example:
1/2 2.5 3
-3  3   pi
x   3   -x
returns:  -18*x + 5*pi*x/2 - 27 - 3*pi/2
"""

def handle(msg):
	chat_id = msg["chat"]["id"]
	if not "text" in msg:
		bot.sendMessage(chat_id, "I only understand text at the moment :(")
		return

	text = msg["text"]

	print "%s: %s" % (msg["from"]["first_name"], text)

	if text == "/start":
		bot.sendMessage(chat_id, start_message)
		return

	matrix = parseMatrix(text)
	if matrix is None:
		bot.sendMessage(chat_id, "Can't parse matrix, please use a different format!")
		return

	if not check_dim(matrix):
		bot.sendMessage(chat_id, "Different row length detected, please check your input!")
		return

	if len(matrix) < 2 or len(matrix[0]) < 2:
		bot.sendMessage(chat_id, "Matrix have to be at least 2x2!")
		return

	if len(matrix) != len(matrix[0]):
		bot.sendMessage(chat_id, "The two dimensions of the matrix must be equal!")
		return

	# calculate determinante
	m = Matrix(matrix)
	det = m.det()
	if len(det.free_symbols) > 0:
		bot.sendMessage(chat_id, 'determinante: %s' % det)
	else:
		bot.sendMessage(chat_id, 'determinante: %s = %s' % (det, det.evalf(4)))


TOKEN = sys.argv[1]

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()

print "Listening..."
while True:
	time.sleep(10)
