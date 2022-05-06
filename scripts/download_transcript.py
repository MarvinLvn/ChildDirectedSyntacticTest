import argparse
import sys
from pathlib import Path

import childespy


def main(argv):
    parser = argparse.ArgumentParser(description='This script download American English '
                                                 'transcripts from the CHILDES database.')
    parser.add_argument('--out', type=str, default='data/transcripts',
                        help='Path where to store the transcripts.')
    args = parser.parse_args(argv)
    args.out = Path(args.out)
    args.out.mkdir(parents=True, exist_ok=True)

    print("Start downloading transcripts...")
    transcripts = childespy.get_transcripts(collection="Eng-NA")
    transcripts.to_csv(args.out / "transcripts.csv", index=False)
    print("Done.")

    print("Start downloading tokens...")
    tokens = childespy.get_tokens(collection="Eng-NA", corpus="Brown", token='%')
    tokens.to_csv(args.out / "tokens.csv", index=False)
    print(tokens)
    print("Done.")

    print("Start downloading types...")
    types = childespy.get_types(collection="Eng-NA")
    types.to_csv(args.out / "types.csv", index=False)
    print(types)
    print("Done.")

    print("Start downloading sentences...")
    sentences = childespy.get_utterances(collection="Eng-NA")
    sentences.to_csv(args.out / "sentences.csv", index=False)
    print("Done.")


if __name__ == "__main__":
    # execute only if run as a script
    args = sys.argv[1:]
    main(args)