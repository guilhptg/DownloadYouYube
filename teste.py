from pytubefix import *

yt = YouTube(input('Digite o url do video: '))

steam = yt.streams.get_audio_only()

steam.download()