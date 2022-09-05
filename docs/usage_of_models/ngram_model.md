```python
# import the ngram language model class
from scripts.models.ngrams_tools import NGramLanguageModel

# create an instance of a ngram language model
ngram_lm = NGramLanguageModel(
    # Add fake tokens at the beginning and ending of each utterance
    pad_utterances=True,
    # A trigram language model
    ngram_size=3,
    # The smooth value for dealing with unknown ngrams. Default=1e-3
    smooth=1e-6
    )

# Train the ngram language model. The estimation function takes as input a raw text file\
# with one sentence per line. These sentences must already be preprocessed and tokenized.
ngram_lm.estimate(
    train_file="path/to/training_file", # training file
    )

# And you can now use this model. For example, to get the log-probability of a sentence:

ngram_lm.assign_logprob("The cat hunts the mouse")

# You can then save the parameters of the model (the ngram counts)
ngram_lm.save_model(
    out_dirname="folder/where/store/the/model",
    out_filename="the_model_name"
    )
```

The model is now stored somewhere. It is always possible to reload and reuse it:

```python
# Instatiate a ngram language model
ngram_lm = NGramLanguageModel()

# Load the parameters already estimated
ngram_lm.load_model(path="path/to/the/stored/parameters")

# And you can now use this model. For example, to get the log-probability of a sentence:
ngram_lm.assign_logprob("The cat hunts the mouse")
```