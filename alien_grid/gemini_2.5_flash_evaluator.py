import json
import time
import os
import sys

if sys.platform == "win32":
    import subprocess
    subprocess.call('chcp 65001', shell=True)
try:
    from google import genai
except ImportError:
    exit()

API_KEY = "AIzaSyBC3lfYxIZM0WMptwjGblF06JSmHWzsRjI"
client = genai.Client(api_key=API_KEY)

MODEL_ID = "gemini-2.0-flash-lite"
BASE_WAIT_TIME = 45.0 

def run_evaluation(input_file="limit_finder_benchmark1.json", output_file="results_gemini_2.5_flash1.json"):
    print(f"Loading dataset: {os.path.abspath(input_file)}")
    
    try:
        with open(input_file, 'r') as f:
            dataset = json.load(f)
    except FileNotFoundError:
        print(f"\nERROR: Could not find {input_file}.")
        return
    results = []
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r') as f:
                results = json.load(f)
            print(f"Resuming from prompt {len(results) + 1}...")
        except:
            results = []

    print(f"\n[START] Starting evaluation of {len(dataset)} prompts on {MODEL_ID}...")
    print(f"Pacing: {BASE_WAIT_TIME}s delay (Free Tier Safety Mode).")
    print("-" * 50)
    
    current_wait = BASE_WAIT_TIME

    for i in range(len(results), len(dataset)):
        item = dataset[i]
        prompt = item["prompt"]
        ground_truth = str(item["ground_truth"])
        
        success = False
        retries = 0
        max_retries = 5 
        
        while not success and retries < max_retries:
            try:
                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=prompt
                )
                model_answer = response.text.strip()
                is_correct = ground_truth.lower() in model_answer.lower()
                item_result = {
                    "depth": item["depth"],
                    "ground_truth": ground_truth,
                    "model_output": model_answer,
                    "is_correct": is_correct
                }
                results.append(item_result)
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=4)
                
                print(f"[{i+1}/{len(dataset)}] Depth: {item['depth']:02d} | Correct: {is_correct}")
                success = True
                if current_wait > BASE_WAIT_TIME:
                    current_wait = max(BASE_WAIT_TIME, current_wait - 5.0)
                
                time.sleep(current_wait) 
                
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower() or "limit" in error_msg.lower():
                    retries += 1
                    current_wait += 10.0
                    backoff_time = 65 * retries 
                    print(f"  -> [FREE TIER LIMIT] Increasing delay to {current_wait}s. Pausing for {backoff_time}s...")
                    time.sleep(backoff_time)
                else:
                    print(f"  -> [API ERROR] Prompt {i+1}: {e}")
                    retries += 1
                    time.sleep(10)
                    
        if not success:
            print(f"\n[CRITICAL] Skipping prompt {i+1} after {max_retries} failed attempts.")

    print("-" * 50)
    print(f"[DONE] Final results saved to: {os.path.abspath(output_file)}")
    
    print("\n[STATS] RESEARCH SUMMARY TABLE")
    print("--------------------------------------------------")
    print("Depth (N)\tAccuracy (%)")
    depth_stats = {}
    for r in results:
        d = r["depth"]
        depth_stats.setdefault(d, {"t": 0, "c": 0})
        depth_stats[d]["t"] += 1
        if r["is_correct"]: depth_stats[d]["c"] += 1
            
    for d in sorted(depth_stats.keys()):
        total = depth_stats[d]["t"]
        if total > 0:
            acc = (depth_stats[d]["c"] / total) * 100
            print(f"Depth {d}:\t{acc:.1f}%")

if __name__ == "__main__":
    run_evaluation()