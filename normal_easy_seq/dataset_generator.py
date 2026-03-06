import random
import json
import string

class ComplexityDatasetGenerator:
    def __init__(self):
        self.dataset = []

    def generate_sequential_arithmetic(self, min_depth=1, max_depth=30, samples_per_depth=10):
        for depth in range(min_depth, max_depth + 1):
            for _ in range(samples_per_depth):
                # Start with a random base number
                equation = str(random.randint(10, 50))
                current_val = int(equation)
                
                # Chain 'depth' number of operations
                for _ in range(depth):
                    op = random.choice(['+', '-'])
                    num = random.randint(1, 15)
                    equation += f" {op} {num}"
                    if op == '+':
                        current_val += num
                    else:
                        current_val -= num
                        
                self.dataset.append({
                    "task_type": "sequential_arithmetic",
                    "complexity_class": "O(N)",
                    "depth": depth,
                    "prompt": f"Calculate the exact result of this sequence: {equation}. Output only the final number.",
                    "ground_truth": str(current_val)
                })

    def generate_multiplication_ood(self, min_digits=1, max_digits=5, samples_per_depth=20):
        for digits in range(min_digits, max_digits + 1):
            for _ in range(samples_per_depth):
                # Generate N-digit numbers
                lower_bound = 10**(digits - 1) if digits > 1 else 1
                upper_bound = (10**digits) - 1
                
                num1 = random.randint(lower_bound, upper_bound)
                num2 = random.randint(lower_bound, upper_bound)
                result = num1 * num2
                
                self.dataset.append({
                    "task_type": "multi_digit_multiplication",
                    "complexity_class": "O(N^2)",
                    "depth": digits, # Depth here represents the number of digits (N)
                    "prompt": f"Calculate the exact product: {num1} * {num2}. Output only the final number.",
                    "ground_truth": str(result)
                })

    def generate_string_reversal(self, min_length=3, max_length=40, samples_per_depth=10):
        for length in range(min_length, max_length + 1):
            for _ in range(samples_per_depth):
                # Generate random string of 'length' characters
                random_string = ''.join(random.choices(string.ascii_lowercase, k=length))
                reversed_string = random_string[::-1]
                
                self.dataset.append({
                    "task_type": "string_reversal",
                    "complexity_class": "O(N)",
                    "depth": length,
                    "prompt": f"Reverse the following string character by character: '{random_string}'. Output only the reversed string.",
                    "ground_truth": reversed_string
                })

    def generate_nested_functions(self, min_depth=1, max_depth=15, samples_per_depth=10):
        for depth in range(min_depth, max_depth + 1):
            for _ in range(samples_per_depth):
                # Define simple linear function f(x) = ax + b
                a = random.randint(2, 4)
                b = random.randint(1, 5)
                start_x = random.randint(1, 3)
                
                # Calculate ground truth
                current_x = start_x
                for _ in range(depth):
                    current_x = (a * current_x) + b
                
                # Format the f(f(...)) string
                func_string = "f(" * depth + str(start_x) + ")" * depth
                
                self.dataset.append({
                    "task_type": "nested_functions",
                    "complexity_class": "O(N)",
                    "depth": depth,
                    "prompt": f"Let f(x) = {a}x + {b}. Evaluate {func_string}. Output only the final number.",
                    "ground_truth": str(current_x)
                })

    def export_dataset(self, filename="complexity_benchmark.json"):
        with open(filename, 'w') as f:
            json.dump(self.dataset, f, indent=4)
        print(f"Successfully generated {len(self.dataset)} prompts.")
        print(f"Dataset saved to {filename}")

if __name__ == "__main__":
    print("Initializing Procedural Dataset Generator...")
    generator = ComplexityDatasetGenerator()
    
    generator.generate_sequential_arithmetic(min_depth=1, max_depth=30, samples_per_depth=10)
    generator.generate_multiplication_ood(min_digits=1, max_digits=5, samples_per_depth=20)
    generator.generate_string_reversal(min_length=3, max_length=40, samples_per_depth=10)
    generator.generate_nested_functions(min_depth=1, max_depth=15, samples_per_depth=10)
    
    generator.export_dataset("llm_complexity_benchmark.json")