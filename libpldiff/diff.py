#! /usr/bin/env python
"""
Diffs structured data
"""

def find_top_level_keys(structure):
	"""
	Finds all values that are valid indexes of the provided structure
	"""
	try:
		# try to be polymorphic friendly
		return structure.keys()
	except AttributeError:
		if isinstance(structure, list):
			return range(len(structure))
	return None

def find_keys(structure):
	tracks = [(structure, [])]
	final = {}
	while tracks:
		obj, path = tracks.pop()
		keys = find_top_level_keys(obj)
		if keys:
			for key in keys:
				tracks.append(
					([obj[key], path + [key]])
				)
		else:
			final[make_path(path)] = obj
	return final

def make_path(parts):
	return '.'.join(map(str, parts))

def diff_structures(structure_1, structure_2):
	"""
	Diffs the two structures, returning a dict containing a map of additions,
	a map of modifications, and a list of deletions
	"""
	final = {
		'+':{}, # additions
		'*':{}, # changes
		'-':[], # deletions
	}

	comparisons = [(structure_1, structure_2, [])]
	while comparisons:
		old, new, path = comparisons.pop()
		if old == new:
			continue

		new_keys = find_top_level_keys(new)
		old_keys = find_top_level_keys(old)
		if not (new_keys and old_keys):
			# either new is a bare value or old was a bare value
			final['*'][make_path(path)] = new
		else:
			new_keys = set(new_keys)
			old_keys = set(old_keys)
			for key in new_keys:
				if key not in old_keys:
					final['+'][make_path(path + [key])] = new[key]
				else:
					comparisons.append((old[key], new[key], path + [key]))
					old_keys.remove(key)

			# keys preset only in old_keys
			for key in old_keys:
				final['-'].append(make_path(path + [key]))

	return final
