import os
import argparse
import re
import subprocess
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from crewai_tools import ScrapeWebsiteTool
from pydantic import BaseModel, Field
from typing import Type, List, Tuple

# --- Configuration ---
os.environ["OPENAI_API_KEY"] = "NA"
PIPER_BINARY = "./piper/piper"
VOICE_MODELS = {
    "Host": "./en_US-lessac-medium.onnx",
    "Guest": "./en_US-ryan-medium.onnx"
}
BACKGROUND_MUSIC = "./background_music.wav"

# --- 1. LLM Setup ---
# Default global LLM (will be overridden dynamically if needed, but we'll try to keep agents dynamic)
# local_llm = LLM(model="ollama/qwen2.5:0.5b", base_url="http://localhost:11434")

def get_ollama_models():
    """Returns a list of available Ollama models."""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        models = []
        # Skip header (NAME ID SIZE MODIFIED)
        for line in lines[1:]:
            parts = line.split()
            if parts:
                models.append(parts[0]) # The name column
        return models
    except Exception as e:
        print(f"Error fetching models: {e}")
        return ["qwen2.5:0.5b"] # Fallback

# --- 2. Tool Definitions ---
class SearchToolInput(BaseModel):
    query: str = Field(description="The search query.")

class SearchTool(BaseTool):
    name: str = "DuckDuckGoSearch"
    description: str = "Search the web for a query using DuckDuckGo."
    args_schema: Type[BaseModel] = SearchToolInput

    def _run(self, query: str) -> str:
        from duckduckgo_search import DDGS
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
            return str(results)
        except Exception as e:
            return f"Search failed: {e}"

search_tool = SearchTool()
scrape_tool = ScrapeWebsiteTool()

# --- 3. Audio Engine ---
class AudioEngine:
    def __init__(self, output_dir="."):
        self.output_dir = output_dir

    def generate_clip(self, text: str, speaker: str, index: int) -> str:
        """Generates a single audio clip for a line of dialogue."""
        model = VOICE_MODELS.get(speaker, VOICE_MODELS["Host"]) # Default to Host
        output_file = os.path.join(self.output_dir, f"line_{index:03d}.wav")
        
        # Ensure output dir exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        command = f'echo "{text}" | {PIPER_BINARY} --model {model} --output_file {output_file}'
        subprocess.run(command, shell=True, check=True)
        return output_file

    def mix_audio(self, clips: List[str], final_output: str):
        """Concatenates clips and mixes with background music."""
        # 1. Concatenate dialogue
        concat_file = "concat_list.txt"
        with open(concat_file, "w") as f:
            for clip in clips:
                f.write(f"file '{clip}'\n")
        
        dialogue_wav = "dialogue_temp.wav"
        subprocess.run(f"ffmpeg -y -f concat -safe 0 -i {concat_file} -c copy {dialogue_wav}", shell=True, check=True)

        # 2. Mix with background music (ducking)
        # Lowers music volume to 10% when dialogue is present, keeps it at 20% otherwise
        if os.path.exists(BACKGROUND_MUSIC):
            cmd = (
                f"ffmpeg -y -i {dialogue_wav} -stream_loop -1 -i {BACKGROUND_MUSIC} "
                f"-filter_complex \"[1:a]volume=0.2[bg];[0:a]volume=1.5[fg];"
                f"[fg][bg]amix=inputs=2:duration=first:dropout_transition=2[a]\" "
                f"-map \"[a]\" {final_output}"
            )
        else:
            print("Background music not found, skipping mix.")
            cmd = f"cp {dialogue_wav} {final_output}"
            
        subprocess.run(cmd, shell=True, check=True)
        
        # Cleanup
        if os.path.exists(concat_file): os.remove(concat_file)
        if os.path.exists(dialogue_wav): os.remove(dialogue_wav)
        for clip in clips:
            if os.path.exists(clip): os.remove(clip)

# --- 5. Logic ---
class ScriptParser:
    @staticmethod
    def parse(script_content: str) -> List[Tuple[str, str]]:
        """
        Parses the script to extract (Speaker, Text) tuples.
        Handles formatting like "Speaker: Text" or "Speaker says: Text".
        """
        lines = script_content.split('\n')
        parsed_lines = []
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Remove markdown bolding/headers
            clean_line = line.replace('*', '').replace('#', '').strip()
            
            # Check for "Name: Text" pattern
            # Matches: "Host: ", "Guest: ", "John says: ", etc.
            match = re.match(r"^([A-Za-z0-9 ]+)\s*(?:says|:|-)\s*(.*)", clean_line, re.IGNORECASE)
            
            if match:
                speaker = match.group(1).strip()
                text = match.group(2).strip()
                
                # Filter out obvious metadata lines that might get caught
                if len(speaker) > 20 or "scene" in speaker.lower() or speaker.upper() in ["NAME", "TEXT", "SPEAKER"]:
                    continue

                # Final cleanup of text
                text = text.strip('" ')
                if not text: continue
                
                parsed_lines.append((speaker, text))
            
        return parsed_lines

