import random
import json

class SymbolicTrackingGenerator:
    def __init__(self):
        self.dataset = []

    def generate_symbolic_benchmark(self, start_depth=5, end_depth=50, step=5, samples_per_depth=2):
        """
        Generates complex symbolic tracking prompts (Pointer Chasing).
        Variables: A, B, C, D, E, F, G.
        Operations: SWAP, SHIFT (L/R), REVERSE, INCREMENT, ARITHMETIC.
        Includes an Operations Guide and a Compact Output Format to prevent truncation.
        """
        ops = [
            "SWAP_A_G",           # End-to-end swap
            "SWAP_C_D",           # Middle swap
            "SHIFT_RIGHT",        # Cyclic shift right
            "SHIFT_LEFT",         # Cyclic shift left
            "REVERSE_ALL",        # Full list reversal
            "INCREMENT_ALL",      # Add 1 to all values (modulo 10)
            "SET_D_TO_A_PLUS_B"   # Inter-variable arithmetic dependency
        ]

        # The Legend provided to the model to ensure it understands the logic
        operations_guide = (
            "OPERATIONS GUIDE:\n"
            "- SWAP_X_Y: Exchange the current values of variable X and variable Y.\n"
            "- SHIFT_RIGHT: A cyclic shift where A's value moves to B, B to C, C to D, D to E, E to F, F to G, and G moves to A.\n"
            "- SHIFT_LEFT: A cyclic shift where A's value moves to G, G to F, F to E, E to D, D to C, C to B, and B moves to A.\n"
            "- REVERSE_ALL: Reverse the entire sequence (A exchanges with G, B with F, and C with E; D remains the same).\n"
            "- INCREMENT_ALL: Add 1 to the current value of every variable (modulo 10).\n"
            "- SET_D_TO_A_PLUS_B: Update variable D to be the sum of the current values of A and B (modulo 10).\n"
        )

        for depth in range(start_depth, end_depth + 1, step):
            for _ in range(samples_per_depth):
                # Initial State: 7 variables with unique values
                state = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7}
                instructions = []
                
                for _ in range(depth):
                    move = random.choice(ops)
                    instructions.append(move)
                    
                    if move == "SWAP_A_G":
                        state["A"], state["G"] = state["G"], state["A"]
                    elif move == "SWAP_C_D":
                        state["C"], state["D"] = state["D"], state["C"]
                    elif move == "SHIFT_RIGHT":
                        vals = [state["G"], state["A"], state["B"], state["C"], state["D"], state["E"], state["F"]]
                        state["A"], state["B"], state["C"], state["D"], state["E"], state["F"], state["G"] = vals
                    elif move == "SHIFT_LEFT":
                        vals = [state["B"], state["C"], state["D"], state["E"], state["F"], state["G"], state["A"]]
                        state["A"], state["B"], state["C"], state["D"], state["E"], state["F"], state["G"] = vals
                    elif move == "REVERSE_ALL":
                        state["A"], state["G"] = state["G"], state["A"]
                        state["B"], state["F"] = state["F"], state["B"]
                        state["C"], state["E"] = state["E"], state["C"]
                    elif move == "INCREMENT_ALL":
                        for k in state:
                            state[k] = (state[k] + 1) % 10
                    elif move == "SET_D_TO_A_PLUS_B":
                        state["D"] = (state["A"] + state["B"]) % 10

                target_var = random.choice(["A", "B", "C", "D", "E", "F", "G"])
                moves_str = "\n".join([f"{i+1}. {m}" for i, m in enumerate(instructions)])
                
                prompt = (
                    "TASK: Symbolic State Tracking (High Complexity)\n"
                    "Initial State: A=1, B=2, C=3, D=4, E=5, F=6, G=7\n"
                    "Constraint: All arithmetic is modulo 10 (e.g., 9 + 1 = 0).\n\n"
                    f"{operations_guide}\n"
                    "INSTRUCTIONS:\n"
                    "1. Apply the operations below in the exact order given.\n"
                    "2. To save space, represent the state after EACH step as a list [A, B, C, D, E, F, G].\n"
                    "3. Format: 'Step X: [valA, valB, valC, valD, valE, valF, valG]'.\n\n"
                    f"{moves_str}\n\n"
                    f"What is the final value of variable {target_var}? End your final response line with: 'FINAL VALUE: X'"
                )
                
                self.dataset.append({
                    "task_type": "symbolic_tracking_v2_with_legend",
                    "depth": depth,
                    "prompt": prompt,
                    "ground_truth": f"FINAL VALUE: {state[target_var]}"
                })

    def export(self, filename="symbolic_benchmark_v2.json"):
        with open(filename, 'w') as f:
            json.dump(self.dataset, f, indent=4)
        print(f"Generated {len(self.dataset)} advanced symbolic prompts with Compact Legends.")

if __name__ == "__main__":
    gen = SymbolicTrackingGenerator()
    gen.generate_symbolic_benchmark()
    gen.export()