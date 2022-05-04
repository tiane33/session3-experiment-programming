from psychopy import core, visual, event

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
    def __init__(self, experiment, name, stimulus, fixation_time=0.5, max_key_wait=5, keys=['y', 'm']):
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

#from experiment_classes import Experiment, Item, Trial
import pandas as pd
import numpy as np

experiment = Experiment((800, 600), (-1, -1, -1), (1, 1, 1))

experiment.show_fixation(2)

stimuli = pd.read_csv('picture_verification_stimuli.csv')
items = []
for index, stimulus in stimuli.iterrows():
    items.append(Item(experiment, stimulus['item'], stimulus['image_file']))

trials = []
for item in items:
    trials.append(Trial(experiment, f'{item.name}_text', item.text))
    trials.append(Trial(experiment, f'{item.name}_image', item.image))

distractors = np.concatenate((trials[1:], trials[:1]))
pairs = list(zip(trials, distractors))
trials = np.random.permutation(pairs)

#trials = np.random.permutation(trials)
results = []
for trial in trials:
    results.append(trial.run())

results = pd.DataFrame(results)
results['reaction_time'] = results['end_time'] - results['start_time']
results.to_csv('demo_output.csv')