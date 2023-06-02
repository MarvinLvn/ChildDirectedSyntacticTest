# Child-directed syntactic probing

### What does the task consist of?

In this task, the participant (be it a human or a machine) receives two spoken (or written) sentences, one of which is a grammatical sentence, the other one being an ungrammatical sentence.
For instance: `I like candies` versus `I likes candies`. The participant is then asked to decide which of the two sentence is the grammatical one. If the participant fails, it obtains a score of 0, if it succeeds a score of 1.
The accuracy is computed as the proportion of trials for which the participant succeeded in finding the grammatical sentence.

When considering a machine participant, one has to extract the probability of the sentence, which is expected to be higher for the grammatical sentence than for the ungrammatical one (how to extract this measure of probability is one of the numerous design choice the programmer is faced with). 

### Examples of stimuli

<center>

| Phenomenon                | Sentence example                                                      |
|---------------------------|-----------------------------------------------------------------------|
| Adjective-noun order      | ✓ The good mom. <br> ✗ The mom good.                                  |
| Noun-verb order           | ✓ The dragon says. <br> ✗ The says dragon.                            |
| Anaphor-gender agreement  | ✓ The dad cuts himself. <br> ✗ The dad cuts herself.                  |
| Anaphor-number agreement  | ✓The boys told themselves. <br> ✗ The boys told himself.              |
| Determiner-noun agreement | ✓ Each good sister. <br> ✗ Many good sister.                          |
| Noun-verb agreement       | ✓ The prince needs the princess. <br> ✗ The prince need the princess. |

Table 2: Minimal pairs of grammatical (✓)  and ungrammatical (✗) sentences used in the syntactic task.
</center>

### Getting started

1. [Install](./docs/installation.md)
2. [Create the evaluation set](./docs/build_evaluation.md)
3. [Run the tasks](./docs/run_tasks.md)