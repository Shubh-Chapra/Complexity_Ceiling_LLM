import json
import time
import os
try:
    from google import genai
except ImportError:
    exit()
API_KEY = "AIzaSyC3wnhIBzYqT_KApNUX3wE0ZCkAT_56nqo"
client = genai.Client(api_key=API_KEY)
MODEL_ID = 'gemini-2.5-flash'

def run_evaluation(input_file="llm_complexity_benchmark.json", output_file="llm_evaluation_results.json"):
    print(f"Looking for dataset at: {os.path.abspath(input_file)}")
    
    try:
        with open(input_file, 'r') as f:
            dataset = json.load(f)
    except FileNotFoundError:
        print(f"\nERROR: Could not find {input_file}.")
        print("Make sure this script is in the SAME FOLDER as your dataset JSON file!")
        return

    results = []
    print(f"\nStarting evaluation of {len(dataset)} prompts...")
    print("-" * 50)
    
    for i, item in enumerate(dataset):
        prompt = item["prompt"]
        ground_truth = str(item["ground_truth"])
        
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=prompt
            )
            model_answer = response.text.strip()
            is_correct = ground_truth.lower() in model_answer.lower()
            item_result = {
                "task_type": item["task_type"],
                "complexity_class": item["complexity_class"],
                "depth": item["depth"],
                "prompt": prompt,
                "ground_truth": ground_truth,
                "model_output": model_answer,
                "is_correct": is_correct
            }
            results.append(item_result)
            print(f"[{i+1}/{len(dataset)}] Depth: {item['depth']} | Correct: {is_correct}")
            time.sleep(2) 
            
        except Exception as e:
            print(f"API Error on prompt {i+1}: {e}")
            print("Saving progress so far and stopping...")
            break
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)
        
    print("-" * 50)
    print(f"Evaluation complete! Saved all results to: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    run_evaluation()