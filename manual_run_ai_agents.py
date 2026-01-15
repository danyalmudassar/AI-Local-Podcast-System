from podcast_agent import AudioEngine
import os

def generate_ai_agents_episode():
    topic = "AI Agents"
    output_file = "ai_agents_podcast.wav"
    
    # Pre-written script about AI Agents
    script = """
Host: Welcome back to Future Tech. Today, we're diving into AI Agents.
Guest: Oh yeah. These aren't just chatbots anymore, right?
Host: Exactly. They can actually DO things. Book flights, write code...
Guest: So, like a personalized digital intern?
Host: Precisely. Imagine an agent that manages your entire calendar.
Guest: That sounds amazing, but also a bit scary.
Host: It is a game changer. The future is agentic.
GUEST: I can't wait to see where this goes.
Host: We'll keep you posted. Thanks for listening!
    """
    
    print(f"Generating manual episode for: {topic}")
    
    # Save script
    with open("script.txt", "w") as f:
        f.write(script.strip())

    engine = AudioEngine()
    clips = []
    
    lines = script.strip().split('\n')
    idx = 0
    for line in lines:
        line = line.strip()
        if not line: continue
        
        if ":" in line:
            speaker, text = line.split(":", 1)
            speaker = speaker.strip().capitalize()
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
    generate_ai_agents_episode()
