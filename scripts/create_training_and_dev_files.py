"""This module will create text files storing tokenized utterances."""

import random
from argparse import ArgumentParser
from random import shuffle
from pathlib import Path
import pandas as pd
from tqdm import tqdm
from preprocessing_tools import clean_utterance, phonemization, phonemic_phonemes_tokenization

random.seed(1798)

def write_utterances_in_text_files(utterances: list,
                output_orthographic_form_tokenized_in_words: Path,
                output_phonemic_form_tokenized_in_phonemes: Path) -> None:
    """
    This function preprocess utterances and write them in\
    the corresponding files.

    Parameters
    ----------
    - utterances: list
        Utterances to preprocess and to write in the files.
    - output_orthographic_form_tokenized_in_words: Path
        The file that will store utterances in orthographic form\
        and tokenized in words.
    - output_phonemic_form_tokenized_in_phonemes: Path
        The file that will store utterances in phonemic form\
        and tokenized in phonemes.
    """
    for utterance in utterances :
        if not isinstance(utterance, str) or len(utterance) < 2:
            continue
        utterance = clean_utterance(utterance)
        if not utterance:
            continue
        output_orthographic_form_tokenized_in_words.write(f"{utterance}\n")
        utterance = phonemization(utterance)
        phonemized_tokenized_in_phonemes = phonemic_phonemes_tokenization(utterance)
        output_phonemic_form_tokenized_in_phonemes.write(f"{phonemized_tokenized_in_phonemes}\n")

def main(args) -> None:
    """
    Create a training and development text files containing all\
    the utterances produced by all the adults (Mother and Father)\
    from all the six families of the providence corpus.
    """

    # In this study, we consider utterances produced\
    # by the mother and the father
    adults = ["Mother", "Father"]
    input_providence_csvs_directory = Path(args.csvs_directory)
    train_output_directory = Path(f"{args.out_directory}/train")
    dev_output_directory = Path(f"{args.out_directory}/dev")
    train_output_directory.mkdir(parents=True, exist_ok=True)
    dev_output_directory.mkdir(parents=True, exist_ok=True)

    # train files
    output_orthographic_form_tokenized_in_words_train = open((train_output_directory \
        / "providence_orthographic_form_tokenized_in_words.train"),
                                        mode="w",
                                        encoding="utf-8")
    output_phonemic_form_tokenized_in_phonemes_train = open((train_output_directory \
        / "providence_phonemic_form_tokenized_in_phonemes.train"),
                                        mode="w",
                                        encoding="utf-8")
    # dev files
    output_orthographic_form_tokenized_in_words_dev = open((dev_output_directory \
        / "providence_orthographic_form_tokenized_in_words.dev"),
                                        mode="w",
                                        encoding="utf-8")
    output_phonemic_form_tokenized_in_phonemes_dev = open((dev_output_directory \
        / "providence_phonemic_form_tokenized_in_phonemes.dev"),
                                        mode="w",
                                        encoding="utf-8")

    providence_csv_files = list(input_providence_csvs_directory.glob("*.csv"))
    total_csv_files = len(providence_csv_files)
    for children_csv in tqdm(providence_csv_files, total=total_csv_files):
        loaded_children_csv = pd.read_csv(children_csv)
        adult_data = loaded_children_csv.loc[loaded_children_csv.speaker_role.isin(adults)]
        adult_utterances = list(adult_data.gloss)
        # split the corpus in training and dev parts
        development_part = len(adult_utterances) * 0.10 # 10 percent for the development corpus
        shuffle(adult_utterances)
        development_utterances = adult_utterances[:int(development_part)]
        trainining_utterances = adult_utterances[int(development_part):]
        # create the training files
        write_utterances_in_text_files(trainining_utterances,
                                    output_orthographic_form_tokenized_in_words_train,
                                    output_phonemic_form_tokenized_in_phonemes_train)
        # create the development files
        write_utterances_in_text_files(development_utterances,
                                    output_orthographic_form_tokenized_in_words_dev,
                                    output_phonemic_form_tokenized_in_phonemes_dev)

    output_orthographic_form_tokenized_in_words_train.close()
    output_phonemic_form_tokenized_in_phonemes_train.close()

    output_orthographic_form_tokenized_in_words_dev.close()
    output_phonemic_form_tokenized_in_phonemes_dev.close()

if __name__ == "__main__" :
    parser = ArgumentParser()
    parser.add_argument("--csvs_directory",
                        help="The directory containing the csv files.",
                        required=True)
    parser.add_argument("--out_directory",
                        help="The directory where outputs will be stored.",
                        required=True)
    main(parser.parse_args())
