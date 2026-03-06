# Complexity Ceiling in Large Language Models

This project studies the limits of reasoning ability in **Large Language Models (LLMs)** by evaluating their performance on structured multi-step reasoning tasks.

The central hypothesis is that **LLMs exhibit a complexity ceiling**: as the number of reasoning steps increases, models begin to fail systematically due to limitations in state tracking, compositional reasoning, or constraint propagation.

To investigate this, we design **synthetic reasoning domains** where the correct solution can be **automatically generated and automatically verified**.

---

# Motivation

LLMs often appear capable of complex reasoning when prompted with step-by-step instructions. However, it is unclear whether they truly perform **algorithmic reasoning** or simply rely on **pattern matching and shallow heuristics**.

This repository provides a framework to test reasoning limits by:

- Automatically generating reasoning tasks
- Querying LLMs for solutions
- Automatically verifying correctness
- Measuring performance as reasoning complexity increases

The goal is to **identify where and why reasoning failures occur**.

---

# Reasoning Domains

The benchmark currently includes multiple reasoning domains, each targeting a different structural form of reasoning.

---

## 1. Alien Grid (Spatial State Tracking)

Models must track the state of a grid after sequential transformations.

### Example

**Initial grid**

```

1 2 3
4 5 6
7 8 9

```

**Operations**

```

rotate_row_1_right
swap_column_1_3

```

The model must compute the **final grid state**.

### Failure Modes

- Losing track of intermediate spatial states  
- Applying transformations in the wrong order  

---

## 2. Symbolic Tracking (Variable State Updates)

Models must track variables that change over time.

### Example

```

A = 2
B = 3

Step1: C = A + B
Step2: A = C * 2
Step3: B = A - 1

```

### Question

```

What are the final values of A, B, and C?

```

### Failure Modes

- Forgetting earlier assignments  
- Confusing variable bindings  

---

## 3. Social Logic (Graph Reasoning)

Models must perform multi-hop reasoning over relationships.

### Example

```

Alice trusts Bob
Bob trusts Carol
Carol trusts Dave

```

### Question

```

Does Alice indirectly trust Dave?

```

### Failure Modes

- Multi-hop inference collapse  
- Hallucinating missing links  

---

## 4. Sequential Logic (Operation Chains)

Models must apply a sequence of symbolic operations.

### Example

```

Start value: 5

Operations
+3
*2
-4

```

### Question

```

What is the final value?

```

### Failure Modes

- Arithmetic step errors  
- Losing track of intermediate values  

---

# Evaluation Framework

Each domain follows the same evaluation pipeline.

---

## 1. Automatic Task Generation

Tasks are generated programmatically to control reasoning depth.

Example parameter

```

number_of_steps = 5

````

---

## 2. Model Query

The prompt is sent to the LLM.

Example models:

- GPT
- Gemini
- Claude

---

## 3. Automatic Verification

The system computes the **true answer programmatically** and compares it with the model's output.

Example output format

```json
{
  "model_answer": "...",
  "correct_answer": "...",
  "correct": true
}
````

---

## 4. Complexity Analysis

Performance is analyzed as a function of reasoning depth.

Example metric

```
Accuracy vs reasoning steps
```

This allows us to detect the **complexity ceiling**.

---

# Repository Structure

```
Complexity_Ceiling_LLM/

alien_grid/
    grid_generator.py
    grid_evaluator.py

symbolic_tracking/
    symbolic_generator.py
    symbolic_evaluator.py

social_logic/
    social_generator.py
    social_evaluator.py

normal_easy_seq/
    sequence_generator.py
    sequence_evaluator.py

multi_model_evaluator.py
results_social_logic.json
README.md
```

---

# Running Experiments

Example usage

```bash
python multi_model_evaluator.py
```

This will:

1. Generate reasoning tasks
2. Query the selected LLM
3. Evaluate correctness
4. Save results to JSON

---

# Example Output

Example result

```json
{
  "task_id": 12,
  "model": "gemini-2.5-flash",
  "steps": 5,
  "correct": false
}
```

Aggregated results can be used to produce plots such as:

```
Reasoning Steps vs Accuracy
```

---

# Research Goal

The long-term goal of this project is to build a **systematic benchmark for reasoning limits in LLMs**, covering different computational structures:

* **Arrays** (Grid tracking)
* **Variables** (Symbolic tracking)
* **Graphs** (Social reasoning)
* **Sequential transformations**

By evaluating performance across these domains, we aim to better understand **when LLM reasoning breaks down and why**.


# Future Work

Planned extensions include:

* Hierarchical reasoning (tree structures)
* Temporal causality tracking
* Constraint propagation tasks
* Recursive reasoning tasks


# Author

**Shubh Chapra**
