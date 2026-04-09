# Uncertainty Collapse in Post-Trained Language Models: Keep Calm or Carry On

**Author:** HiP (Ivan Phan)  
**ORCID:** [0009-0003-1095-5855](https://orcid.org/0009-0003-1095-5855)  
**Date:** April 2026  
**License:** CC BY 4.0  
**DOI:** [10.5281/zenodo.19482051](https://doi.org/10.5281/zenodo.19482051)

## Summary

Sycophancy, confident fabrication, and reward hacking are studied as separate alignment failures. This paper proposes they share a computational pattern: **uncertainty collapse**. When a post-trained language model encounters elevated uncertainty, it resolves it by descending the nearest low-entropy slope in a landscape shaped by post-training. The specific failure mode depends on the type of uncertainty encountered.

Two novel contributions:

1. **Orthogonal entropy divergence:** a measurable signature where token-level entropy collapses while semantic entropy remains high. The model becomes certain *how* to speak while remaining uncertain *what* it is saying.

2. **Functional empathy mechanism:** the model's capacity for tracking user emotional states recruits warmth-associated representations that, in the absence of a stable honesty attractor, slide toward sycophantic agreement. Each link has independent causal support within a single model family.

The paper presents 12 falsifiable predictions, engages three alternate hypotheses, and proposes an intervention taxonomy based on where each approach acts relative to the autoregressive cascade.

## Contents

- `uncertainty-collapse.md`: source manuscript (Markdown)
- `uncertainty-collapse.html`: HTML version (sans-serif, screen-optimised)
- `uncertainty-collapse.pdf`: PDF version (serif, archival)
- `uncertainty-collapse-fig1.jpg`: Figure 1, predicted temporal signature
- `uncertainty-collapse-fig2.jpg`: Figure 2, post-training landscape topology
- `convert.py`: build script (Markdown to HTML + PDF)
- `zenodo-metadata.json`: Zenodo upload metadata

## Reading Guide

The paper serves multiple audiences:

- **ML alignment researchers:** §§2–4 (mechanism), §7 (predictions), §8 (alternate hypotheses)
- **Cognitive scientists / HCI researchers:** §6 (functional empathy), §10 (psychological parallels)
- **Policy / education researchers:** §9 (intervention implications), §10 (wider context)

The core mechanism is self-contained in §§2–4. An ML reader can stop there and have a testable proposal.

## Citation

```bibtex
@misc{phan2026uncertainty,
  title={Uncertainty Collapse in Post-Trained Language Models: Keep Calm or Carry On},
  author={Phan, Ivan},
  year={2026},
  note={Preprint. DOI: 10.5281/zenodo.19482051},
  url={https://hip1.github.io/Uncertainty-Collapse/}
}
```

## Related Work

This paper extends the Confidence Curriculum series:

- [P1: The Confidence Vulnerability](https://hip1.github.io/confidence-curriculum/)
- [P5: The Confidence Collision](https://hip1.github.io/confidence-curriculum/)
- [Divided Focus](https://hip1.github.io/Divided-Focus/divided-focus.html)

## Acknowledgments

Developed through adversarial collaboration with three frontier language models acting as methodological instruments: Claude Opus 4.6 (Weaver), ChatGPT (Surgeon), and Gemini (Alchemist). The author served as sole editorial authority.

All predictions were derived from the framework before any literature search for supporting evidence.
