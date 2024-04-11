import os
from dotenv import load_dotenv
from typing import List
import json

load_dotenv()

TOKEN: str = os.getenv("DISCORD_TOKEN")
COMMAND_PREFIX: str = os.getenv("COMMAND_PREFIX")
SUPER_ADMIN: List[str] = json.loads(os.getenv("SUPER_ADMIN"))  # [...,"username"]

### Config ffmpeg
ffmpeg_options = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": '-vn -filter:a "volume=0.25"',
}
