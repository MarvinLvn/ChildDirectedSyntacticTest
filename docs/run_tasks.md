# 1) Get providence training data
First, activate the `cdsyn` conda environment. Then, run this command:
```bash
python scripts/download_providence_csvs.py --out_directory_name data/children_csvs
```

# 2) Run tokenizations and creation of text training files

Always being with the `cdsyn` environment, run this command:

```bash
python scripts/create_training_and_dev_files.py --csvs_directory data/children_csvs/ --out_directory_name data/tokenized/
```

For all the following steps, activate the `paraphone` environment

# 3) Run the models

Train and save models using paraphone scripts. For example, for a orthographic word level language model of order 5, run this command to train the model and save the model on a folder `trained` :

```bash
python scripts/models/ngram_lm.py --train_file data/tokenized/train/providence_orthographic_form_tokenized_in_words.train --out_directory trained --out_filename bigram_lm_orthographic_form_tokenized_in_words --ngram_size 2
```

# 4) Test the models on the syntactic tasks

Test the trained models in the previous step on the syntactic tasks. For example, for the fivegram orthographic words language model, run this command:

```bash
python scripts/run_tasks.py --tasks_folder data/tasks/ --no-phonemize --tokenize_in_words --ngram_model trained/trigram_lm_orthographic_form_tokenized_in_words.json --out_filename trigram_lm_orthographic_form_tokenized_in_words
```

`--phonemize` argument means whether phonemize or not the sentences. Since, this language model works on orthographic form, phonemization is not needed.

`--tokenize_in_words` argument means whether tokenize the sentences in words or not. This language model works with words, so we need the word tokenization.

All results will be stored on the `results/` folder