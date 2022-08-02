"""This module will create text files storing tokenized utterances."""

from typing import List
from random import shuffle
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from preprocessing_tools import clean_utterance, phonemization, \
    phonemic_words_tokenization, phonemic_phonemes_tokenization, \
    remove_multiple_spaces

def write_utterances_in_text_files(utterances: list,
                                    output_orthographic_words: Path,
                                    output_phonemic_words: Path,
                                    output_phonemic_phonemes: Path) -> None:
    for utterance in utterances :
        if not utterance or not isinstance(utterance, str): 
            continue
        if len(utterance) == 1:
            continue
        utterance = clean_utterance(utterance)
        if not utterance:
            continue
        output_orthographic_words.write(f"{utterance}\n")
        utterance = phonemization(utterance)
        phonemic_words = phonemic_words_tokenization(utterance)
        phonemic_words = remove_multiple_spaces(phonemic_words)
        if not phonemic_words:
            continue
        output_phonemic_words.write(f"{phonemic_words}\n")
        phonemes = phonemic_phonemes_tokenization(utterance)
        phonemes = remove_multiple_spaces(phonemes)
        if not phonemes:
            continue
        output_phonemic_phonemes.write(f"{phonemes}\n")

def create_sentences_files(csvs_directory: str,
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
    output_orthographic_words_train = open((train_output_directory \
        / Path("providence_orthographic_tokenized_in_words.train")),
                                        mode="w",
                                        encoding="utf-8")
    output_phonemic_words_train = open((train_output_directory \
        / Path("providence_phonemic_tokenized_in_words.train")),
                                    mode="w",
                                    encoding="utf-8")
    output_phonemic_phonemes_train = open((train_output_directory \
        / Path("providence_phonemic_tokenized_in_phonemes.train")),
                                    mode="w",
                                    encoding="utf-8")
    # dev files
    output_orthographic_words_dev = open((dev_output_directory \
        / Path("providence_orthographic_tokenized_in_words.dev")),
                                        mode="w",
                                        encoding="utf-8")
    output_phonemic_words_dev = open((dev_output_directory \
        / Path("providence_phonemic_tokenized_in_words.dev")),
                                    mode="w",
                                    encoding="utf-8")
    output_phonemic_phonemes_dev = open((dev_output_directory \
        / Path("providence_phonemic_tokenized_in_phonemes.dev")),
                                    mode="w",
                                    encoding="utf-8")
    csv_files = list(input_directory.glob("*.csv"))
    total_csv_files = len(csv_files)
    for csv_file in tqdm(csv_files, total=total_csv_files):
        csv = pd.read_csv(csv_file)
        adult_utterances = csv.loc[csv.speaker_role.isin(adults)]
        utterances = list(adult_utterances["gloss"])
        # split the corpus in training and dev parts
        dev_part = len(utterances) * 0.10 # 10 percent for the development corpus
        shuffle(utterances)
        dev_paragraphs = utterances[:int(dev_part)]
        train_paragraphs = utterances[int(dev_part):]
        # create the training files and dev files
        write_utterances_in_text_files(dev_paragraphs,
                                    output_orthographic_words_dev,
                                    output_phonemic_words_dev,
                                    output_phonemic_phonemes_dev)

        write_utterances_in_text_files(train_paragraphs,
                                    output_orthographic_words_train,
                                    output_phonemic_words_train,
                                    output_phonemic_phonemes_train)

    output_orthographic_words_train.close()
    output_phonemic_words_train.close()
    output_phonemic_phonemes_train.close()

    output_orthographic_words_dev.close()
    output_phonemic_words_dev.close()
    output_phonemic_phonemes_dev.close()

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
    create_sentences_files(args.csvs_directory, args.out_directory_name)