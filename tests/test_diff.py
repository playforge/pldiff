from libpldiff import diff
import unittest

class TestDiff(unittest.TestCase):
    def testDictTopLevelKeys(self):
        dict_keys = ['hotdogs', 'pickles', 'relish']
        dict_values = [1, None, 'goose']
        structure = dict(zip(dict_keys, dict_values))
        self.assertEquals(
            set(dict_keys),
            set(diff.find_top_level_keys(structure))
        )
        self.assertEquals([], diff.find_top_level_keys({}))

    def testListTopLevelKeys(self):
        structure = ['cabbage', 24, False]
        self.assertEquals(
            set([0, 1, 2]),
            set(diff.find_top_level_keys(structure))
        )
        self.assertEquals([], diff.find_top_level_keys([]))

    def testValueTopLevelKeys(self):
        self.assertEquals(None, diff.find_top_level_keys(10))
        self.assertEquals(None, diff.find_top_level_keys('frond'))
        self.assertEquals(None, diff.find_top_level_keys(False))
        self.assertEquals(None, diff.find_top_level_keys(None))

    def testDiffNoChange(self):
        no_change_result = {'+':{}, '*':{}, '-':[]}
        self.assertEquals(
            no_change_result,
            diff.diff_structures({}, {})
        )

        self.assertEquals(
            no_change_result,
            diff.diff_structures([], [])
        )

        # not sure how to handle these, but they don't seem problematic
        self.assertEquals(
            no_change_result,
            diff.diff_structures({}, [])
        )

        self.assertEquals(
            no_change_result,
            diff.diff_structures([], {})
        )

    def testDiffEmpty(self):
        full_structure = {
            'mario': 1,
            'luigi': 2
        }
        self.assertEquals(
            {'+':{}, '*':{}, '-':full_structure.keys()},
            diff.diff_structures(full_structure, {})
        )
        self.assertEquals(
            {'+':full_structure, '*':{}, '-':[]},
            diff.diff_structures({}, full_structure)
        )

        full_list = ['zoo', False, None]
        self.assertEquals(
            {'+':{}, '*':{}, '-':['0', '1', '2']},
            diff.diff_structures(full_list, [])
        )
        self.assertEquals(
            {
                '+':dict(zip(
                    map(str, range(len(full_list))),
                    full_list
                )),
                '*':{},
                '-':[]
            },
            diff.diff_structures([], full_list)
        )

    def testModifications(self):
        old_structure = {'a': 'b'}
        new_structure = {'a': 'z'}
        self.assertEquals(
            {'+':{}, '*':{'a':'z'}, '-':[]},
            diff.diff_structures(old_structure, new_structure)
        )

    def testOverwrite(self):
        old_structure = {'a': {'b': {}}}
        new_structure = {'a': {'c': {}}}
        self.assertEquals(
            {'+':{}, '*': new_structure, '-': []},
            diff.diff_structures(old_structure, new_structure)
        )

    def testPatchEmpty(self):
        a = {'hello': 'there'}
        self.assertEquals(a, diff.patch(a, {}))
        self.assertEquals(a, diff.patch(a, {'+':{}, '*':{}, '-':[]}))

    def testPatch(self):
        a = {'hello': 'there', 'done': None}
        b = {'hello': 'hola', 'tank': False, 'gas': 8}
        patch = diff.diff_structures(a, b)
        self.assertEquals(b, diff.patch(a, patch))

        a = ['hello']
        b = ['hola', False, None]
        patch = diff.diff_structures(a, b)
        self.assertEquals(b, diff.patch(a, patch))

    def testPatchNested(self):
        a = {'a': {'b': {'c': 7}}}
        b = {'a': {'b': {'d': 7}}}
        patch = diff.diff_structures(a, b)
        self.assertEquals(b, diff.patch(a, patch))
