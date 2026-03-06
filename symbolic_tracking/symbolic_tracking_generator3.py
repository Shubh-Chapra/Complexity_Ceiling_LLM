import random
import json

class SymbolicTrackingGenerator:
    def __init__(self):
        self.dataset = []

    def generate_symbolic_benchmark(self, start_depth=5, end_depth=50, step=5, samples_per_depth=2):
        """
        Generates complex symbolic tracking prompts (Pointer Chasing).
        Variables: A, B, C, D, E, F, G.
        Optimized for Token Efficiency: Enforces a strict, concise output format to avoid TPM quota hits.
        """
        ops = [
            "SWAP_A_G",           
            "SWAP_C_D",           
            "SHIFT_RIGHT",        
            "SHIFT_LEFT",         
            "REVERSE_ALL",        
            "INCREMENT_ALL",      
            "SET_D_TO_A_PLUS_B"   
        ]

        operations_guide = (
            "OPERATIONS GUIDE:\n"
            "- SWAP_X_Y: Exchange values of X and Y.\n"
            "- SHIFT_RIGHT: A->B, B->C, C->D, D->E, E->F, F->G, G->A.\n"
            "- SHIFT_LEFT: A->G, G->F, F->E, E->D, D->C, C->B, B->A.\n"
            "- REVERSE_ALL: Reverse order (A<->G, B<->F, C<->E).\n"
            "- INCREMENT_ALL: Add 1 to all values (modulo 10).\n"
            "- SET_D_TO_A_PLUS_B: D = (A + B) mod 10.\n"
        )

        for depth in range(start_depth, end_depth + 1, step):
            for _ in range(samples_per_depth):
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
                    "TASK: Symbolic State Tracking\n"
                    "Initial State: [1, 2, 3, 4, 5, 6, 7]\n"
                    "Rules: Modulo 10 arithmetic.\n\n"
                    f"{operations_guide}\n"
                    "INSTRUCTIONS:\n"
                    "1. Apply operations in exact order.\n"
                    "2. CONCISE OUTPUT ONLY: For each step, only provide the step number and the current state as a list: 'Step X: [A, B, C, D, E, F, G]'.\n"
                    "3. DO NOT explain the logic. DO NOT show arithmetic work. ONLY show the list.\n\n"
                    f"{moves_str}\n\n"
                    f"Final Value of {target_var}? End with: 'FINAL VALUE: X'"
                )
                
                self.dataset.append({
                    "task_type": "symbolic_tracking_v2_concise",
                    "depth": depth,
                    "prompt": prompt,
                    "ground_truth": f"FINAL VALUE: {state[target_var]}"
                })

    def export(self, filename="symbolic_benchmark_v3.json"):
        with open(filename, 'w') as f:
            json.dump(self.dataset, f, indent=4)
        print(f"Generated {len(self.dataset)} concise symbolic prompts.")

if __name__ == "__main__":
    gen = SymbolicTrackingGenerator()
    gen.generate_symbolic_benchmark()
    gen.export()