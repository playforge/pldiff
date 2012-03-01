#! /usr/bin/env python
"""
Diffs structured data
"""

import copy

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
        if new_keys is None or old_keys is None:
            # either new is a bare value or old was a bare value
            final['*'][make_path(path)] = new
        else:
            new_keys = set(new_keys)
            old_keys = set(old_keys)

            # path is used because we cannot represent a type change at the root
            # level of the structure
            if new_keys.isdisjoint(old_keys) and path:
                final['*'][make_path(path)] = new
            else:
                for key in new_keys:
                    if key not in old_keys:
                        final['+'][make_path(path + [key])] = new[key]
                    else:
                        comparisons.append((old[key], new[key], path + [key]))
                        old_keys.remove(key)

                # keys present only in old_keys
                for key in old_keys:
                    final['-'].append(make_path(path + [key]))

    return final

def patch(structure, diff):
    """
    Applies the changes represented in `diff` to `structure`. This function makes
    no assumptions about the presence of +, *, - keys in `diff`.

    `structure` is not modified by calling this function. A modified copy of
    structure is returned.
    """
    # additions and modifications can be collapsed into one changeset
    obj = copy.deepcopy(structure)
    additions = diff.get('*', {}).items() + diff.get('+', {}).items()
    for key, value in additions:
        key_parts = key.split('.')
        init, tail = key_parts[:-1], key_parts[-1]
        struct = obj
        for part in init:
            struct = struct[part]

        try:
            tail = int(tail, 10)
            # I will assume that this structure is list-like
            if tail < 0:
                raise Exception('List index must be >= 0')

            while len(struct) < tail+1:
                # I can't think of a better way, unfortunately
                struct.append(None)
        except ValueError:
            pass

        struct[tail] = value

    for key in diff.get('-', []):
        key_parts = key.split('.')
        init, tail = key_parts[:-1], key_parts[-1]
        struct = obj
        for part in init:
            struct = struct[part]

        try:
            tail = int(tail, 10)
            if tail < 0:
                raise Exception('List index must be >= 0')

            while len(struct) >= tail+1:
                del struct[tail]
        except ValueError:
            del struct[tail]

    return obj
