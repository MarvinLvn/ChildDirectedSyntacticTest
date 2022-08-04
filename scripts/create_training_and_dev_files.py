"""This module will create text files storing tokenized utterances."""

from typing import List
from random import shuffle
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from preprocessing_tools import clean_utterance, phonemization, \
    phonemic_words_tokenization, phonemic_phonemes_tokenization

def write_utterances_in_text_files(utterances: list,
                output_orthographic_form_tokenized_in_words: Path,
                output_phonemic_form_tokenized_in_words: Path,
                output_phonemic_form_tokenized_in_phonemes: Path) -> None:
    """
    This function preprocess utterances and write them in\
    the corresponding files.
    
    Parameters
    ----------
    - utterances: list
        Utterances to prerocess and to write in the files.
    - 
    """
    for utterance in utterances :
        if not isinstance(utterance, str) or len(utterance) < 2:
            continue
        utterance = clean_utterance(utterance)
        if not utterance:
            continue
        output_orthographic_form_tokenized_in_words.write(f"{utterance}\n")
        utterance = phonemization(utterance)
        phonemized_tokenized_in_words = phonemic_words_tokenization(utterance)
        output_phonemic_form_tokenized_in_words.write(f"{phonemized_tokenized_in_words}\n")
        phonemized_tokenized_in_phonemes = phonemic_phonemes_tokenization(utterance)
        output_phonemic_form_tokenized_in_phonemes.write(f"{phonemized_tokenized_in_phonemes}\n")

def main(csvs_directory: str,
                            out_directory: str,
                            adults: List[str]=["Mother", "Father"]) -> None:
    """
    Create a training and development text files\
    containing all utterances produced by all the adults (Mother and Father)\
    from all the six families of the providence corpus.

    Parameters
    ----------
    - csvs_directory : str
        Directory where the csv files of the providence corpus\
        are stored.
    - out_directory : str
        Directory whre the text file produced by this script\
        will be stored.
    - speaker_roles : list
        The speaker roles to be considered as adults
    """
    input_directory = Path(csvs_directory)
    train_output_directory = Path(f"{out_directory}/train")
    dev_output_directory = Path(f"{out_directory}/dev")
    train_output_directory.mkdir(parents=True, exist_ok=True)
    dev_output_directory.mkdir(parents=True, exist_ok=True)

    # train files
    output_orthographic_form_tokenized_in_words_train = open((train_output_directory \
        / Path("providence_orthographic_form_tokenized_in_words.train")),
                                        mode="w",
                                        encoding="utf-8")
    output_phonemic_form_tokenized_in_words_train = open((train_output_directory \
        / Path("providence_phonemic_form_tokenized_in_words.train")),
                                    mode="w",
                                    encoding="utf-8")
    output_phonemic_form_tokenized_in_phonemes_train = open((train_output_directory \
        / Path("providence_phonemic_form_tokenized_in_phonemes.train")),
                                    mode="w",
                                    encoding="utf-8")
    # dev files
    output_orthographic_form_tokenized_in_words_dev = open((dev_output_directory \
        / Path("providence_orthographic_form_tokenized_in_words.dev")),
                                        mode="w",
                                        encoding="utf-8")
    output_phonemic_form_tokenized_in_words_dev = open((dev_output_directory \
        / Path("providence_phonemic_form_tokenized_in_words.dev")),
                                    mode="w",
                                    encoding="utf-8")
    output_phonemic_form_tokenized_in_phonemes_dev = open((dev_output_directory \
        / Path("providence_phonemic_form_tokenized_in_phonemes.dev")),
                                    mode="w",
                                    encoding="utf-8")
    csv_files = list(input_directory.glob("*.csv"))
    total_csv_files = len(csv_files)
    for csv_file in tqdm(csv_files, total=total_csv_files):
        csv = pd.read_csv(csv_file)
        adult_utterances = csv.loc[csv.speaker_role.isin(adults)]
        utterances = list(adult_utterances.gloss)
        # split the corpus in training and dev parts
        dev_part = len(utterances) * 0.10 # 10 percent for the development corpus
        shuffle(utterances)
        dev_utterances = utterances[:int(dev_part)]
        train_utterances = utterances[int(dev_part):]
        # create the training files
        write_utterances_in_text_files(train_utterances,
                                    output_orthographic_form_tokenized_in_words_train,
                                    output_phonemic_form_tokenized_in_words_train,
                                    output_phonemic_form_tokenized_in_phonemes_train)
        # create the development files
        write_utterances_in_text_files(dev_utterances,
                                    output_orthographic_form_tokenized_in_words_dev,
                                    output_phonemic_form_tokenized_in_words_dev,
                                    output_phonemic_form_tokenized_in_phonemes_dev)

    output_orthographic_form_tokenized_in_words_train.close()
    output_phonemic_form_tokenized_in_words_train.close()
    output_phonemic_form_tokenized_in_phonemes_train.close()

    output_orthographic_form_tokenized_in_words_dev.close()
    output_phonemic_form_tokenized_in_words_dev.close()
    output_phonemic_form_tokenized_in_phonemes_dev.close()

if __name__ == "__main__" :
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--csvs_directory",
                        help="The directory containing the csv files.",
                        required=True)
    parser.add_argument("--out_directory_name",
                        help="The directory where outputs will be stored.",
                        required=True)
    args = parser.parse_args()
    main(args.csvs_directory, args.out_directory_name)