from podcast_agent import AudioEngine
import os

def generate_manual_episode():
    topic = "Mars Colonization"
    output_file = "mars_podcast.wav"
    
    # Pre-written script to demonstrate multi-speaker logic
    script = """
Host: Welcome back to the Daily Tech! Today we're talking about the Red Planet.
Guest: Thanks for having me. Mars is looking more reachable than ever.
Host: Absolutely. SpaceX is targeting a Starship launch soon, right?
Guest: Yes, the goal is to have a self-sustaining city by 2050.
Host: That's ambitious! But what about the radiation?
Guest: We'll likely live in lava tubes underground.
Host: Sounds cozy. Thanks for the update!
    """
    
    print(f"Generating manual episode for: {topic}")
    
    # Save script for record
    with open("script.txt", "w") as f:
        f.write(script.strip())

    engine = AudioEngine()
    clips = []
    
    lines = script.strip().split('\n')
    idx = 0
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Simple extraction
        if ":" in line:
            speaker, text = line.split(":", 1)
            speaker = speaker.strip()
            text = text.strip()
        else:
            speaker = "Host"
            text = line
            
        print(f"Generating line {idx} ({speaker}): {text}")
        try:
            clip_path = engine.generate_clip(text, speaker, idx)
            clips.append(clip_path)
            idx += 1
        except Exception as e:
            print(f"Failed to generate line: {e}")

    print("Mixing final audio...")
    engine.mix_audio(clips, output_file)
    print(f"Audio generated: {output_file}")

if __name__ == "__main__":
    generate_manual_episode()
