verbosity = 0

def set_verbosity(level:int) -> None:
	global verbosity

	verbosity = level

# Verbose print
def vprint(level:int, text:str) -> None:
	global verbosity

	if verbosity >= level:
		print('[{}] {}'.format(level, text))
