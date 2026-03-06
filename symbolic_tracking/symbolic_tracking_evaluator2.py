import json
import time
import os
from google import genai
from google.genai import types

# ==========================================
# CONFIGURATION
# ==========================================
# Replace with your actual API Key
API_KEY = "AIzaSyBC3lfYxIZM0WMptwjGblF06JSmHWzsRjI"
client = genai.Client(api_key=API_KEY)
MODEL_ID = "gemini-2.5-flash"

# Free Tier Safety Delay: 45 seconds to avoid TPM limits.
# If you move to a paid key, you can reduce this to 1.0.
WAIT_TIME = 45.0 

def run_evaluation(input_file="symbolic_benchmark_v2.json", output_file="results_symbolic_v2.json"):
    """
    Evaluates the model on the symbolic tracking benchmark.
    Updated to handle high-token reasoning chains without truncation.
    """
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Please run the generator first.")
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
    
    print(f"\n[START] Evaluating {MODEL_ID} on Symbolic Tracking (V2)...")
    print(f"Output will be saved to: {output_file}")
    print("-" * 50)
    
    for i in range(len(results), len(dataset)):
        item = dataset[i]
        success = False
        retries = 0
        
        while not success and retries < 3:
            try:
                # INCREASED TOKEN LIMIT:
                # High-depth reasoning (N=40+) often exceeds 1024 tokens.
                # 4096 ensures the model can finish its work-showing steps.
                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=item["prompt"],
                    config=types.GenerateContentConfig(max_output_tokens=4096)
                )
                
                answer = response.text.strip()
                
                # Case-insensitive check for the ground truth string in the answer
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
                    print("  -> [QUOTA LIMIT] Waiting 300s (5 mins) for window reset...")
                    time.sleep(300)
                    retries += 1
                else:
                    print(f"  -> [API ERROR] {e}")
                    time.sleep(10)
                    retries += 1

        if not success:
            print(f"  -> [CRITICAL] Skipping prompt {i+1} after {retries} retries.")

    # Generate Final Research Summary
    print("\n" + "="*50)
    print("FINAL ACCURACY BY DEPTH")
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