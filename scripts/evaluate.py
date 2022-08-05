"""Implementation of an evaluation function for ngram language models."""

from typing import Dict
from math import exp
from argparse import ArgumentParser
from pathlib import Path
from models.ngram_lm import NGramLanguageModel
import pandas as pd

def evaluate(text_file: str,
             ngram_language_model: NGramLanguageModel) -> Dict[str, float]:
    """
    This function evaluates a ngram language model on a\
    given raw text file. This text file must already be\
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
        evaluation_results = {}
        total_utterances = 0.0
        total_logprobs = 0.0
        for utterance in input_file:
            utterance = utterance.strip()
            utterance_logprob = ngram_language_model.assign_logprob(utterance)
            if not utterance_logprob :
                continue
                # This condition can only holds when pad_utterance is set to\
                # False in the ngram language model.
                # We ignore utterances smaller than the ngram size of
                # the language model.
            total_logprobs += utterance_logprob
            total_utterances += 1
        corpus_log_prob = total_logprobs / total_utterances
        evaluation_results["log_prob"] = corpus_log_prob
        evaluation_results["perplexity"] = exp(-corpus_log_prob)
    return evaluation_results

def main(args) -> None:
    """
    This function calls the evaluation function\
    and stores the results in a csv file.
    """

    ngram_lm = NGramLanguageModel()
    ngram_lm.load_model(args.ngram_model)

    train_evaluation = evaluate(args.train_file, ngram_lm)
    train_evaluation['corpus'] = 'train'
    dev_evaluation = evaluate(args.dev_file, ngram_lm)
    dev_evaluation['corpus'] = 'dev'
    out_directory = Path("results/model_evaluations")
    out_directory.mkdir(exist_ok=True, parents=True)

    pd.DataFrame([train_evaluation, dev_evaluation],
                columns=['Corpus', 'Log_prob', 'Perplexity'],
                ).to_csv(out_directory / f"{args.out_filename}.csv",
                        index=False)


if __name__ == "__main__" :    
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
    main(parser.parse_args())
