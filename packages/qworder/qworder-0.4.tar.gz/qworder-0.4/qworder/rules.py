import csv
import os

from qworder import config


class Rules(dict):

    def __init__(self, rules_path: str = ""):
        self._rules_path = rules_path if rules_path else config.PATH
        super().__init__(self._load_existing_rules())

    def rules(self):
        return self.rules

    def _load_existing_rules(self):
        rules = {}
        if os.path.isfile(self._rules_path):
            with open(self._rules_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    rules[row[0]] = row[1]
        return rules

    def write_rules(self):
        output_file = open(self._rules_path, "w")
        for rule in self:
            output_file.write(rule + "," + self[rule] + "\n")
        output_file.close()


class Word(list):

    def __init__(self, word: str, sign: bool):
        super().__init__([word, sign])

    def __eq__(self, other):
        return self.word == other.word and self.sign == other.sign

    def replace(self, old: str, new: list):
        self[0] = self[0].replace(old, new[0])
        self[1] = self[1] == new[1]

    @property
    def word(self):
        return self[0]

    @property
    def sign(self):
        return self[1]
