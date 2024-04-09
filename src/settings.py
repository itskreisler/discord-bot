import os

TOKEN:str = os.environ.get('DISCORD_TOKEN')

### Config ffmpeg
ffmpeg_options = {
  'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
  'options': '-vn -filter:a "volume=0.25"'
  }