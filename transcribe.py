from youtube_transcript_api import YouTubeTranscriptApi
import time
time_init = time.time()
yt = YouTubeTranscriptApi.get_transcript('9t6Fs-1tEQI')
subtitle = ''
for t in yt:
    print(t['text'])
    subtitle+=' '+t['text']
# for t in YouTubeTranscriptApi.get_transcript('nC9i0zi1DCE'):#("IA3WxTTPXqQ"):
#     print(t['text'])
#     pass
print(subtitle)
print(time.time()-time_init)