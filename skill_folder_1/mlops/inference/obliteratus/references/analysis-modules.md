# Analysis Modules

OBLITERATUS includes 28 analysis modules for mechanistic interpretability.
See `skill_view(name="obliteratus", file_path="references/analysis-modules.md")` for the full reference.

### Quick analysis commands
```bash
# Run specific analysis modules
obliteratus run analysis-config.yaml --preset quick

# Key modules to run first:
# - alignment_imprint: Fingerprint DPO/RLHF/CAI/SFT alignment method
# - concept_geometry: Single direction vs polyhedral cone
# - logit_lens: Which layer decides to refuse
# - anti_ouroboros: Self-repair risk score
# - causal_tracing: Causally necessary components
```

### Steering Vectors (Reversible Alternative)
Instead of permanent weight modification, use inference-time steering:
```python
# Python API only — for user's own projects
from obliteratus.analysis.steering_vectors import SteeringVectorFactory, SteeringHookManager
```
