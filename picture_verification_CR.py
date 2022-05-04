import pandas as pd
from psychopy import core, sound, visual, event
import numpy as np

stimuli = pd.read_csv('picture_verification_stimuli.csv')

window = visual.Window()
message = visual.TextStim(window)
clock = core.Clock()


class Experiment:
    def __init__(self, window_size, text_color, background_color):
        self.text_color = text_color
        self.window = visual.Window(window_size, color=background_color)
        self.fixation = visual.TextStim(self.window, '+', color=text_color)
        self.clock = core.Clock()
    
    def show_fixation(self, time=0.5):
        self.fixation.draw()
        self.window.flip()
        core.wait(time)

class Item:
    def __init__(self, experiment, name, image_path):
        self.experiment = experiment
        self.name = name
        self.text = visual.TextStim(experiment.window, text=name, color=experiment.text_color)
        self.image = visual.ImageStim(experiment.window, image=image_path)

class Trial:
    def __init__(self, experiment, name, stimulus, fixation_time=0.5, max_key_wait=5, keys=['z', 'm']):
        self.name = name
        self.experiment = experiment
        self.stimulus = stimulus
        self.fixation_time = fixation_time
        self.max_key_wait = max_key_wait
        self.keys = keys
    
    def run(self):
        self.experiment.show_fixation(self.fixation_time)

        self.stimulus.draw()
        self.experiment.window.flip()
        
        start_time = self.experiment.clock.getTime()
        keys = event.waitKeys(maxWait=self.max_key_wait, keyList=self.keys, timeStamped=self.experiment.clock, clearEvents=True)
        if keys is not None:
            key, end_time = keys[0]
        else:
            key = None
            end_time = self.experiment.clock.getTime()
        
        return {
            'trial': self.name,
            'start_time': start_time,
            'end_time': end_time,
            'key': key
        }

items = []
for index, stimulus in stimuli.iterrows():
    items.append()

images = []
for item_path in stimuli['image_file']:
    image_stim = visual.ImageStim(window, image=item_path)
    images.append(image_stim)
words = []
for word in stimuli['text']:
    text_stim = visual.TextStim(window, text=word)
    words.append(text_stim)
items = []
for item in stimuli['item']:
    text_stim = visual.TextStim(window, text=item)
    items.append(text_stim)

images = np.random.permutation(images)
words = np.random.permutation(words)

message.text = "Welcome to the experiment!"
message.draw()
window.flip()
core.wait(2.0)

results = []

for image in images:
    message.text = stimuli['text']
    message.draw()
    window.flip()
    core.wait(2.0)
    image.draw()
    window.flip()
    # clock.reset()
    start_time = clock.getTime()
    keys = event.waitKeys(maxWait=5, keyList=['y', 'm'], timeStamped=clock, clearEvents=True)
    if keys is not None:
        key, end_time = keys[0]
    else:
        key = None
        end_time = clock.getTime()
    
    results.append({
        'start_time': start_time,
        'end_time': end_time,
        'key': key
    })

results = pd.DataFrame(results)
results['reaction_time'] = results['end_time'] - results['start_time']
results.to_csv('demo_output.csv')