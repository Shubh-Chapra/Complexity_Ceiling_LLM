import random
import json

class SocialLogicGenerator:
    def __init__(self):
        self.dataset = []

    def get_relation(self, graph, start, target):
        """
        BFS Graph Solver to determine the current relationship between two nodes.
        Returns: 1 for FRIEND, -1 for RIVAL, 0 for NEUTRAL.
        Logic: Multiplicative weights (Rival * Rival = Friend -> -1 * -1 = 1)
        """
        queue = [(start, 1)]
        visited = {start}
        
        while queue:
            curr, weight = queue.pop(0)
            if curr == target:
                return weight
                
            for neighbor, edge_weight in graph[curr].items():
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, weight * edge_weight))
                    
        return 0 # No path found, so they are NEUTRAL

    def generate_benchmark(self, start_depth=5, end_depth=50, step=5, samples_per_depth=2):
        """
        Generates Relational Logic prompts (Social Graph).
        People: Alice, Bob, Charlie, David, Eve, Frank.
        Logic: Transitive friendship and enmity.
        """
        people = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"]
        
        system_instruction = (
            "You are a logic engine tracking social relationships. People: Alice, Bob, Charlie, David, Eve, Frank.\n"
            "RULES:\n"
            "1. Friendship is transitive: If X is friends with Y, and Y is friends with Z, X is friends with Z.\n"
            "2. Enmity is non-transitive but recursive: The rival of my rival is my friend.\n"
            "3. The rival of my friend is my rival.\n"
            "4. All relationships are symmetric (If A is a friend of B, B is a friend of A).\n"
            "OUTPUT: For each event, list ONLY the new alliances formed. End with the final relationship status requested."
        )

        for depth in range(start_depth, end_depth + 1, step):
            for _ in range(samples_per_depth):
                # Initialize an empty adjacency list for the social graph
                graph = {p: {} for p in people}
                events = []
                
                for i in range(depth):
                    p1, p2 = random.sample(people, 2)
                    
                    # Check if they already have a derived relationship
                    current_rel = self.get_relation(graph, p1, p2)
                    
                    if current_rel != 0:
                        # Enforce logical consistency: don't contradict existing relations
                        new_rel = current_rel
                    else:
                        # No existing relation, safe to assign a random one
                        new_rel = random.choice([1, -1])
                        # Add undirected edge to the graph
                        graph[p1][p2] = new_rel
                        graph[p2][p1] = new_rel
                        
                    rel_str = "become FRIENDS" if new_rel == 1 else "become RIVALS"
                    events.append(f"{i+1}. {p1} and {p2} {rel_str}.")

                # Ensure we ask a question about a pair that actually has a relationship
                connected_pairs = []
                for a in people:
                    for b in people:
                        if a < b and self.get_relation(graph, a, b) != 0:
                            connected_pairs.append((a, b))
                            
                if not connected_pairs:
                    # Fallback for extreme edge cases
                    q_p1, q_p2 = random.sample(people, 2)
                    ans_str = "NEUTRAL"
                else:
                    q_p1, q_p2 = random.choice(connected_pairs)
                    ans = self.get_relation(graph, q_p1, q_p2)
                    ans_str = "FRIENDS" if ans == 1 else "RIVALS"
                
                prompt = (
                    f"Initial State: All 6 people are neutral to each other.\n\n"
                    f"Events:\n"
                    f"{chr(10).join(events)}\n\n"
                    f"Question: Based on the rules, are {q_p1} and {q_p2} FRIENDS, RIVALS, or NEUTRAL? "
                    f"Show the chain of inference. End with: 'RELATIONSHIP: [STATUS]'"
                )

                self.dataset.append({
                    "task_type": "social_logic_v1",
                    "depth": depth,
                    "system_instruction": system_instruction,
                    "prompt": prompt,
                    "ground_truth": f"RELATIONSHIP: {ans_str}"
                })

    def export(self, filename="social_logic_benchmark.json"):
        with open(filename, 'w') as f:
            json.dump(self.dataset, f, indent=4)
        print(f"Generated {len(self.dataset)} Relational Logic prompts with auto-solved ground truth.")

if __name__ == "__main__":
    gen = SocialLogicGenerator()
    gen.generate_benchmark()
    gen.export()