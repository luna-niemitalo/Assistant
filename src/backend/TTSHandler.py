import json
import os
import sys
import time
from RealtimeTTS import TextToAudioStream, SystemEngine, AzureEngine, ElevenlabsEngine, GTTSEngine, GTTSVoice, CoquiEngine


def replay_from_json_file(filename):
    """Reads from a JSON file and replays the saved entries."""
    global entries
    with open(filename, 'r') as file:
        entries = json.load(file)
        prev_ts = 1722090250721282400
        for entry in entries:
            ts = entry['timestamp']
            param = entry['parameter']
            delay = ts - prev_ts
            prev_ts = ts
            sleepTime = delay / 1_000_000_000
            time.sleep(sleepTime)
            print(f"Replaying: {param}")
            yield(param)


if __name__ == "__main__":
    #engine = GTTSEngine(voice=GTTSVoice("en", "com", speed_increase=1.5))
    engine = CoquiEngine()
    stream = TextToAudioStream(engine)
    text_stream = replay_from_json_file("recursion.json")
    stream.feed(text_stream)
    stream.play_async()
    while stream.is_playing():
        time.sleep(0.1)