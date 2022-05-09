## Download CHILDES transcriptions

1) Download transcripts from CHILDES:

```bash
python scripts/download_transcript.py
```

This will create a file `data/transcripts/sentences.csv` that contain all sentences of American English CHILDES.

2) Extract nouns, adjectives and verbs that will be used in the evaluation sentences:

```bash
python scripts/find_word_candidates.py
```

By default, the script extract the 100 most frequent nouns (resp. adjectives, resp. verbs) whose POS probability of 
being a noun (resp. adj, resp. verb) is greater than 0.95. However, you may need to extract more words, in which case you
should set the `--n_to_keep` parameter. Although, bare in mind that this will require more manual work !

## Manual work & task generation

Once you have extracted words that will be used in the evaluation sentences, you'll need to further split them 
(and this depends on the syntactic task you want to generate).

### 1) At the beginning of syntax: part-of-speech prder

This consists of minimal pair (`The <ADJ> <NOUN>.` versus `The <NOUN> <ADJ>`) and (`The <NOUN> <VERB>` and `The <VERB> <NOUN>`).
Example: 
1) `The good cat.` vs `The cat good.`
2) `The kitty lets.` vs`The lets kitty.`

To generate this task, you'll need a file `data/word_candidates/nouns_animate.csv` that contain animate nouns.

### 2) Anaphor agreement

#### A) Anaphor gender agreement:

To generate this task, you'll need:
- a file `data/word_candidates/nouns_gendered.csv` that contain gendered nouns (along with their plural form and their gender)
- a file `data/word_candidates/verbs_reflexive.csv` that contain reflexive verbs (a verb whose object is the same as its subject).

Note: this leads to quite unnatural sentences that are more present in self-motivational quotes than child-directed speech...
Note 2: I gave myself (here's an example of reflexive pronoun) some freedom and moved away from CHILDES verbs.

#### B) Anaphor number agreement

To generate this task, you'll need:
- a file `data/word_candidates/nouns_gendered.csv` that contain gendered nouns (along with their plural form and their gender)
- a file `data/word_candidates/verbs_reflexive.csv` that contain reflexive verbs (a verb whose object is the same as its subject).

Note: Verbs are conjugated to past tense (to avoid any mismatch between singular and plural in the present form). i
If you re-generate this task, you should check that verbs correctly conjugated (see `conjugate_verb` function in which we had to fix
many mistakes made by the automatic conjugator).

### 3) Determiner noun agreement

To generate this task, you'll need:
- a file `data/word_candidates/nouns_gendered.csv` that contain gendered nouns (along with their plural form and their gender)

### 4) Noun verb agreement





