import sys
import json

def analyze(video_path):
    return {
        "overall_score": 82,
        "facial_expression": {"happy": 65, "nervous": 20},
        "voice_analysis": {"clarity": "good", "filler_words": 5},
        "body_language": {"eye_contact": "moderate"}
    }

if __name__ == "__main__":
    video_path = sys.argv[1]
    result = analyze(video_path)
    print(json.dumps(result))
