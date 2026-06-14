---
name: prompt-optimizer
description: "Automated prompt optimization using gradient-free search, A/B testing, and LLM-as-judge evaluation."
version: 0.1.0
category: technology
---

# Prompt Optimizer

## Overview

Automated prompt optimization using gradient-free search, A/B testing, and LLM-as-judge evaluation to systematically improve prompt quality for LLM applications.

## When To Use

- When prompt performance is inconsistent or sub-optimal
- When you need systematic prompt improvement with measurable results
- When building production LLM applications requiring reliable prompt engineering
- When migrating prompts between models or adapting to new model versions

## Core Techniques

### 1. Gradient-Free Search (MIPRO-style)
- Monte Carlo prompt mutations with acceptance criteria
- Pareto-frontier tracking for quality vs. token cost tradeoffs
- Batch evaluation with statistical significance testing

### 2. A/B Testing Framework
- Controlled prompt variant comparison
- Traffic splitting with consistent assignment
- Minimum detectable effect calculation

### 3. LLM-as-Judge Evaluation
- Structured rubric-based scoring
- Chain-of-thought reasoning for judge consistency
- Calibration against human preferences

## Workflow

1. **Define Objective**: Specify task, success criteria, and constraints (latency, cost, format)
2. **Generate Variants**: Apply mutation operators (rephrase, restructure, add examples, adjust tone)
3. **Evaluate**: Run variants against test set with LLM judge + automated metrics
4. **Select**: Pareto-optimal variants advance; dominated ones discarded
5. **Iterate**: Repeat with top performers until convergence or budget exhausted
6. **Validate**: Holdout test set confirms generalization

## Example Usage

```python
from prompt_optimizer import PromptOptimizer, LLMJudge

optimizer = PromptOptimizer(
    task="summarize technical documentation",
    judge=LLMJudge(rubric="accuracy, completeness, clarity, conciseness"),
    budget=100  # evaluation calls
)

best_prompt = optimizer.optimize(
    initial_prompt="Summarize the following text in 3 sentences.",
    test_cases=[...]
)
```

## Mutation Operators

| Operator | Description | Use Case |
|----------|-------------|----------|
| `rephrase` | Semantic-preserving rewrite | Tone, clarity |
| `add_examples` | Insert few-shot examples | Complex reasoning |
| `restructure` | Change prompt sections order | Attention allocation |
| `constraint_tighten` | Add format/length constraints | Output control |
| `persona_adopt` | Add role/persona framing | Domain expertise |

## Evaluation Metrics

- **Task Score**: LLM-judge rubric (0-100)
- **Token Efficiency**: Output tokens / input tokens
- **Latency P95**: End-to-end response time
- **Failure Rate**: Parse errors, refusals, format violations
- **Consistency**: Variance across repeated runs

## Reference Notes

- Auto-generated on 2026-06-06
- Extend with concrete mutation implementations, judge prompt templates, and CI/CD integration patterns.
- See also: `agent-contract-validator`, `llm-router-optimizer`