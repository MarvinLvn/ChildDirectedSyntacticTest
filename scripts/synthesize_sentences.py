import argparse
import sys
from pathlib import Path
from tasks.synthetizer import BaseCorporaSynthesisTask


def synthetize(input, output, credentials_path, test_mode=False):
    synthetizer = BaseCorporaSynthesisTask(no_confirmation=False)
    synthetizer.run(input, output, credentials_path, test_mode)


def main(argv):
    parser = argparse.ArgumentParser(description='This script generates minimal pairs of '
                                                 '(grammatical/ungrammatical) sentences.')
    parser.add_argument('--input', type=str, default='data/tasks',
                        help='Path where to find the words that need to be used')
    parser.add_argument('--out', type=str, default='data/synth',
                        help='Path where to store the generated pairs.')
    parser.add_argument('--which', type=str, choices=['adj_noun_order', 'noun_verb_order', 'ana_gender', 'ana_number',
                                                      'det_noun', 'noun_verb', 'all'], default='all',
                        help='which tasks must be generated (default to all).')
    parser.add_argument('--test', action='store_true',
                        help='if True, will generate only a few stimuli')
    parser.add_argument('--credentials_path', type=str, required=True,
                        help='Path to your Google TTS credentials')
    args = parser.parse_args(argv)
    args.input = Path(args.input)
    args.out = Path(args.out)
    if args.test:
        args.out = args.out / 'test'
    else:
        args.out = args.out / 'audio'
    args.out.mkdir(parents=True, exist_ok=True)

    if args.which == 'adj_noun_order' or args.which == 'all':
        print("Adjective noun order task:", end=' ')
        input = args.input / 'adj_noun_order.csv'
        output = args.out / input.stem
        synthetize(input, output, args.credentials_path, args.test)

    if args.which == 'noun_verb_order' or args.which == 'all':
        print("Noun verb order task:", end=' ')
        input = args.input / 'noun_verb_order.csv'
        output = args.out / input.stem
        synthetize(input, output, args.credentials_path, args.test)

    if args.which == 'ana_gender' or args.which == 'all':
        print("Anaphor gender agreement task:", end=' ')
        input = args.input / 'anaphor_gender_agreement.csv'
        output = args.out / input.stem
        synthetize(input, output, args.credentials_path, args.test)

    if args.which == 'ana_number' or args.which == 'all':
        print("Anaphor number agreement task:", end=' ')
        input = args.input / 'anaphor_number_agreement.csv'
        output = args.out / input.stem
        synthetize(input, output, args.credentials_path, args.test)

    if args.which == 'det_noun' or args.which == 'all':
        print("Determiner noun agreement task:", end=' ')
        input = args.input / 'determiner_noun_agreement.csv'
        output = args.out / input.stem
        synthetize(input, output, args.credentials_path, args.test)

    if args.which == 'noun_verb' or args.which == 'all':
        print("Noun verb agreement task:", end=' ')
        input = args.input / 'noun_verb_agreement.csv'
        output = args.out / input.stem
        synthetize(input, output, args.credentials_path, args.testwhich)


if __name__ == "__main__":
    # execute only if run as a script
    args = sys.argv[1:]
    main(args)