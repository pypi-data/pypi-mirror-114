# Generate all possible words of given length
from typing import Dict, List
from qworder.rules import Word
from qworder.cascading_rules import Cascader


class WordGenerator:

    def __init__(self, input_set: list, length: int, cascader: Cascader = None):
        self.output = []
        self.input_set = input_set
        self.length = length
        if cascader:
            self.cascader = cascader

    def generate_words(self) -> list:
        print("Generating words for length " + str(self.length))
        self.__generate_words_rec("", self.length)
        return self.output

    def __generate_words_rec(self, word: str, length: int) -> None:
        if length == 0:
            if self.cascader:
                self.output.append(self.cascader.cascade_word(Word(word, True)).word)
            else:
                self.output.append(word)
            return
        for i in range(len(self.input_set)):
            self.__generate_words_rec(word + self.input_set[i], length - 1)

    def generate_words_shorter_than(self) -> List[str]:
        for i in range(self.length):
            self.__generate_words_rec("", i + 1)
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
    w = WordGenerator(['a', 'b', 'c'], 4, cascader=Cascader())
    print(w.generate_words())
