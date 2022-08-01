"""This module will compute accuracies on the different tasks."""
import csv
from typing import Dict
from pathlib import Path
from tqdm import tqdm
from paraphone.ngrams_tools import NGramLanguageModel

def run_tasks(tasks_folder: str,
                ngram_lm: NGramLanguageModel,
                phonemized: bool,
                tokenized_in_words: bool) -> Dict[str, float] :
    """
    Run the tasks on ngram language model.

    Parameters
    ----------
    - tasks_folder: str
        The folder containing the task csvs
    - ngram_lm: NGramLanguageModel
        The ngram language model object
    - phonemized: bool
        Whether phonemize or not the utterance
    - tokenized_in_words: bool
        Whether tokenize the model in words or not
    
    Return
    ------
    - dict:
        Dictionnaty mapping tasks and their accuracy.
    """
    task_csvs = list(Path(tasks_folder).glob("*.csv"))
    total_tasks = len(task_csvs)
    task_scores = {}
    for task in tqdm(task_csvs, total=total_tasks) :
        task_name = task.stem
        total = 0.0
        goods = 0.0
        with open(task, mode="r", encoding="utf-8") as task_file :
            task_csv = csv.reader(task_file, delimiter="\t")
            for real_sentence, modified_sentence in task_csv :
                real_sentence, modified_sentence = real_sentence.strip(), modified_sentence.strip()
                real_sentence = preprocess(real_sentence, phonemized, tokenized_in_words)
                modified_sentence = preprocess(modified_sentence, phonemized, tokenized_in_words)
                real_sentence = list(ngram_lm.get_ngrams(real_sentence.split(" ")))
                modified_sentence = list(ngram_lm.get_ngrams(modified_sentence.split(" ")))
                goods += (int(ngram_lm.to_ngram_logprob(real_sentence) > \
                                ngram_lm.to_ngram_logprob(modified_sentence)))
                total += 1
        task_scores[task_name] = goods / total
    return task_scores

if __name__ == "__main__" :
    from argparse import ArgumentParser
    import csv
    print("Loading phonemizer...")
    from preprocessing_tools import preprocess
    print("Phonemizer loaded !")
    parser = ArgumentParser()
    parser.add_argument("--train_file",
                        type=str,
                        help="The directory containing the train file.",
                        required=True)
    parser.add_argument("--tasks_folder",
                    type=str,
                    help="The folder containing the tasks",
                    required=True)
    parser.add_argument("--ngram_model",
                        type=str,
                        help="The trained ngram model.",
                        required=True)

    parser.add_argument('--phonemize', action='store_true')
    parser.add_argument('--no-phonemize', dest='phonemize', action='store_false')
    parser.add_argument('--tokenize_in_words', action='store_true')
    parser.add_argument('--no-tokenize_in_words', dest='tokenize_in_words', action='store_false')
    parser.add_argument("--out_filename",
                        type=str,
                        help="The filename of the output file",
                        required=True)
    parser.set_defaults(feature=False)
    parser.set_defaults(tokenized_in_words=True)
    args = parser.parse_args()

    out_directory = Path("results")
    out_directory.mkdir(exist_ok=True, parents=True)
    ngram_lm = NGramLanguageModel()
    print("Loading the model...")
    ngram_lm.load_parameters(args.ngram_model)
    print("Running the tasks...")
    result_tasks = run_tasks(args.tasks_folder,
                                ngram_lm,
                                args.phonemize,
                                args.tokenize_in_words)
    with open(out_directory / Path(f"{args.out_filename}.csv"), "w") as out_csv:
        csv_writer = csv.writer(out_csv)
        for task, accuracy in result_tasks.items():
            csv_writer.writerow([task, accuracy])
