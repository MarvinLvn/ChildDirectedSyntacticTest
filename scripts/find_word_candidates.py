import argparse
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import itertools

def main(argv):
    parser = argparse.ArgumentParser(description='This script find words that will be used in the syntactic'
                                                 'tasks (Verbs are returned in infinitive form)')
    parser.add_argument('--out', type=str, default='data/word_candidates',
                        help='Path where to store the transcripts.')
    parser.add_argument('--input', type=str, default='data/transcripts/sentences.csv',
                        help='Path where to store the transcripts.')
    parser.add_argument('--n_to_keep', type=int, default=100,
                        help='Number of words to keep in each category')
    args = parser.parse_args(argv)
    args.out = Path(args.out)
    args.out.mkdir(parents=True, exist_ok=True)

    # Load sentences
    data = pd.read_csv(args.input)

    # Filter Media/Environment
    data = data[~data.speaker_role.isin([['Media', 'Environment']])]

    # Filter rows for which POS tags or stem is NA
    data = data[['stem', 'part_of_speech']]
    len1 = len(data)
    data = data.dropna(axis=0, how='any')
    len2 = len(data)
    print("Lost %.1f %% data when excluding items for which the number of POS or stem is NA." % (100 - len2 * 100 / len1))
    stem = [s.lower().split(' ') for s in data.stem]
    pos = [p.split(' ') for p in data.part_of_speech]

    # Filter rows for which number of POS tags != number of words
    len1 = len(data)
    data = [(s, p) for s, p in zip(stem, pos) if len(s) == len(p)]
    len2 = len(data)
    print("Lost %.1f %% data when excluding items for which the number of POS is different from the number of words" % (100 - len2*100/len1))

    word = list(itertools.chain.from_iterable([s for s, _ in data]))
    pos = list(itertools.chain.from_iterable([p for _, p in data]))
    data = pd.DataFrame.from_dict({'word': word, 'pos': pos})
    data = data.groupby('word')['pos'].value_counts().unstack().fillna(0)
    data['count'] = data.sum(axis=1)
    data = data.sort_values(by='count', ascending=False).reset_index()
    columns = list(data.columns)
    columns = [c for c in columns if c not in ['count', 'word']]
    for col in columns:
        data[col] = data[col] / data['count']

    data['freq'] = data['count'] / data['count'].sum()

    # Find proba that a word is a noun, an adjective, or a verb
    nouns_col = ['n', 'n:adj', 'n:gerund', 'n:let', 'n:prop', 'n:pt']
    data['noun_prob'] = data[nouns_col].sum(axis=1)
    adj_col = ['adj']
    data['adj_prob'] = data[adj_col].sum(axis=1)
    verb_col = ['v']
    data['verb_prob'] = data[verb_col].sum(axis=1)

    # Filter words whose proba is lower than 0.9 and save to csv file
    nouns = data.loc[data.noun_prob > 0.95, ['word', 'freq', 'noun_prob']]
    to_exclude = ['chi', 'ross', 'laura', 'lot', 'bit', 'top', 'ma', 'e', 'sarah',
                  'naima', 'adam', 'b', 'william', 'o', 'carl', 'momma', 'michael',
                  'alex', 'd', 'nomi', 'bro', 's', 'henry', 'lily', 'david', 'peter',
                  't', 'abe', 'c', 'paul', 'sis']
    nouns = nouns[~nouns.word.isin(to_exclude)]
    nouns[:args.n_to_keep].to_csv(args.out / 'nouns.csv', index=False)

    adjs = data.loc[data.adj_prob > 0.95, ['word', 'freq', 'adj_prob']]
    to_exclude = ['thirst', 'craze', 'eensie', 'weensie', 'loll', 'ying', 'shag']
    adjs = adjs[~adjs.word.isin(to_exclude)]
    adjs[:args.n_to_keep].to_csv(args.out / 'adjs.csv', index=False)

    verbs = data.loc[data.verb_prob > 0.95, ['word', 'freq', 'verb_prob']]
    to_exclude = ['ooh', 'best', 'zipper', 'pishie', 'sticker', 'dirty', 'scoot',
                  'sprout', 'pant', 'jingle', 'bicycle', 'clink', 'scallop', 'boog',
                  'muddy', 'headquarter']
    verbs = verbs[~verbs.word.isin(to_exclude)]
    verbs[:args.n_to_keep].to_csv(args.out / 'verbs.csv', index=False)


if __name__ == "__main__":
    # execute only if run as a script
    args = sys.argv[1:]
    main(args)