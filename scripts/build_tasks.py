import argparse
import sys
from pathlib import Path
from tasks.part_of_speech import POSOrderTask
from tasks.anaphor_agreement import AnaphorGenderAgreementTask, AnaphorNumberAgreementTask
from tasks.determiner_noun_agreement import DeterminerNounAgreementTask
from tasks.noun_verb_agreement import NounVerbAgreementTask
def main(argv):
    parser = argparse.ArgumentParser(description='This script generates minimal pairs of '
                                                 '(grammatical/ungrammatical) sentences.')
    parser.add_argument('--input', type=str, default='data/word_candidates',
                        help='Path where to find the words that need to be used')
    parser.add_argument('--out', type=str, default='data/tasks',
                        help='Path where to store the generated pairs.')
    args = parser.parse_args(argv)
    args.input = Path(args.input)
    args.out = Path(args.out)
    args.out.mkdir(parents=True, exist_ok=True)

    # pos_task = POSOrderTask(args.input, args.out / 'pos_order.csv')
    # pos_task.generate_all()
    # pos_task.write()
    #
    # ana_ag1 = AnaphorGenderAgreementTask(args.input, args.out / 'anaphor_gender_agreement.csv')
    # ana_ag1.generate_all()
    # ana_ag1.write()

    #ana_ag2 = AnaphorNumberAgreementTask(args.input, args.out / 'anaphor_number_agreement.csv')
    #ana_ag2.generate_all()
    #ana_ag2.write()

    #det_noun_ag = DeterminerNounAgreementTask(args.input, args.out / 'determiner_noun_agreement.csv')
    #det_noun_ag.generate_all()
    #det_noun_ag.write()

    noun_verb_ag = NounVerbAgreementTask(args.input, args.out / 'noun_verb_agreement.csv')
    noun_verb_ag.generate_all()
    noun_verb_ag.write()

if __name__ == "__main__":
    # execute only if run as a script
    args = sys.argv[1:]
    main(args)