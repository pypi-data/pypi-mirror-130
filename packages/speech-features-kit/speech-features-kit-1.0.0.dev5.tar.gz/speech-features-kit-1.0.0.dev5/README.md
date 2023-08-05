# Speech Feature Kit

A Python wrapper for convenient speech feature extraction

## Functions
1. MFCC feature analysis
2. Volume analysis
3. Emotion analysis

## Example of emotion analysis
```python
from speech_features_kit.Emotion.speech_toolkit import SpeechEmotionToolkit

# set the path of pre-trained model for speech emotion model
speech_kit = SpeechEmotionToolkit(
    model_path='../data/speech_emotion/speech_mfcc_model.h5',
    model_para_path='../data/speech_emotion/mfcc_model_para_dict.pkl')

# load the model
speech_kit.load()

# obtain emotion list with timestamp given an audio file
## num_sec_each_file: specify the number of seconds each chunk contains when dividing the audio file
list_emo, list_timestamp = speech_kit.get_emotion_list_by_blocks(audio_file="../data/speech_emotion/haodf.mp3",
                                                                     num_sec_each_file=5)

# print the list of emotion over timestamp
print("Time interval\tEmotion")
for idx, e in enumerate(list_emo):
    print(list_timestamp[idx], "\t", e)

```

## Note
Other functions please see the examples folder!

