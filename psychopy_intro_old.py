from psychopy import visual, sound, core

window = visual.Window(size=(400,400))
message = visual.TextStim(window)
note_c = sound.Sound("C", secs=1.0)
grating = visual.GratingStim(window, tex="sin", mask="gauss", sf=10, name="gabor")
image = visual.ImageStim(window, image="images/baby.png")
audio = sound.Sound("sounds/HF/baby.wav")

message.text = "Hello"
message.draw()
window.flip()
note_c.play()
core.wait(2.0)

grating.draw()
window.flip()
core.wait(2.0)

image.draw()
window.flip()
audio.play()
core.wait(2.0)

