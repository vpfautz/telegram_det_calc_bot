import telepot
from telepot.loop import MessageLoop
import time
import numpy as np
from matrix_parser import parseMatrix,check_dim
import sys

"""
$ python detBot.py <token>

calculate the determinante of a given matrix.
"""

def handle(msg):
	chat_id = msg["chat"]["id"]
	text = msg["text"]

	if text == "/start":
		bot.sendMessage(chat_id, "Give me some Matrix and I calculate the determinante. For example:\n1 2\n3 4\nwill return -2.0. You also could use the Format '1 2,3 4' and many more :)")
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

	print matrix

	# calculate determinante
	a = np.array(matrix)
	det = round(np.linalg.det(a), 4)

	bot.sendMessage(chat_id, 'determinante: %s' % det)


TOKEN = sys.argv[1]

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()

print "Listening..."
while True:
	time.sleep(10)
