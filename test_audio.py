from podcast_agent import AudioEngine
import os

def test_engine():
    print("Testing Audio Engine...")
    engine = AudioEngine()
    
    # Test Data
    lines = [
        ("Welcome to the show!", "Host"),
        ("Thanks for having me.", "Guest"),
        ("Let's talk about AI.", "Host")
    ]
    
    clips = []
    for idx, (text, speaker) in enumerate(lines):
        print(f"Generating line {idx} for {speaker}...")
        try:
            clip = engine.generate_clip(text, speaker, idx)
            clips.append(clip)
            print(f"  -> Created {clip}")
        except Exception as e:
            print(f"  -> Failed: {e}")
            return

    print("Mixing audio...")
    try:
        output = "test_mix.wav"
        engine.mix_audio(clips, output)
        if os.path.exists(output):
            print(f"SUCCESS: Created {output}")
        else:
            print("FAILURE: Output file not found")
    except Exception as e:
        print(f"Mixing failed: {e}")

if __name__ == "__main__":
    test_engine()
