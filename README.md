# Highlights generator
* Takes a video as input
* Gets transcript along with timestamps using whisper
* Sends it to llm(openai)
* Uses structured output to extract key events
* Uses moviepy to merge key events and generate highlights

# Demo
* Here we tried for a soccer match
* youtube url: https://www.youtube.com/live/N-1f7nVEdOM?si=WdwlWa7GFQ0Y60Cp
* Result

![Demo](output.webp)

# Dependencies
* whisper, openai, moviepy

# How to run
* check `main.py`
* put your openai key, edit the prompt if you want, change the path to your video file path and run.



