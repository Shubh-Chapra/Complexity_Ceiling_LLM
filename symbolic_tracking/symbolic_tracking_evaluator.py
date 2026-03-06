import json
import time
import os
from google import genai
from google.genai import types

# ==========================================
# CONFIGURATION
# ==========================================
API_KEY = "AIzaSyBC3lfYxIZM0WMptwjGblF06JSmHWzsRjI"
client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-2.5-flash"

# Free Tier Safety Delay: 45 seconds to avoid TPM limits
WAIT_TIME = 45.0 

def run_evaluation(input_file="symbolic_benchmark_v2.json", output_file="results_symbolic.json"):
    if not os.path.exists(input_file):
        print("Dataset not found!")
        return

    results = []
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            results = json.load(f)
        print(f"Resuming from prompt {len(results) + 1}...")

    dataset = json.load(open(input_file, 'r'))
    
    print(f"\n[START] Evaluating {MODEL_ID} on Symbolic Tracking...")
    
    for i in range(len(results), len(dataset)):
        item = dataset[i]
        success = False
        retries = 0
        
        while not success and retries < 3:
            try:
                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=item["prompt"],
                    config=types.GenerateContentConfig(max_output_tokens=1024)
                )
                answer = response.text.strip()
                is_correct = item["ground_truth"].lower() in answer.lower()
                
                results.append({
                    "depth": item["depth"],
                    "ground_truth": item["ground_truth"],
                    "model_output": answer,
                    "is_correct": is_correct
                })
                
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=4)
                
                print(f"[{i+1}/{len(dataset)}] Depth {item['depth']:02d} | Correct: {is_correct}")
                success = True
                time.sleep(WAIT_TIME)
                
            except Exception as e:
                if "429" in str(e) or "quota" in str(e).lower():
                    print("  -> [QUOTA] Waiting 300s (5 mins) for reset...")
                    time.sleep(300)
                    retries += 1
                else:
                    print(f"  -> [ERROR] {e}")
                    time.sleep(10)
                    retries += 1

    # Print Summary Table
    print("\n[STATS] ACCURACY BY DEPTH")
    stats = {}
    for r in results:
        d = r["depth"]; stats.setdefault(d, [0,0])
        stats[d][0] += 1; stats[d][1] += 1 if r["is_correct"] else 0
    for d in sorted(stats.keys()):
        print(f"Depth {d}: {(stats[d][1]/stats[d][0])*100:.1f}%")

if __name__ == "__main__":
    run_evaluation()