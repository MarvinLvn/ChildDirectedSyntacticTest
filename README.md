# Child-directed syntactic probing

### What does the task consist of?

In this task, the participant (be it a human or a machine) receives two spoken (or written) sentences, one of which is a grammatical sentence, the other one being an ungrammatical sentence.
For instance: `I like candies` versus `I likes candies`. The participant is then asked to decide which of the two sentence is the grammatical one. If the participant fails, it obtains a score of 0, if it succeeds a score of 1.
The accuracy is computed as the proportion of trials for which the participant succeeded in finding the grammatical sentence.

When considering a machine participant, one has to extract the probability of the sentence, which is expected to be higher for the grammatical sentence than for the ungrammatical one (how to extract this measure of probability is one of the numerous design choice the programmer is faced with). 

### How minimal pairs of sentences are generated?

WIP

### Getting started

1. [Install](./docs/installation.md)
2. [Create the evaluation set](./docs/build_evaluation.md)
3. [Compute the accuracy](./docs/compute_accuracy.md)