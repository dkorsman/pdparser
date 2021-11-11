hidden_cats = set()

def hide_cat(cat:str) -> None:
	hidden_cats.add(cat)

def catprint(cat:str, text:str) -> None:
	global hidden_cats

	if cat not in hidden_cats:
		print('[{:>12}] {}'.format(cat, text))