from .base import BaseTask
import pandas as pd

class NounVerbAgreementTask(BaseTask):

    def __init__(self, word_path, out_path):
        self.word_path = word_path
        self.out_path = out_path
        self.init_words()
        self._nouns = list(pd.read_csv(self.nouns_path)['word'])[:self.n_nouns]
        self._nouns_plural = list(pd.read_csv(self.nouns_path)['plural'])[:self.n_nouns]
        self._verbs = list(pd.read_csv(self.verbs_path)['word'])[:self.n_verbs]
        self._verbs_first_person = self._verbs
        self._verbs = [self.conjugate_verb(v) for v in self._verbs]
        self.pairs = []

    def init_words(self):
        self.nouns_path = self.word_path / 'nouns_gendered.csv'
        self.verbs_path = self.word_path / 'verbs_noun_verb_agreement.csv'
        self.n_verbs = 10
        self.n_nouns = 10

    def generate_block(self, noun1, plural_noun1, noun2, verb, verb_first_person):

        gr1, un1 = 'The %s %s the %s.' % (noun1, verb, noun2), 'The %s %s the %s.' % (noun1, verb_first_person, noun2)
        gr2, un2 = 'The %s %s the %s.' % (plural_noun1, verb_first_person, noun2), 'The %s %s the %s.' % (plural_noun1, verb, noun2)
        gr3, un3 = 'The %s %s the %s.' % (noun1, verb, noun2), 'The %s %s the %s.' % (plural_noun1, verb, noun2)
        gr4, un4 = 'The %s %s the %s.' % (plural_noun1, verb_first_person, noun2), 'The %s %s the %s.' % (noun1, verb_first_person, noun2)

        self.pairs.append((gr1, un1))
        self.pairs.append((gr2, un2))
        self.pairs.append((gr3, un3))
        self.pairs.append((gr4, un4))

    def generate_all(self):
        for i, verb in enumerate(self.verbs):
            verb_first_person = self._verbs_first_person[i]
            for j, noun1 in enumerate(self.nouns):
                plural_noun1 = self._nouns_plural[j]
                for noun2 in self.nouns:
                    if noun1 != noun2:
                        self.generate_block(noun1, plural_noun1, noun2, verb, verb_first_person)