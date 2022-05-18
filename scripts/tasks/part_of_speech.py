from .base import BaseTask


class POSOrderTask(BaseTask):

    def init_words(self):
        self.adjs_path = self.word_path / 'adjs.csv'
        self.nouns_path = self.word_path / 'nouns_animate.csv'
        self.verbs_path = self.word_path / 'verbs_intransitive.csv'
        self.n_adjs = 40
        self.n_nouns = 40
        self.n_verbs = 40

    def generate_block(self, word1, word2):
        # The <word1> <word2> is legal. The <word2> <word1> is illegal.
        gr, un = 'The %s %s.' % (word1, word2), 'The %s %s.' % (word2, word1)
        self.pairs.append((gr, un))

    def generate_all(self):
        for adj in self.adjs:
            for noun1 in self.nouns:
                self.generate_block(adj, noun1)

        for verb in self.verbs:
            for noun1 in self.nouns:
                self.generate_block(noun1, verb)
