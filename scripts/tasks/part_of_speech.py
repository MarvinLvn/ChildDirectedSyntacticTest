from .base import BaseTask


class POSOrderTask(BaseTask):

    def init_words(self):
        self.adjs_path = self.word_path / 'adjs.csv'
        self.nouns_path = self.word_path / 'nouns_animate.csv'
        self.verbs_path = self.word_path / 'verbs.csv'
        self.n_adjs = 10
        self.n_nouns = 10
        self.n_verbs = 10

    def generate_block(self, adj, verb, noun1):
        gr1, un1 = 'The %s %s.' % (adj, noun1), 'The %s %s.' % (noun1, adj)
        gr2, un2 = 'The %s %s.' % (noun1, verb), 'The %s %s.' % (verb, noun1)
        self.pairs.append((gr1, un1))
        self.pairs.append((gr2, un2))

    def generate_all(self):
        for adj in self.adjs:
            for verb in self.verbs:
                for noun1 in self.nouns:
                    self.generate_block(adj, verb, noun1)
