import random
import json

class LimitFinderGenerator:
    def __init__(self):
        self.dataset = []

    def generate_scaled_alien_grid(self, start_depth=5, end_depth=50, step=5, samples_per_depth=5):
        moves_list = [
            "SWAP_CORNERS", # Swap 0 and 8
            "SHIFT_ROW_1_RIGHT", # 0,1,2 -> 2,0,1
            "REVERSE_GRID", # Reverse entire list
            "SHIFT_ROW_2_LEFT", # 3,4,5 -> 4,5,3
            "SWAP_EDGES", # Swap middle-left (3) and middle-right (5)
            "SHIFT_COL_2_DOWN" # 1,4,7 -> 7,1,4
        ]
        moves_list1 = [
            "SWAP_CORNERS", # Swap 0 and 8
            "SWAP_EDGES", # Swap middle-left (3) and middle-right (5)
        ]

        for depth in range(start_depth, end_depth + 1, step):
            for _ in range(samples_per_depth):
                grid = list(range(1, 10))
                instructions = []
                
                for _ in range(depth):
                    move = random.choice(moves_list)
                    instructions.append(move)
                    
                    if move == "SWAP_CORNERS":
                        grid[0], grid[8] = grid[8], grid[0]
                    elif move == "SHIFT_ROW_1_RIGHT":
                        grid[0], grid[1], grid[2] = grid[2], grid[0], grid[1]
                    elif move == "REVERSE_GRID":
                        grid.reverse()
                    elif move == "SHIFT_ROW_2_LEFT":
                        grid[3], grid[4], grid[5] = grid[4], grid[5], grid[3]
                    elif move == "SWAP_EDGES":
                        grid[3], grid[5] = grid[5], grid[3]
                    elif move == "SHIFT_COL_2_DOWN":
                        grid[1], grid[4], grid[7] = grid[7], grid[1], grid[4]
                        
                moves_str = "\n".join([f"{i+1}. {m}" for i, m in enumerate(instructions)])
                
                prompt = (
                    "Imagine a 3x3 grid numbered 1 to 9 sequentially from top-left to bottom-right. "
                    "Row 1 is [1,2,3]. Row 2 is [4,5,6]. Row 3 is [7,8,9].\n\n"
                    f"{moves_list1}\n"
                    "Apply the following operations in exact order. You must output the full 3x3 grid "
                    "after EVERY single step to show your work.\n\n"
                    f"{moves_str}\n\n"
                    "What is the final number in the exact center of the grid (Row 2, Column 2)? "
                    "End your response with: 'FINAL CENTER: X' where X is the single digit."
                )
                
                ground_truth = str(grid[4])
                
                self.dataset.append({
                    "task_type": "scaled_alien_grid",
                    "complexity_class": "O(N*M)",
                    "depth": depth,
                    "prompt": prompt,
                    "ground_truth": f"FINAL CENTER: {ground_truth}"
                })

    def export_dataset(self, filename="limit_finder_benchmark1.json"):
        with open(filename, 'w') as f:
            json.dump(self.dataset, f, indent=4)
        print(f"Generated {len(self.dataset)} prompts scaling from Depth 5 to 50.")
        print(f"Saved to {filename}")

if __name__ == "__main__":
    generator = LimitFinderGenerator()
    generator.generate_scaled_alien_grid()
    generator.export_dataset()