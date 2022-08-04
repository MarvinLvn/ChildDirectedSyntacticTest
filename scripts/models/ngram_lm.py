"""This module implements a trainer of ngram language models.
"""
from paraphone.ngrams_tools import NGramLanguageModel

if __name__ == "__main__" :
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--train_file",
                        type=str,
                        help="The directory containing the train file.",
                        required=True)
    parser.add_argument("--ngram_size",
                        type=int,
                        default=3,
                        help="The size of the left context\
                            for the n-gram language model",
                        required=False)
    parser.add_argument("--smooth",
                        type=float,
                        default=1e-3,
                        help="The value for smoothing the probability\
                            distribution of the language model",
                        required=False)
    parser.add_argument("--out_directory",
                        type=str,
                        help="The directory where the model will be stored",
                        required=True)
    parser.add_argument("--out_filename",
                        help="The filename for the model.",
                        required=True)
    args = parser.parse_args()
    ngram_lm = NGramLanguageModel(ngram_size=args.ngram_size, smooth=args.smooth)
    print("Training the model...")
    ngram_lm.estimate(args.train_file)
    print("Saving the model...")
    ngram_lm.save_model(args.out_directory, args.out_filename)
