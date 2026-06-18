# Claude Code Instructions

This repository is a portable English-only economics paper pre-review skill.

When asked to review an economics paper, follow `SKILL.md` and the canonical protocol in `references/`.

Default command:

```text
Review this economics paper using the economics-paper-reviewer protocol.
```

Required behavior:

- Review English economics papers only.
- Classify the paper type before choosing a review lens.
- If the task is benchmark, validation, or reviewer-quality testing, load `references/benchmark_mode.md`.
- Use the six-role economics review panel.
- Use economics-specific literature grounding when tools are available.
- Mark unverified literature, data, method, theorem, style, and structure claims as provisional.
- Produce a structured pre-review report, not a final editorial decision.

Do not duplicate or override the protocol in `references/`; load the relevant reference files as needed.
