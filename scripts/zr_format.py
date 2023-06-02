import argparse
import sys
from pathlib import Path
import pandas as pd
import numpy as np
import random
import shutil
from pydub import AudioSegment
from tqdm import tqdm

def get_gold(in_folder, subtasks, voices):
    out = pd.DataFrame()
    for subtask in subtasks:
        sentences = pd.read_csv(in_folder / (subtask + '.csv'), header=None, sep='\t')
        gr_sentences = sentences.iloc[:, 0].values
        ungr_sentences = sentences.iloc[:, 1].values
        sub_out = pd.DataFrame([item[:-1] for pair in zip(gr_sentences, ungr_sentences) for item in pair],
                               columns=['transcription'])
        sub_out['type'] = subtask
        sub_out['subtype'] = subtask
        out = pd.concat([out, sub_out], axis=0)

    # Now that we have every sentences (grammatical or ungrammatical) in one dataframe, we'll:
    # Assign them an id (trial-wise)
    out.reset_index(drop=True, inplace=True)
    out['id'] = out.index // 2 + 1
    # Duplicate it for each voice
    out2 = pd.DataFrame()
    for voice in voices:
        out['voice'] = voice[-1]
        out['filename'] = out['transcription'].apply(lambda x: x.replace(' ', '_') + '_' +  voice)
        out2 = pd.concat([out2, out])
    out2 = out2.sort_values(by=['id', 'voice'])
    out2['correct'] = 0
    out2.loc[::2, 'correct'] = 1
    out2 = out2[['id', 'filename', 'voice', 'type', 'subtype', 'correct', 'transcription']]
    return out2


def split_dev_test(gold, subtask_sizes, dev_prop, dev_voices):
    nb_voices = len(gold['voice'].unique())
    expected_nb_stimuli = np.sum([s*nb_voices*2 for s in subtask_sizes])
    if expected_nb_stimuli != len(gold):
        print('Expected number of stimuli: %d' % expected_nb_stimuli)
        print('Number of stimuli: %d' % len(gold))
        print('Probably the number of sentences has changed... '
              'You should modify the python variables of this script: subtasks_sizes & dev_prop')
        exit()

    # Split dev/test voices
    dev_voices = [v[-1] for v in dev_voices]
    nb_dev_voices = len(dev_voices)
    nb_test_voices = nb_voices - len(dev_voices)
    dev_gold = gold[gold.voice.isin(dev_voices)]
    test_gold = gold[~gold.voice.isin(dev_voices)]

    # Split dev/test trials
    ids = gold.id.unique()
    np.random.seed(42)
    np.random.shuffle(ids) # this is done in place.
    dev_ids = ids[0:int(len(ids)*dev_prop)]
    test_ids = ids[int(len(ids)*dev_prop):]
    dev_gold = dev_gold[dev_gold.id.isin(dev_ids)].reset_index(drop=True)
    test_gold = test_gold[test_gold.id.isin(test_ids)].reset_index(drop=True)
    dev_gold['id'] = dev_gold.index // (2*nb_dev_voices) + 1
    test_gold['id'] = test_gold.index // (2*nb_test_voices) + 1
    return dev_gold, test_gold


def main(argv):
    parser = argparse.ArgumentParser(description='This scripts mimics zerospeech 2021 format '
                                                 'and split into dev and test sets.')
    parser.add_argument('--input', type=str, default='data/synth',
                        help='Path where to find the .ogg files that have been synthetized.')
    parser.add_argument('--sentences', type=str, default='data/tasks',
                        help='Where to find the sentences (textual version).')
    parser.add_argument('--out', type=str, default='data/zr_format',
                        help='Path where the output will be stored.')
    args = parser.parse_args(argv)
    args.input = Path(args.input)
    args.sentences = Path(args.sentences)

    args.out = Path(args.out)
    (args.out / 'syntactic' / 'dev').mkdir(parents=True, exist_ok=True)
    (args.out / 'syntactic' / 'test').mkdir(parents=True, exist_ok=True)

    voices = ['en-US-Wavenet-A', 'en-US-Wavenet-B', 'en-US-Wavenet-C', 'en-US-Wavenet-D', 'en-US-Wavenet-E',
              'en-US-Wavenet-F', 'en-US-Wavenet-G', 'en-US-Wavenet-H', 'en-US-Wavenet-I', 'en-US-Wavenet-J']
    subtasks = ['adj_noun_order', 'anaphor_number_agreement', 'noun_verb_agreement',
                'anaphor_gender_agreement', 'determiner_noun_agreement', 'noun_verb_order']

    # 1) Create gold file, in a ZR-2021-like format
    gold_data = get_gold(args.sentences, subtasks, voices)

    # 2) Split into dev & test
    subtasks_sizes = [1600, 1000, 2000, 1000, 3600, 1600]
    dev_prop = 0.2
    dev_voices = ['en-US-Wavenet-B', 'en-US-Wavenet-I']
    dev_gold, test_gold = split_dev_test(gold_data, subtasks_sizes, dev_prop, dev_voices)

    # 3) Save gold.csv and copy .wav files
    dev_gold.to_csv(args.out / 'syntactic' / 'dev' / 'gold.csv', index=False, sep=',')
    test_gold.to_csv(args.out / 'syntactic' / 'test' / 'gold.csv', index=False, sep=',')

    print("Converting dev files.")
    for filename, subtask in tqdm(zip(dev_gold['filename'], dev_gold['type'])):
        voice = filename.split('_')[-1]
        filename = '_'.join(filename.split('_')[:-1])
        input_file = args.input / 'audio' / subtask / voice / (filename + '.ogg')
        output_file = args.out / 'syntactic' / 'dev' / (filename + '_' + voice + '.wav')
        ogg = AudioSegment.from_ogg(input_file).set_frame_rate(16000).set_channels(1)
        ogg.export(output_file, format='wav')

    print("Converting test files.")
    for filename, subtask in tqdm(zip(test_gold['filename'], test_gold['type'])):
        voice = filename.split('_')[-1]
        filename = '_'.join(filename.split('_')[:-1])
        input_file = args.input / 'audio' / subtask / voice / (filename + '.ogg')
        output_file = args.out / 'syntactic' / 'test' / (filename + '_' + voice + '.wav')
        ogg = AudioSegment.from_ogg(input_file).set_frame_rate(16000).set_channels(1)
        ogg.export(output_file, format='wav')


if __name__ == "__main__":
    # execute only if run as a script
    args = sys.argv[1:]
    main(args)