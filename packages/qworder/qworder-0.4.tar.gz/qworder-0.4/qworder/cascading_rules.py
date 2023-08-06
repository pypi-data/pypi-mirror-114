# Cascader class reduces sequences of quantum gates for given gate-set and generates
# a multiplication table of all possible reductions

import time

import numpy as np

from qworder.rules import Rules


class Cascader(object):
    base_gates = {
        'I': np.array(
            [[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
        'X': np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]]),
        'Y': np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]]),
        'Z': np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]]),
        'H': np.array([[0, 0, 1], [0, -1, 0], [1, 0, 0]]),
        'T': np.array(
            [[np.cos(np.pi / 4), -np.sin(np.pi / 4), 0], [np.sin(np.pi / 4), np.cos(np.pi / 4), 0], [0, 0, 1]]),
        'R': np.array(
            [[np.cos(np.pi / 4), np.sin(np.pi / 4), 0], [- np.sin(np.pi / 4), np.cos(np.pi / 4), 0], [0, 0, 1]])
    }

    def __init__(self, rules_path: str = ""):
        if len(rules_path):
            self.rules = Rules(rules_path)
        else:
            self.rules = Rules()

    def cascade_word(self, word: str) -> str:
        index = 0
        while index < len(word) - 1 and len(word) > 1:
            sub = word[index: index + 2]
            replacement = self._check_replace(sub)
            if replacement and replacement[0] != sub:
                word = word.replace(sub, replacement)
                index = max(0, index - 1)
            else:
                sub = word[index: index + 3]
                replacement = self._check_replace(sub)
                if replacement and replacement[0] != sub:
                    word = word.replace(sub, replacement)
                    index = max(0, index - 1)
                else:
                    index += 1
        return word

    def is_cascadable(self, word: str) -> bool:
        index = 0
        while index < len(word) - 1 and len(word) > 1:
            sub = word[index: index + 2]
            replacement = self._check_replace(sub)
            if replacement and replacement[0] != sub:
                return True
            else:
                sub = word[index: index + 3]
                replacement = self._check_replace(sub)
                if replacement and replacement[0] != sub:
                    return True
                else:
                    index += 1
        return False

    def _check_replace(self, sub):
        if sub in self.rules and sub != self.rules[sub]:
            return self.rules[sub]
        replacement = self._check_product(sub)
        if replacement:
            self.rules[sub] = replacement
            return replacement
        else:
            self.rules[sub] = sub
            return False

    def _check_product(self, prod: str) -> str:
        g = [self.base_gates[p] for p in prod]
        for letter in self.base_gates:
            temp = g[0]
            for i in range(1, len(g)):
                temp = np.matmul(temp, g[i])
            bg = self.base_gates[letter]
            if np.allclose(temp, bg):
                return letter
        return ""


if __name__ == '__main__':
    start_time = time.time()
    w = "HXYYXZXH"
    c = Cascader()
    print(w)
    print(c.cascade_word(w))
    print(c.is_cascadable(w))
    c.rules.write_rules()
    print("--- %s seconds ---" % (time.time() - start_time))
