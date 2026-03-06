import json
import time
import os

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Please install the Google GenAI SDK: pip install google-genai")
    exit()

# ==========================================
# CONFIGURATION
# ==========================================
API_KEY = "AIzaSyBC3lfYxIZM0WMptwjGblF06JSmHWzsRjI"
client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-2.5-flash"

# Free Tier Safety Delay: 60 seconds to avoid TPM limits with heavy reasoning
WAIT_TIME = 60.0 

def run_evaluation(input_file="social_logic_benchmark.json", output_file="results_social_logic.json"):
    """
    Evaluates the model on the Social Logic (Relational) benchmark.
    """
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Please run the social_logic_generator.py first.")
        return

    results = []
    # Resume logic to pick up where the script left off
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r') as f:
                results = json.load(f)
            print(f"Resuming from prompt {len(results) + 1}...")
        except Exception:
            results = []

    dataset = json.load(open(input_file, 'r'))
    
    print(f"\n[START] Evaluating {MODEL_ID} on Relational Logic (Social Graph)...")
    print(f"Output will be saved to: {output_file}")
    print("-" * 50)
    
    for i in range(len(results), len(dataset)):
        item = dataset[i]
        success = False
        retries = 0
        
        while not success and retries < 3:
            try:
                # Passing the system_instruction securely in the config 
                # This ensures the model knows the Transitive/Recursive rules
                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=item["prompt"],
                    config=types.GenerateContentConfig(
                        system_instruction=item.get("system_instruction", ""),
                        max_output_tokens=4096 
                    )
                )
                
                answer = response.text.strip()
                
                # Check for the ground truth text (e.g., "RELATIONSHIP: FRIENDS")
                is_correct = item["ground_truth"].lower() in answer.lower()
                
                results.append({
                    "depth": item["depth"],
                    "ground_truth": item["ground_truth"],
                    "model_output": answer,
                    "is_correct": is_correct
                })
                
                # Save progress incrementally
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=4)
                
                status = "Correct" if is_correct else "Incorrect"
                print(f"[{i+1}/{len(dataset)}] Depth {item['depth']:02d} | Result: {status}")
                
                success = True
                time.sleep(WAIT_TIME)
                
            except Exception as e:
                error_str = str(e).lower()
                if "429" in error_str or "quota" in error_str or "limit" in error_str:
                    # Extended wait for quota resets
                    print("  -> [QUOTA LIMIT] Waiting 120s (2 mins) for window reset...")
                    time.sleep(120)
                    retries += 1
                else:
                    print(f"  -> [API ERROR] {e}")
                    time.sleep(10)
                    retries += 1

        if not success:
            print(f"  -> [CRITICAL] Skipping prompt {i+1} after {retries} retries.")

    # Generate Final Research Summary
    print("\n" + "="*50)
    print("FINAL ACCURACY BY DEPTH (SOCIAL LOGIC)")
    print("="*50)
    stats = {}
    for r in results:
        d = r["depth"]
        stats.setdefault(d, {"total": 0, "correct": 0})
        stats[d]["total"] += 1
        if r["is_correct"]:
            stats[d]["correct"] += 1
            
    for d in sorted(stats.keys()):
        total = stats[d]["total"]
        correct = stats[d]["correct"]
        acc = (correct / total) * 100
        print(f"Depth {d}:\t{acc:.1f}% ({correct}/{total})")
    print("="*50)

if __name__ == "__main__":
    run_evaluation()