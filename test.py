from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

clip = VideoFileClip("rates.mp4")

text = TextClip("Hola QvaPay!", fontsize=80, color="white")
text = text.set_position(("center", "center")).set_duration(clip.duration)

final = CompositeVideoClip([clip, text])
final.write_videofile("rates_test.mp4", codec="libx264", audio_codec="aac")