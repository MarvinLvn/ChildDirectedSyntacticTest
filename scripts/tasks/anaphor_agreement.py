from .base import BaseTask
import pandas as pd
import mlconjug3

class AnaphorGenderAgreementTask(BaseTask):

    def __init__(self, word_path, out_path):
        self.word_path = word_path
        self.out_path = out_path
        self.init_words()
        self._nouns = list(pd.read_csv(self.nouns_path)['word'])[:self.n_nouns]
        self._gender = list(pd.read_csv(self.nouns_path)['gender'])[:self.n_nouns]
        self._equiv_idx = list(pd.read_csv(self.nouns_path)['equiv'])[:self.n_nouns]
        self._verbs = list(pd.read_csv(self.verbs_path)['word'])[:self.n_verbs]
        self._verbs = [self.conjugate_verb(v) for v in self._verbs]
        self.pairs = []

    def init_words(self):
        self.nouns_path = self.word_path / 'nouns_gendered.csv'
        self.verbs_path = self.word_path / 'verbs_reflexive.csv'
        self.n_verbs = 50
        self.n_nouns = 10

    def generate_block(self, noun, equiv_noun, verb, gender):
        if gender == 'M':
            pronoun = 'himself'
            opposite = 'herself'
        elif gender == 'F':
            pronoun = 'herself'
            opposite = 'himself'
        else:
            raise ValueError("Gender should belong to [M,F]")

        gr1, un1 = 'The %s %s %s.' % (noun, verb, pronoun), 'The %s %s %s.' % (noun, verb, opposite)
        gr2, un2 = 'The %s %s %s.' % (noun, verb, pronoun), 'The %s %s %s.' % (equiv_noun, verb, pronoun)
        self.pairs.append((gr1, un1))
        self.pairs.append((gr2, un2))

    def generate_all(self):
        for verb in self.verbs:
            for i, noun in enumerate(self.nouns):
                gender = self._gender[i]
                equiv_id = self._equiv_idx[i]
                equiv_noun = self._nouns[equiv_id]
                self.generate_block(noun, equiv_noun, verb, gender)


class AnaphorNumberAgreementTask(BaseTask):

    def __init__(self, word_path, out_path):
        self.word_path = word_path
        self.out_path = out_path
        self.init_words()
        self.conjugator = mlconjug3.Conjugator(language='en')
        self._nouns = list(pd.read_csv(self.nouns_path)['word'])[:self.n_nouns]
        self._nouns_plural = list(pd.read_csv(self.nouns_path)['plural'])[:self.n_nouns]
        self._gender = list(pd.read_csv(self.nouns_path)['gender'])[:self.n_nouns]
        self._equiv_idx = list(pd.read_csv(self.nouns_path)['equiv'])[:self.n_nouns]
        self._verbs = list(pd.read_csv(self.verbs_path)['word'])[:self.n_verbs]
        self._verbs = [self.conjugate_verb(v) for v in self._verbs]
        self.pairs = []

    def init_words(self):
        self.nouns_path = self.word_path / 'nouns_gendered.csv'
        self.verbs_path = self.word_path / 'verbs_reflexive.csv'
        self.n_verbs = 50
        self.n_nouns = 10

    def generate_block(self, noun, plural_noun, verb, gender):
        opposite = 'themselves'
        if gender == 'M':
            pronoun = 'himself'
        elif gender == 'F':
            pronoun = 'herself'
        else:
            raise ValueError("Gender should belong to [M,F]")

        gr1, un1 = 'The %s %s %s.' % (noun, verb, pronoun), 'The %s %s %s.' % (noun, verb, opposite)
        gr2, un2 = 'The %s %s %s.' % (plural_noun, verb, opposite), 'The %s %s %s.' % (plural_noun, verb, pronoun)
        gr3, un3 = 'The %s %s %s.' % (noun, verb, pronoun), 'The %s %s %s.' % (plural_noun, verb, pronoun)
        gr4, un4 = 'The %s %s %s.' % (plural_noun, verb, opposite), 'The %s %s %s.' % (noun, verb, opposite)

        self.pairs.append((gr1, un1))
        self.pairs.append((gr2, un2))
        self.pairs.append((gr3, un3))
        self.pairs.append((gr4, un4))

    def generate_all(self):
        for verb in self.verbs:
            for i, noun in enumerate(self.nouns):
                gender = self._gender[i]
                plural_noun = self._nouns_plural[i]
                self.generate_block(noun, plural_noun, verb, gender)

    def conjugate_verb(self, verb):
        # In this task the verbs are conjugated to the past tense to avoid mismatch between singular and plural
        # Here are the verbs for which the automatic conjugator fails
        if verb == 'acclimate':
            out = 'acclimated'
        elif verb == 'fulfill':
            out = 'fulfilled'
        elif verb == 'transcend':
            out = 'transcended'
        elif verb == 'wash':
            out = 'washed'
        elif verb == 'content':
            out = 'contented'
        elif verb == 'convince':
            out = 'convinced'
        elif verb == 'hurt':
            out = 'hurt'
        elif verb == 'eat':
            out = 'ate'
        elif verb == 'hang':
            out = 'hung'
        else:
            out = self.conjugator.conjugate(verb).conjug_info['indicative']['indicative past tense']['3s']
        return out