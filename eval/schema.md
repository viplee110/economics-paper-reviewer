# Evaluation Case Schema

Each lightweight evaluation case uses:

```text
eval/cases/[case_id]/
  input.md
  expected_review.md
```

## input.md

Minimum fields:

```text
Case id:
Paper type:
Target or venue class:
Manuscript excerpt:
Available evidence:
Unavailable evidence:
Reviewer task:
```

## expected_review.md

Minimum fields:

```text
Expected paper type:
Must-load lenses:
Must-not-miss strengths:
Must-not-miss fatal risks:
Fixable risks:
Wrong criticisms:
Expected recommendation range:
Expected scorecard flags:
Evidence labels expected:
```

Do not include copyrighted paper text unless permission is clear. Toy cases are preferred for v1.

Supported v1 paper types include theory, empirical causal, structural, econometrics, experimental, computational, survey or literature review, and mixed papers.
