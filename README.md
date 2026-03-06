Mapping the Complexity Ceiling in LLMs 🧠📉

Algorithmic Trace Verification of State-Drift in Large Language Models

Overview

Current Large Language Models (LLMs) demonstrate exceptional surface-level intelligence and pattern matching. However, when forced to execute strict, multi-step sequential tasks (Depth $N$), errors inevitably accumulate. This research investigates the "Complexity Ceiling" of autoregressive models—the exact point at which an LLM's internal state-tracking collapses.

Instead of merely evaluating the final answer, this repository introduces Algorithmic Trace Verification. By forcing the model to output intermediate states, we can algorithmically pinpoint the exact step where logic degrades across different cognitive domains.

Repository Structure

Based on our multi-domain benchmark methodology, the repository is organized into distinct reasoning challenges:

Complexity_Ceiling_LLM/
├── alien_grid/              # Spatial state-tracking (2D grid coordinate transformations)
├── normal_easy_seq/         # Baseline sequential tasks (O(N) arithmetic & string logic)
├── social_logic/            # Relational tracking (Recursive transitive graph logic)
├── symbolic_tracking/       # Pointer-chasing (Abstract variables & modulo arithmetic)
├── multi_model_evaluator.py # Unified evaluator for Gemini, OpenAI, and OpenRouter models
├── results_social_logic.json# Example output data containing algorithmic trace results
└── README.md


The Reasoning Domains

This benchmark stress-tests models across fundamentally orthogonal data structures:

Spatial Tracking (alien_grid): Tests 2D spatial orientation. The model tracks a 3x3 grid through $N$ rotations and swaps.

Symbolic Tracking (symbolic_tracking): Tests pure working memory. The model tracks 7 distinct variables through $N$ cyclic shifts and arithmetic dependencies.

Relational Logic (social_logic): Tests graph-based memory. The model tracks diplomatic alliances based on transitive rules (e.g., "the rival of my rival is my friend").

Baseline Sequential (normal_easy_seq): Evaluates standard linear composition limits (e.g., sequential arithmetic).

Evaluation Methodology

This project does not just grade final answers. It evaluates the journey:

Dataset Generators: Python scripts generate $N$-depth prompts and calculate the exact mathematical state at every intermediate step (the Expected Trace).

LLM Inference: The model is prompted to output its state in a strict, ultra-concise format (e.g., Step 14: [A, B, C...]).

Trace Verification: Evaluator scripts use Regex to extract the model's arrays, comparing them to the Expected Trace to find the Exact Point of Failure (e.g., Accuracy: 0% | Avg Failure Point: Step 16).

Getting Started

Prerequisites

Install the required SDKs for model evaluation:

pip install google-genai openai


Running an Evaluation

Clone the repository:

git clone [https://github.com/Shubh-Chapra/Complexity_Ceiling_LLM.git](https://github.com/Shubh-Chapra/Complexity_Ceiling_LLM.git)
cd Complexity_Ceiling_LLM


Navigate into a specific domain folder to generate a benchmark dataset (e.g., cd symbolic_tracking and run the generator).

Insert your API keys (Google, OpenAI, or OpenRouter) into the evaluator script.

Run the multi-model evaluator:

python multi_model_evaluator.py


Author

Shubh Chapra
Research Artifact for SOP & Complexity Analysis
