"""Implementation of evaluation function for ngram language models"""

from typing import Dict
from math import exp
from pathlib import Path
from paraphone.ngrams_tools import NGramLanguageModel

def evaluate(text_file: str,
                ngram_language_model: NGramLanguageModel) -> Dict[str, float]:
    """
    This function evaluate a ngram language model on a\
    given raw text file. This texte file muste already be\
    preprocessed and tokenized, with one sentence/utterance\
    per line. The evaluation of the ngram language model\
    consists in returning the log-probability and the\
    perplexity of the corpus.

    Parameters
    ----------
    - text_file: str
        The path to the text on which the language model\
        will be evaluated.
    - ngram_language_model: NGramLanguageModel
        An instance of a trained ngram language model.
    
    Return
    ------
    - dict:
        Dictionary associating 
    """
    with open(text_file) as input_file:
        results = {}
        total_ngrams = 0.0
        total_logprobs = 0.0
        for sentence in input_file:
            sentence = sentence.strip()
            ngrams = list(ngram_language_model.get_ngrams(sentence.split(" ")))
            total_ngrams += len(ngrams)
            total_logprobs += ngram_language_model.to_ngram_logprob(ngrams)
        corpus_log_prob = total_logprobs / total_ngrams
        results["log_prob"] = corpus_log_prob
        results["perplexity"] = exp(-corpus_log_prob)
    return results

if __name__ == "__main__" :
    from argparse import ArgumentParser
    import csv

    parser = ArgumentParser()
    parser.add_argument("--train_file",
                        type=str,
                        help="The directory containing the train file.",
                        required=True)
    parser.add_argument("--dev_file",
                    type=str,
                    help="The folder containing the development corpus.",
                    required=True)
    parser.add_argument("--ngram_model",
                        type=str,
                        help="The trained ngram language model.",
                        required=True)
    parser.add_argument("--out_filename",
                        type=str,
                        help="The filename of the output results.",
                        required=True)
    args = parser.parse_args()

    ngram_lm = NGramLanguageModel()
    ngram_lm.load_model(args.ngram_model)

    train_evaluation = evaluate(args.train_file, ngram_lm)
    train_evaluation['corpus'] = 'train'
    dev_evaluation = evaluate(args.dev_file, ngram_lm)
    dev_evaluation['corpus'] = 'dev'
    out_directory = Path("results/model_evaluations")
    out_directory.mkdir(exist_ok=True, parents=True)
    with open(out_directory / Path(f"{args.out_filename}.csv"),
                'w', newline='') as csvfile:
        fieldnames = ['corpus', 'log_prob', 'perplexity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(train_evaluation)
        writer.writerow(dev_evaluation)
