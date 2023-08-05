import os
import random

class Phraser():
    def __init__(self) -> None:
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.path = os.path.join(self.path, './data/phrases.txt')
        self.path = os.path.normpath(self.path)
        self.text = ''
        self.charge_data()


    def charge_data(self, path=None):
        if not path:
            path = self.path
        with open(path, 'rt', encoding='utf-8') as file:
            self.text = file.readlines()
        return self.text

    def get_all_phrases(self):
        lines = [line.strip() for line in self.text]
        lines = filter(lambda x: (len(x)>0), lines)
        return list(lines)

    def get_random_phrase(self):
        if not self.text:
            self.charge_data()
        phrases = self.get_all_phrases()
        return phrases[random.randint(0, len(phrases))]

