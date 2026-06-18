# Computational / Simulation Review Lens

Use for computational economics, agent-based models, numerical dynamic models, simulations, calibration, algorithmic mechanism design, and computation-heavy papers.

## Must Check

- What economic question requires computation?
- Are algorithms specified clearly?
- Are calibration choices justified?
- Are numerical results robust to parameters, seeds, grids, tolerances, or solver choices?
- Is code or pseudocode sufficient for reproducibility?
- Are simulations tied to economic interpretation?
- Are limitations and failure modes clear?

## Fatal Risks

- algorithm is underspecified
- results depend on unreported calibration choices
- no robustness to numerical settings
- code or data access is insufficient for claims made
- simulation output is interpreted as theory without justification
- economic mechanism is hidden by computation

## Fixable Risks

- missing pseudocode
- weak numerical diagnostics
- unclear calibration table
- insufficient sensitivity analysis
- incomplete replication instructions
