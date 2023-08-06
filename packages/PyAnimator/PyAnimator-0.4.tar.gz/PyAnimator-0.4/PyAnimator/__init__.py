import os, sys, time
from colorama import Fore, init, AnsiToWin32
import threading
import itertools

stopt = True

def animation2(message, tempo, cycle, xx, xy, inf=None, dots=None):
	sys.stderr.flush()
	os.system("cls")
	sys.stderr.flush()
	init(autoreset=True)
	init(wrap=False)
	stream = AnsiToWin32(sys.stderr).stream
	colors = dict(Fore.__dict__.items())
	dot = '.'
	sys.stderr.flush()

	if dots:
		if inf:
			count = 0
			for color, i in zip(colors.keys(), range(tempo)):
				if stopt == False:

					return
				else:
					sys.stderr.write("\x1b7\x1b\x1b[F\x1b[F[%d;%df%s\x1b8" % (xx, xy, colors[color] + message + dot))
					sys.stderr.flush()
					time.sleep(cycle)
					dot = dot + '.'

					if count == 1:
						dot = dot[:-tempo]
						count = count - 1

				sys.stderr.flush()
				count = count + 1

		else:
			if stopt == False:

				return
			else:
				for color, i in zip(colors.keys(), range(tempo)):
					sys.stderr.write("\x1b7\x1b\x1b[F\x1b[F[%d;%df%s\x1b8" % (xx, xy, colors[color] + message + dot))
					sys.stderr.flush()
					time.sleep(cycle)
					dot = dot + '.'
				sys.stderr.flush()
	else:
		if inf:
			while stopt:
				if stopt == False:
					break
				else:
					for color, i in zip(colors.keys(), range(tempo)):
						if stopt == False:

							return
						sys.stderr.write("\x1b7\x1b\x1b[F\x1b[F[%d;%df%s\x1b8" % (xx, xy, colors[color] + message))
						sys.stderr.flush()
						time.sleep(cycle)
					sys.stderr.flush()
		else:
			if stopt == False:

				return
			else:
				sys.stderr.flush()
				for color, i in zip(colors.keys(), range(tempo)):
					sys.stderr.write("\x1b7\x1b\x1b[F\x1b[F[%d;%df%s\x1b8" % (xx, xy, colors[color] + message))
					sys.stderr.flush()
					time.sleep(cycle)
				sys.stderr.flush()


def animation(message, tempo, cycle, xx, xy, inf=None, dots=None):
	sys.stderr.flush()
	taskjrhkajshurhuuuuwuuauslkjrljksaf = threading.Thread(target=animation2, args=(message, tempo, cycle, xx, xy), kwargs={'inf': inf, 'dots': dots})
	taskjrhkajshurhuuuuwuuauslkjrljksaf.daemon = True
	taskjrhkajshurhuuuuwuuauslkjrljksaf.start()
	os.system("cls")
	sys.stderr.flush()
	time.sleep(0.10)
	os.system("cls")

def stop():
	sys.stderr.flush()
	sys.stderr.flush()
	global stopt
	stopt = False
