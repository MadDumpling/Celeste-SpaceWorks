# Contributing to Celeste SpaceWorks

Thank you for contributing to Celeste SpaceWorks.

Celeste SpaceWorks is an open engineering and scientific software project focused on spacecraft design, mission analysis, engineering traceability, and aerospace reference data.

Whether you are contributing code, documentation, tests, datasets, design proposals, bug reports, or engineering research, your contributions help improve the project's accuracy, usability, and long-term sustainability.

---

# Project Philosophy

Celeste SpaceWorks is guided by a few core principles:

> Traceability is more important than completeness.

> Unknown data is preferable to unsupported assumptions.

> Engineering transparency is more valuable than artificial precision.

> Systems should grow through reusable architecture and validated data.

The project favors:

- documented facts over assumptions
- reproducible results over convenience
- simplicity over unnecessary complexity
- maintainable architecture over quick fixes
- data-driven growth over hardcoded behavior

---

# Ways to Contribute

Contributions are not limited to software development.

Examples include:

## Software Development

- Bug fixes
- New features
- UI improvements
- Rendering enhancements
- Performance optimization
- Testing infrastructure
- Build tooling
- Documentation tooling

---

## Engineering and Scientific Data

- Launch site datasets
- Vehicle datasets
- Component libraries
- Mission packages
- Landing site packages
- Celestial body datasets
- Validation datasets

See:

```text
docs/DATA-CONTRIBUTION.md
```

for detailed data-contribution requirements.

---

## Documentation

Examples:

- User guides
- Tutorials
- Architecture documentation
- API documentation
- Engineering notes
- Validation procedures
- Contributor onboarding material

---

## Testing

Examples:

- Unit tests
- Integration tests
- Regression tests
- Validation cases
- Historical reconstruction tests

---

## Research

Examples:

- Source identification
- Historical mission reconstruction
- Validation benchmark development
- Engineering reviews
- Data-gap resolution

---

# Development Principles

## Keep Systems Decoupled

Prefer solutions that improve separation of concerns.

Good:

```text
UI
    ↓

Application

    ↓

Engineering Domain

    ↓

Simulation
```

Avoid:

```text
UI
    ↓

Directly manipulating simulation internals
```

---

## Generic Before Specialized

When adding new features, ask:

> Can this be useful outside aerospace?

Examples:

Generic:

```text
Mass Properties
Attachment Nodes
Constraint Systems
Provenance Tracking
Readiness Assessment
Rule Engines
```

Aerospace-Specific:

```text
Lambert Solver
Lunar Missions
TLI Analysis
Apollo Reference Data
```

Whenever practical:

```text
engineering/
```

should contain reusable systems.

```text
aerospace/
```

should contain aerospace-specific behavior.

---

## Prefer Extension Over Modification

The architecture should evolve primarily through:

```text
New Data
New Packages
New Configurations
```

rather than:

```text
New Hardcoded Logic
```

Good:

```text
Add a Mars mission package
```

Better than:

```text
Add Mars-specific conditionals throughout the codebase
```

---

# Code Standards

## Readability First

Code is read more often than it is written.

Prefer:

```python
required_delta_v = available_delta_v - margin
```

over:

```python
rdv = adv - m
```

unless the abbreviation is widely understood.

---

## Explicit Is Better Than Implicit

Prefer:

```python
if engine is None:
```

over:

```python
if not engine:
```

when checking engineering objects.

---

## Unknown Means Unknown

Do not replace unknown values with defaults.

Correct:

```python
max_tilt_deg = None
```

Incorrect:

```python
max_tilt_deg = 15.0
```

unless supported by a source.

This principle applies to both code and data.

---

## Fail Closed

When required data is unavailable:

Prefer:

```python
raise MissingDataError(...)
```

over:

```python
return guessed_value
```

Many systems intentionally refuse to make unsupported engineering claims.

---

# Architecture Principles

## Preserve Separation Between Domains

Target architecture:

```text
core/
engineering/
aerospace/
knowledge/
rendering/
viewport/
ui/
```

Contributions should move the system toward clearer boundaries rather than tighter coupling.

---

## Engineering vs Aerospace

Reusable functionality belongs in:

```text
engineering/
```

Examples:

```text
Components
Mass Properties
Constraint Systems
Placement
Attachment Nodes
Provenance
Readiness
Rule Engines
```

Aerospace-specific functionality belongs in:

```text
aerospace/
```

Examples:

```text
Orbit Mechanics
Mission Planning
Lunar Analysis
Trajectory Propagation
Planetary Data Access
Touchdown Assessment
```

---

## Data vs Logic

Reference information should live in data packages.

Prefer:

```text
knowledge/apollo/
knowledge/missions/
knowledge/landing_sites/
```

over embedding mission data directly in simulation code.

---

# Future Assembly System

The project is moving toward a true assembly-based architecture.

Contributors should consider future compatibility with:

```text
Attachment Nodes
Assembly Graphs
Constraint Systems
Viewport Gizmos
Symmetry Placement
```

---

## Attachment Nodes

Future attachable parts should support:

```text
Top Nodes
Bottom Nodes
Side Nodes
Mount Nodes
```

Attachments should be represented through:

```text
Node Relationships
```

rather than raw coordinates.

---

## Assembly Graph

Future spacecraft assemblies are expected to evolve toward:

```text
Part
    ↓

Node
    ↓

Constraint
    ↓

Assembly Graph
```

rather than:

```text
Part
    ↓

Position
```

---

## Gizmo-Based Editing

Future viewport functionality may include:

```text
Translate Gizmos
Rotate Gizmos
Scale Gizmos
Node Snap Gizmos
```

New editor features should avoid assumptions that conflict with this direction.

---

# Testing Requirements

Bug fixes should include tests whenever practical.

Examples:

```text
Unit Tests
Regression Tests
Historical Validation Tests
```

A bug is not fully fixed until it becomes difficult to reintroduce.

---

# Documentation Requirements

New systems should include documentation where appropriate.

At minimum contributors should document:

```text
Purpose
Inputs
Outputs
Assumptions
Known Limitations
```

---

# Pull Request Guidelines

Before submitting a pull request:

- [ ] Code builds successfully
- [ ] Existing tests pass
- [ ] New tests added where appropriate
- [ ] Documentation updated if needed
- [ ] No unsupported engineering assumptions introduced
- [ ] Architecture boundaries respected
- [ ] New data includes provenance information
- [ ] Unknown values remain unknown

---

# Issues and Feature Requests

Feature requests should ideally explain:

```text
Problem
Motivation
Expected Behavior
Potential Architecture Impact
```

Rather than only describing an implementation.

Good:

```text
Need support for reusable attachment nodes.
```

Less helpful:

```text
Add field X to class Y.
```

Focus on the engineering problem first.

---

# Respect the Long-Term Vision

The long-term goal is for Celeste SpaceWorks to grow through:

```text
New Data
+ New Vehicles
+ New Components
+ New Missions
+ New Validation Datasets
+ New Celestial Bodies

= New Capability
```

while keeping:

```text
Engineering Platform
Simulation Framework
Readiness System
Provenance System
Assembly System
```

relatively stable.

Contributors are encouraged to build solutions that are:

- reusable
- traceable
- testable
- data-driven
- maintainable

for the long-term benefit of the project.

---

# Final Note

Perfection is not required.

Well-documented limitations, known gaps, and clear uncertainty are valuable contributions.

A contribution that clearly states:

```text
"This value is unknown."
```

is more useful than one that silently invents an answer.

The project values honesty, reproducibility, and engineering rigor above apparent completeness.
