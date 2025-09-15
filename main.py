from pydantic import BaseModel
from moviepy import *
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
import pickle
from typing import List
import whisper

client = OpenAI(api_key="")

class Commentary(BaseModel):
    commentary: str
    start_time : float
    end_time : float
    
class CommentaryList(BaseModel):
    events: List[Commentary]
    
def get_times(transcription):
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"""Given the transcription of a soccer game, I want to get highlights by extracting short commentaries.
                Start with introduction or start of the game(3-4 sentences).
                Then extract at least 10 key actions(passes, fouls, goals) describing each action in 4-6 sentences. Strictly maintain the order.
                Finally describe the end of the game or session in 3-4 sentences.
                Return commentary, start time and end time maintaing the order. Never go backwards.
                transcription: {transcription}""",
                }
            ],
            }
        ],
        response_format=CommentaryList,
        temperature=0.1
        )
    return response.choices[0].message.parsed


def merge_clips(path:str,highlights:list[Commentary]):
    video = VideoFileClip(path)
    clips = [video.subclipped(int(k.start_time), int(k.end_time)) for k in highlights]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile("merged_clip.mp4", codec="libx264", audio_codec="aac")
    

if __name__ == "__main__":
    path = "match3.mp4"
    video = VideoFileClip(path)
    audio = video.audio
    audio.write_audiofile("match_audio.mp3")
    model = whisper.load_model("base.en")
    result = model.transcribe("match_audio.mp3")
    print(result)
    with open('transc.pickle', 'wb') as handle:
        pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('transc.pickle', 'rb') as handle:
        result = pickle.load(handle)
    temp = []
    words = []
    for seg in result["segments"]:
        temp.append({"text":seg["text"],"start":seg["start"], "end":seg["end"]})
        words.extend(seg["text"].split())
    print(temp)
    print(len(words))
    final_response = get_times(temp)
    print(final_response.events)
    with open('transcr.pickle', 'wb') as handle:
        pickle.dump(final_response.events, handle, protocol=pickle.HIGHEST_PROTOCOL)
    merge_clips(path,final_response.events)
