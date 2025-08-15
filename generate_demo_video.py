from gtts import gTTS
import moviepy.editor as mpy

lines = [
    "Meet PonyXpress — a delivery platform designed for the real world.",
    "Scan packages, map routes, and keep going — even without signal.",
    "Auto-sync your deliveries with the cloud once you're back online.",
    "Run it on web, Android, or desktop — no matter the terrain.",
    "PonyXpress — Deliver Anywhere."
]

# Generate audio clips
audio_paths = []
for i, line in enumerate(lines):
    tts = gTTS(text=line, lang='en')
    path = f"vo{i}.mp3"
    tts.save(path)
    audio_paths.append(path)

# Load and combine
clips = [mpy.AudioFileClip(p) for p in audio_paths]
full_audio = mpy.concatenate_audioclips(clips)
base = mpy.ColorClip((1280, 720), color=(0, 0, 0), duration=full_audio.duration).set_audio(full_audio)

text_clips = []
timestamps = [0, 4, 9, 14, 19]
for i, (line, start) in enumerate(zip(lines, timestamps)):
    txt = mpy.TextClip(line, fontsize=40, color='white', method='caption', size=(1100, None))
    txt = txt.set_start(start).set_duration(4).set_position("center")
    text_clips.append(txt)

final = mpy.CompositeVideoClip([base, *text_clips])
final.write_videofile("ponyxpress_demo.mp4", fps=24, codec="libx264", audio_codec="aac")
