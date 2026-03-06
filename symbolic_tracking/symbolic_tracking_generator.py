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
        """
        # Expanded operation set for higher complexity
        ops = [
            "SWAP_A_G",           # End-to-end swap
            "SWAP_C_D",           # Middle swap
            "SHIFT_RIGHT",        # Cyclic shift right
            "SHIFT_LEFT",         # Cyclic shift left
            "REVERSE_ALL",        # Full list reversal
            "INCREMENT_ALL",      # Add 1 to all values (modulo 10)
            "SET_D_TO_A_PLUS_B"   # Inter-variable arithmetic dependency
        ]

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
                        # A->B, B->C, ..., G->A
                        vals = [state["G"], state["A"], state["B"], state["C"], state["D"], state["E"], state["F"]]
                        state["A"], state["B"], state["C"], state["D"], state["E"], state["F"], state["G"] = vals
                    elif move == "SHIFT_LEFT":
                        # A->G, B->A, ..., G->F
                        vals = [state["B"], state["C"], state["D"], state["E"], state["F"], state["G"], state["A"]]
                        state["A"], state["B"], state["C"], state["D"], state["E"], state["F"], state["G"] = vals
                    elif move == "REVERSE_ALL":
                        # A<->G, B<->F, C<->E
                        state["A"], state["G"] = state["G"], state["A"]
                        state["B"], state["F"] = state["F"], state["B"]
                        state["C"], state["E"] = state["E"], state["C"]
                    elif move == "INCREMENT_ALL":
                        # Add 1 to everything, wrap at 10
                        for k in state:
                            state[k] = (state[k] + 1) % 10
                    elif move == "SET_D_TO_A_PLUS_B":
                        state["D"] = (state["A"] + state["B"]) % 10

                target_var = random.choice(["A", "B", "C", "D", "E", "F", "G"])
                moves_str = "\n".join([f"{i+1}. {m}" for i, m in enumerate(instructions)])
                
                # Complex prompt requesting state verification at every step
                prompt = (
                    "Initial State: A=1, B=2, C=3, D=4, E=5, F=6, G=7\n"
                    "Note: All arithmetic operations are performed modulo 10 (e.g., 9 + 1 = 0).\n"
                    "Apply the following operations in exact order. You MUST show the state of all 7 variables after EACH step to show your tracking.\n\n"
                    f"{moves_str}\n\n"
                    f"What is the final value of variable {target_var}? End your final response line with: 'FINAL VALUE: X'"
                )
                
                self.dataset.append({
                    "task_type": "symbolic_tracking_v2",
                    "depth": depth,
                    "prompt": prompt,
                    "ground_truth": f"FINAL VALUE: {state[target_var]}"
                })

    def export(self, filename="symbolic_benchmark_v2.json"):
        with open(filename, 'w') as f:
            json.dump(self.dataset, f, indent=4)
        print(f"Generated {len(self.dataset)} advanced symbolic prompts.")

if __name__ == "__main__":
    gen = SymbolicTrackingGenerator()
    gen.generate_symbolic_benchmark()
    gen.export()