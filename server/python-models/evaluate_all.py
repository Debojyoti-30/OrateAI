import sys
import json

def fake_analysis(video_path):
    return {
        "facial": "mostly confident",
        "tone": "calm and clear",
        "body": "open posture",
        "score": 87
    }

if __name__ == "__main__":
    video_path = sys.argv[1]
    result = fake_analysis(video_path)
    print(json.dumps(result))
