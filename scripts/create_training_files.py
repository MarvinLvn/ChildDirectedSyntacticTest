"""This module will create text files storing tokenized utterances."""

from typing import List
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from preprocessing_tools import clean_utterance, phonemization, \
    phonemic_words_tokenization, phonemic_phonemes_tokenization, \
    remove_multiple_spaces

def create_sentences_files(csvs_directory: str,
                            out_directory: str,
                            adults: List[str]=["Mother", "Father"]) -> None:
    """
    Create a text file containing all utterances\
    produced by all the adults (Mother and Father)\
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
    output_directoty = Path(out_directory)
    output_directoty.mkdir(parents=True, exist_ok=True)
    output_orthographic_words = open((output_directoty \
        / Path("providence_orthographic_tokenized_in_words.txt")),
                                        mode="w",
                                        encoding="utf-8")
    output_phonemic_words = open((output_directoty \
        / Path("providence_phonemic_tokenized_in_words.txt")),
                                    mode="w",
                                    encoding="utf-8")
    output_phonemic_phonemes = open((output_directoty \
        / Path("providence_phonemic_tokenized_in_phonemes.txt")),
                                    mode="w",
                                    encoding="utf-8")
    csv_files = list(input_directory.glob("*.csv"))
    total_csv_files = len(csv_files)
    for csv_file in tqdm(csv_files, total=total_csv_files):
        csv = pd.read_csv(csv_file)
        adult_utterances = csv.loc[csv.speaker_role.isin(adults)]
        for utterance in adult_utterances["gloss"] :
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
    output_orthographic_words.close()
    output_phonemic_words.close()
    output_phonemic_phonemes.close()

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