def run_podcast(topic: str, output_file: str = "podcast.wav", length: str = "short", 
                allow_human_input: bool = True, host_name: str = "Host", guest_name: str = "Guest",
                llm_model_name: str = "qwen2.5:0.5b"):
    
    print(f"Starting generation with model: {llm_model_name}")
    
    # Dynamic LLM for CrewAI
    # We need to recreate agents to switch models if we use CrewAI
    from crewai import LLM as CrewLLM
    dynamic_llm = CrewLLM(model=f"ollama/{llm_model_name}", base_url="http://localhost:11434")

    # Re-define agents with the specific model
    researcher = Agent(
        role='Podcast Researcher',
        goal='Find relevant and interesting news topics.',
        backstory='You are a meticulous researcher who loves finding deep cuts and interesting stories.',
        tools=[search_tool, scrape_tool],
        verbose=True,
        llm=dynamic_llm
    )
    
    # Define length prompt
    length_map = {
        "short": "approx 10 lines",
        "medium": "approx 30 lines",
        "long": "approx 60 lines"
    }
    length_desc = length_map.get(length, "approx 10 lines")

    # 1. Research
    research_task = Task(
        description=f"Find the latest news on {topic}. Summarize them into a list.",
        expected_output="A list of news summaries.",
        agent=researcher,
        human_input=allow_human_input 
    )

    research_crew = Crew(
        agents=[researcher],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True
    )
    
    print("Running Research...")
    try:
        research_result = research_crew.kickoff()
    except Exception as e:
        print(f"Research failed: {e}")
        research_result = "Could not find news. Using general knowledge."

    print(f"Research Result parsed: {str(research_result)[:100]}...")

    # 2. Write Script (Direct LLM Call)
    print(f"Writing Script (Direct Mode using {llm_model_name})...")
    
    prompt = (
        f"You are a scriptwriter. Write a script between {host_name} and {guest_name} about:\n"
        f"{str(research_result)}\n\n"
        "RULES:\n"
        "1. Write ONLY the spoken dialogue.\n"
        "2. Format: Name: Text\n"
        "3. DO NOT use 'NAME:' or 'TEXT:' headers. Just the name of the speaker.\n"
        "4. No intro/outro/scene headers.\n\n"
        "SCRIPT:"
    )

    try:
        # Direct call to Ollama 
        # Note: 'ollama run' takes the model name directly (e.g. 'qwen2.5:0.5b')
        cmd = ["ollama", "run", llm_model_name, prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        script_content = result.stdout
    except Exception as e:
        print(f"Direct generation failed: {e}")
        script_content = ""

    print(f"Raw Script Output:\n{script_content[:200]}...\n")
    
    # Validation and Audio generation remains same...
    
    # Validation
    if len(script_content) < 50 or ":" not in script_content:
        # ... (fallback logic)
        script_content = (
            f"{host_name}: Welcome listeners. We encountered an error generating the script.\n"
            f"{guest_name}: It seems our AI writer is having a bad day.\n"
            f"{host_name}: Please try strictly researching a simple topic like 'Weather'."
        )

    # Save script
    with open("script.txt", "w") as f:
        f.write(script_content)
    print("\nScript saved to script.txt")

    # 3. Audio Generation
    print("Generating audio...")
    engine = AudioEngine()
    clips = []
    
    parsed_lines = ScriptParser.parse(script_content)
    
    idx = 0
    for speaker, text in parsed_lines:
        print(f"Generating line {idx} ({speaker}): {text[:50]}...")
        
        # Map custom names to generic Voice Models with fuzzy matching
        s_norm = speaker.lower().strip()
        h_norm = host_name.lower().strip()
        g_norm = guest_name.lower().strip()
        
        # Check if speaker name contains or is contained by host/guest name 
        # (e.g. "Dany" matches "Dany Bhatti")
        if (s_norm in h_norm and len(s_norm) > 2) or (h_norm in s_norm):
            voice_role = "Host"
        elif (s_norm in g_norm and len(s_norm) > 2) or (g_norm in s_norm):
            voice_role = "Guest"
        else:
            # Fallback for unexpected names
            voice_role = "Host" if idx % 2 == 0 else "Guest"

        try:
            clip_path = engine.generate_clip(text, voice_role, idx)
            clips.append(clip_path)
            idx += 1
        except Exception as e:
            print(f"Failed to generate line {idx}: {e}")

    engine.mix_audio(clips, output_file)
    print(f"Audio generated: {output_file}")
    return output_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local Agentic Podcast System")
    parser.add_argument("--topic", help="Topic for the podcast")
    parser.add_argument("--output", default="podcast.wav", help="Output audio file")
    parser.add_argument("--length", default="short", choices=["short", "medium", "long"], help="Length of the podcast (short=10 lines, medium=30 lines, long=60 lines)")
    
    args = parser.parse_args()
    
    if args.topic:
        topic = args.topic
    else:
        print("Local Agentic Podcast System")
        topic = input("Enter a topic for the podcast: ")
        
    run_podcast(topic, args.output, args.length)
