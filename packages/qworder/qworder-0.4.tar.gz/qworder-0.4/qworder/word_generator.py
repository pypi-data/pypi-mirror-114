# Generate all possible words of given length
import sys
import time
from typing import Dict, List

from tqdm import tqdm

from qworder.cascading_rules import Cascader


class WordGenerator:

    def __init__(self, input_set: list, length: int, cascader: Cascader = None):
        self.output = []
        self.input_set = input_set
        self.length = length
        self.cascader = cascader if cascader else None
        self.pbar = tqdm()

    def generate_words(self) -> list:
        if self.cascader:
            self._generate_words_rec_c("", self.length)
        else:
            self._generate_words_rec("", self.length)

        return self.output

    def _generate_words_rec_c(self, word: str, length: int) -> None:
        self.pbar.update(1)
        if length == 0:
            if not self.cascader.is_cascadable(word):
                self.output.append(word)
            return
        for i in range(len(self.input_set)):
            self._generate_words_rec_c(word + self.input_set[i], length - 1)

    def _generate_words_rec(self, word: str, length: int) -> None:
        self.pbar.update(1)
        if length == 0:
            self.output.append(word)
            return
        for i in range(len(self.input_set)):
            self._generate_words_rec(word + self.input_set[i], length - 1)

    def generate_words_shorter_than(self) -> List[str]:
        for i in range(self.length):
            self._generate_words_rec("", i + 1)
            self._remove_unnecessary(i + 1)
        return self.output

    def _remove_unnecessary(self, length: int = 0) -> None:
        if length == 1:
            return
        if length == 0:
            length = self.length
        for letter in self.input_set:
            self.output.remove(letter * length)

    def get_words_dictionary(self) -> Dict[int, list]:
        words = {}
        length = self.length
        for k in range(1, length + 1):
            self.length = k
            words[k] = self.generate_words()
            self.output = []
        return words


if __name__ == '__main__':
    start_time = time.time()
    c = Cascader()
    w = WordGenerator(['H', 'T', 'R', 'I', 'X', 'Y', 'Z'], 7, cascader=c)
    words = w.generate_words()
    print(len(words))
    c.rules.write_rules()
    print("--- %s seconds ---" % (time.time() - start_time))
    print("with truncating:\t" + str(sys.getsizeof(words)/1000.0))

    w = WordGenerator(['H', 'T', 'R', 'I', 'X', 'Y', 'Z'], 7)
    words = w.generate_words()
    print("without truncating:\t" + str(sys.getsizeof(words)/1000.0))
