import json
import time
import os

GOOGLE_API_KEY = "PASTE_GOOGLE_API_KEY_HERE"
OPENAI_API_KEY = "PASTE_OPENAI_API_KEY_HERE"

google_client = genai.Client(api_key=GOOGLE_API_KEY)
openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)

MODEL_TO_TEST = "gemini-3.1-pro"

if "flash" in MODEL_TO_TEST:
    WAIT_TIME = 12.5 
elif "gemini" in MODEL_TO_TEST:
    WAIT_TIME = 32.0 
else:
    WAIT_TIME = 2.0 

def evaluate_prompt(prompt, model_name):
    if "gemini" in model_name:
        response = google_client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text.strip()
    else:
        response = openai_client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()

def run_evaluation(input_file="limit_finder_benchmark.json"):
    output_file = f"results_{MODEL_TO_TEST}.json"
    print(f"Loading dataset: {os.path.abspath(input_file)}")
    
    try:
        with open(input_file, 'r') as f:
            dataset = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Could not find {input_file}. Did you run the dataset generator?")
        return

    results = []
    print(f"\n🚀 Starting evaluation of {len(dataset)} prompts on {MODEL_TO_TEST}...")
    print(f"Wait time between prompts: {WAIT_TIME} seconds.")
    print("-" * 50)
    
    for i, item in enumerate(dataset):
        prompt = item["prompt"]
        ground_truth = str(item["ground_truth"])
        
        success = False
        retries = 0
        
        while not success and retries < 3:
            try:
                model_answer = evaluate_prompt(prompt, MODEL_TO_TEST)
                is_correct = ground_truth.lower() in model_answer.lower()
                item_result = {
                    "depth": item["depth"],
                    "ground_truth": ground_truth,
                    "model_output": model_answer,
                    "is_correct": is_correct
                }
                results.append(item_result)
                
                print(f"[{i+1}/{len(dataset)}] Depth: {item['depth']:02d} | Correct: {is_correct}")
                success = True
                time.sleep(WAIT_TIME) 
                
            except Exception as e:
                error_msg = str(e)
                if "429" in error_msg or "quota" in error_msg.lower():
                    print(f"  -> Rate Limit Hit! Pausing for 60 seconds...")
                    time.sleep(60)
                    retries += 1
                else:
                    print(f"  -> API Error on prompt {i+1}: {e}")
                    retries += 1
                    time.sleep(5)
        if not success:
            print(f"  -> Skipping prompt {i+1} after 3 failed attempts.")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
        
    print("-" * 50)
    print(f"✅ Evaluation complete! Saved to: {output_file}")
    print("\n📊 RESEARCH PAPER SUMMARY TABLE (Accuracy vs. Depth)")
    print("--------------------------------------------------")
    print("Depth (N)\tAccuracy (%)")
    
    # Group by depth
    depth_stats = {}
    for r in results:
        d = r["depth"]
        if d not in depth_stats:
            depth_stats[d] = {"total": 0, "correct": 0}
        depth_stats[d]["total"] += 1
        if r["is_correct"]:
            depth_stats[d]["correct"] += 1
            
    # Print sorted table
    for d in sorted(depth_stats.keys()):
        total = depth_stats[d]["total"]
        correct = depth_stats[d]["correct"]
        accuracy = (correct / total) * 100
        print(f"Depth {d}:\t{accuracy:.1f}%")

if __name__ == "__main__":
    run_evaluation()