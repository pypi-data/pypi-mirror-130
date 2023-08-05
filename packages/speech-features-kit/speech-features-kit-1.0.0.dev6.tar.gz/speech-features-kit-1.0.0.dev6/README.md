# Speech Feature Kit

A Python wrapper for convenient speech feature extraction

## Installation
```python
pip install speech-features-kit
```

## Functions
1. MFCC feature analysis
2. Volume analysis
3. Emotion analysis

## Example of emotion analysis
```python
from speech_features_kit.Emotion.speech_toolkit import SpeechEmotionToolkit

# set the path of pre-trained model for speech emotion model
# the used model here is optimized for Chinese speech; however, it is possible you can train your own model. 
speech_kit = SpeechEmotionToolkit()

# load the model
speech_kit.load()

# obtain emotion list with timestamp given an audio file
list_emo, list_timestamp = speech_kit.get_emotion_list_by_blocks(audio_file="../data/english.wav",
                                                                     num_sec_each_file=1)

# print the list of emotion over timestamp
print("Time interval\tEmotion")
for idx, e in enumerate(list_emo):
    print(list_timestamp[idx], "\t", e)

```

## Note
Other functions please see the examples folder!

