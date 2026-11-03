# Data Contribution Guide

Thank you for contributing reference data to Celeste SpaceWorks.

The long-term goal of Celeste SpaceWorks is to grow primarily through the addition of high-quality engineering and scientific datasets rather than modifications to the simulation core. Contributors are therefore building a reusable aerospace reference library, not merely supplying JSON files.

The most important principle is:

> Traceability is more important than completeness.
>
> A missing value is acceptable.
> An undocumented assumption is not.

---

# Scope

Contributors may provide:

- Launch site packages
- Spacecraft component packages
- Vehicle packages
- Historical mission packages
- Celestial body datasets
- Landing site datasets
- Validation datasets
- Supporting scientific reference data

Examples include:

- Apollo Lunar Module
- Saturn V
- Falcon 9
- Tranquility Base
- Jezero Crater
- Kennedy Space Center LC-39A
- Moon gravity models
- Apollo 11 mission references

---

# Core Principles

## 1. Unknown Means Unknown

Never replace missing data with assumptions.

Correct:

```json
{
  "engine_clearance_m": null
}
```

Incorrect:

```json
{
  "engine_clearance_m": 1.0
}
```

unless the value is explicitly supported by a source.

---

## 2. Every Value Must Be Traceable

Contributors must be able to answer:

1. Where did this value come from?
2. How was it derived?
3. How reliable is it?

If these questions cannot be answered, the value should not be included.

---

## 3. Preserve Scientific Uncertainty

Aerospace data is often incomplete.

Do not hide uncertainty.

Correct:

```json
{
  "uncertainty_pct": null
}
```

Incorrect:

```json
{
  "uncertainty_pct": 5.0
}
```

unless a source provides or supports the estimate.

---

## 4. Prefer Primary Sources

Preferred source hierarchy:

1. Flight telemetry
2. Test data
3. Manufacturer documentation
4. Agency publications (NASA, ESA, JAXA, ISRO, CNSA, etc.)
5. Peer-reviewed papers
6. Technical books
7. Secondary summaries
8. Wikipedia

Wikipedia may be used as a discovery aid but should not be the sole source for critical engineering values.

---

# Provenance Requirements

Every package must contain a provenance record.

Example:

```json
{
  "provenance": {
    "quality": "published",
    "source": "NASA TN D-7143",
    "revision": "March 1973",
    "uncertainty_pct": null,
    "notes": "Engine performance values from mission-era documentation."
  }
}
```

---

# Data Quality Classification

Every dataset and every component must use one of the following quality levels.

## measured

Direct observations or measurements.

Examples:

- Telemetry
- Laboratory measurements
- Surveyed coordinates

```json
{
  "quality": "measured"
}
```

---

## published

Officially published values.

Examples:

- NASA reports
- Manufacturer specifications
- Mission documentation

```json
{
  "quality": "published"
}
```

---

## estimated

Values derived from published information.

Examples:

- CAD measurements
- Mass derivations
- Geometry reconstructions

```json
{
  "quality": "estimated"
}
```

Estimated values must include a methodology note.

---

## illustrative

Synthetic or educational examples.

Examples:

- Showcase demos
- Failure demonstrations
- Tutorial vehicles

```json
{
  "quality": "illustrative"
}
```

Illustrative data must never be presented as historical or flight-qualified data.

---

# Source Citation Standards

Every non-illustrative dataset must include at least one source.

Minimum:

```json
{
  "source": "NASA TN D-7143"
}
```

Preferred:

```json
{
  "source": [
    {
      "title": "NASA TN D-7143",
      "url": "...",
      "pages": "64-68"
    }
  ]
}
```

---

# Estimation Standards

Estimated values are permitted.

Estimated values must document their derivation.

Example:

```json
{
  "quality": "estimated",
  "notes": "Measured from NASA CAD model and cross-checked against published dimensions."
}
```

Unexplained estimates will be rejected during review.

---

# Package Structure

All packages must contain:

```json
{
  "schema_version": 2,

  "id": "unique_identifier",

  "name": "Human-readable Name",

  "revision": "...",

  "provenance": {...}
}
```

---

# Identifier Rules

Identifiers must:

- Use lowercase
- Use underscores
- Be stable over time
- Never depend on display names

Good:

```json
"id": "apollo_lm_descent"
"id": "tranquility_base"
"id": "ksc_lc39a"
```

Bad:

```json
"id": "Apollo LM"
```

Names may change.

Identifiers must not.

---

# Units

All values must use SI units whenever possible.

Examples:

| Quantity | Unit |
|----------|------|
| Mass | kg |
| Force | N |
| Length | m |
| Velocity | m/s |
| Pressure | Pa |
| Rotation Rate | deg/s |
| Energy | kWh |
| Power | kW |

If original sources use non-SI units, cite the original source and convert the stored value to SI.

---

# Data Gap Reporting

Known missing information must be documented.

Example:

```json
{
  "data_gaps": [
    "allowable_touchdown_tilt_deg",
    "allowable_touchdown_rate_deg_s",
    "engine_clearance_m"
  ]
}
```

A package with documented gaps is preferable to a package containing unsupported assumptions.

---

# Readiness Levels

Datasets may be assigned readiness classifications.

## Demonstration

Illustrative and educational.

## Prototype

Source-backed but contains significant gaps.

## Reference

Substantially complete and traceable.

## Validated

Cross-checked against historical flight or mission data.

---

# Vehicle Contributions

Vehicle datasets should include:

- Vehicle name
- Revision description
- Components
- Landing gear (if applicable)
- Mass information
- Sources
- Data gaps
- Provenance

Vehicle contributors should avoid reconstructing unknown subsystem details without evidence.

---

# Mission Contributions

Mission packages should include:

- Launch information
- Mission timeline
- Transfer references
- Orbit parameters
- Landing site references
- Sources
- Validation references

Mission packages are historical references unless explicitly marked illustrative.

---

# Celestial Body Contributions

Required where available:

- Physical constants
- Radius
- Mass
- Gravity parameters
- Rotation information
- Terrain references
- Gravity model references
- Ephemeris references

---

# Validation Data Contributions

Validation datasets are highly encouraged.

Examples:

- Apollo 11 touchdown conditions
- Apollo LM descent profile
- Surveyor landing metrics
- Falcon 9 recovery trajectories

Validation datasets help verify simulation behavior against historical references.

---

# Spacecraft Components

Contributors should prefer the smallest reusable component that can accurately represent the source material.

If a subsystem can reasonably be used in multiple vehicles, it should be contributed as a Part package.

Vehicles should primarily be assemblies of referenced parts rather than monolithic datasets.

All attachable parts must define one or more attachment nodes. Attachment nodes represent physical connection locations and form the primary assembly mechanism used by Celeste SpaceWorks.
---

# Review Checklist

All submissions must satisfy the following:

- [ ] Valid JSON
- [ ] Correct schema version
- [ ] Stable identifier
- [ ] Provenance record included
- [ ] Sources documented
- [ ] Units documented
- [ ] No unsupported assumptions
- [ ] Unknown values remain null
- [ ] Estimates explain methodology
- [ ] Data gaps documented
- [ ] Readiness classification appropriate

---

# Acceptance Philosophy

Celeste SpaceWorks is a scientific and engineering reference project.

Contributors should favor:

- documented facts over assumptions
- provenance over convenience
- uncertainty over false precision
- traceability over completeness

A package with ten well-supported values and twenty documented unknowns is significantly more valuable than a package containing thirty undocumented guesses.
