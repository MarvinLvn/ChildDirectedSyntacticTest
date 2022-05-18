from abc import ABCMeta, abstractmethod
import pandas as pd
import numpy as np
#import mlconjug3

class BaseTask(metaclass=ABCMeta):
    def __init__(self, word_path, out_path):
        self.word_path = word_path
        self.out_path = out_path
        self.init_words()
        self._adjs = list(pd.read_csv(self.adjs_path)['word'])
        self._nouns = list(pd.read_csv(self.nouns_path)['word'])
        self._verbs = list(pd.read_csv(self.verbs_path)['word'])

        assert len(self._adjs) >= self.n_adjs
        assert len(self._nouns) >= self.n_nouns
        assert len(self._verbs) >= self.n_verbs

        self._adjs = self._adjs[:self.n_adjs]
        self._nouns = self._nouns[:self.n_nouns]
        self._verbs = self._verbs[:self.n_verbs]

        self._verbs = [self.conjugate_verb(v) for v in self._verbs]
        self.pairs = []


    def init_words(self):
        self.adjs_path = self.word_path / 'adjs.csv'
        self.nouns_path = self.word_path / 'nouns.csv'
        self.verbs_path = self.word_path / 'verbs.csv'
        self.n_adjs = 10
        self.n_nouns = 10
        self.n_verbs = 10

    @property
    def nouns(self):
        return self._nouns

    @property
    def verbs(self):
        return self._verbs

    @property
    def adjs(self):
        return self._adjs

    def get_list(self, word_type):
        if word_type == 'N':
            return self.nouns
        elif word_type == 'V':
            return self.verbs
        elif word_type == 'A':
            return self.adjs
        else:
            raise ValueError("Argument word_type should belong to ['N','V','A'].")


    @abstractmethod
    def generate_block(self):
        pass

    @abstractmethod
    def generate_all(self):
        pass

    def conjugate_verb(self, verb):
        if verb == 'have':
            return 'has'
        if verb == 'do':
            return 'does'
        if verb == 'go':
            return 'goes'
        if verb == 'be':
            return 'is'

        if verb[-2:] in ['ch', 'sh'] or verb[-1] in ['s', 'z', 'x']:
            verb += 'es'
        elif verb[-1] == 'y' and verb[-2] not in ['a', 'e', 'i', 'o', 'u', 'y']:
            verb = verb[:-1]
            verb += 'ies'
        else:
            verb += 's'
        return verb

    def write(self):
        if len(self.pairs) == 0:
            raise ValueError("Pairs should be generated before attempting to write.")

        self.out_path.parent.mkdir(parents=True, exist_ok=True)
        with self.out_path.open("w") as fin:
            print("Len is", len(self.pairs))
            for elem in self.pairs:
                grammatical, ungrammatical = elem[0], elem[1]
                fin.write("%s\t%s\n" % (grammatical, ungrammatical))
