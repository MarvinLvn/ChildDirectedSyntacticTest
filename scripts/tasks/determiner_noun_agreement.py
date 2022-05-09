from .base import BaseTask
import pandas as pd

class DeterminerNounAgreementTask(BaseTask):

    def __init__(self, word_path, out_path):
        self.word_path = word_path
        self.out_path = out_path
        self.init_words()
        self._nouns = list(pd.read_csv(self.nouns_path)['word'])[:self.n_nouns]
        self._nouns_plural = list(pd.read_csv(self.nouns_path)['plural'])[:self.n_nouns]
        self._adjs = list(pd.read_csv(self.adjs_path)['word'])[:self.n_adjs]
        self.pairs = []

    def init_words(self):
        self.nouns_path = self.word_path / 'nouns_gendered.csv'
        self.adjs_path = self.word_path / 'adjs.csv'
        self.n_adjs = 25
        self.n_nouns = 10

    def generate_block(self, noun, plural_noun, adj):

        gr1, un1 = 'Each %s %s.' % (adj, noun), 'Many %s %s.' % (adj, noun)
        gr2, un2 = 'Many %s %s.' % (adj, plural_noun), 'Each %s %s.' % (adj, plural_noun)
        gr3, un3 = 'Each %s %s.' % (adj, noun), 'Each %s %s.' % (adj, plural_noun)
        gr4, un4 = 'Many %s %s.' % (adj, plural_noun), 'Many %s %s.' % (adj, noun)

        self.pairs.append((gr1, un1))
        self.pairs.append((gr2, un2))
        self.pairs.append((gr3, un3))
        self.pairs.append((gr4, un4))

    def generate_all(self):
        for adj in self.adjs:
            for i, noun in enumerate(self.nouns):
                plural_noun = self._nouns_plural[i]
                self.generate_block(noun, plural_noun, adj)