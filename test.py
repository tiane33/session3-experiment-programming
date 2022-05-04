import pandas as pd
from psychopy import core, sound, visual, event
import numpy as np

stimuli = pd.read_csv('picture_verification_stimuli.csv')

stimuli

stimuli_dataframe = pd.DataFrame(stimuli)



print(stimuli['item'])