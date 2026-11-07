# Celeste SpaceWorks

Celeste SpaceWorks is a data-driven aerospace engineering platform for vehicle design, mission analysis, engineering traceability, and scientific reference modeling.

The project combines spacecraft configuration, mission screening, trajectory simulation, engineering readiness assessment, provenance tracking, and aerospace reference datasets into a unified environment for exploring real-world and conceptual space systems.

Unlike traditional spacecraft design tools, Celeste SpaceWorks treats engineering data as a first-class concern. Every vehicle, component, mission profile, and reference dataset can carry source citations, uncertainty information, revision metadata, and readiness assessments.

---

## Setup

Requires Python 3.11 and a GPU/driver with OpenGL 3.3.

```powershell
.\setup.ps1   # create .venv and install requirements
.\run.ps1     # launch the configurator
.\test.ps1    # run the tests
```

On macOS/Linux use `setup.sh`, `run.sh`, and `test.sh`.

See [docs/LUNAR_LANDING_ROADMAP.md](docs/LUNAR_LANDING_ROADMAP.md) for the
project's definition of a successful lunar landing and the fidelity roadmap.

## Current Capabilities

### Vehicle Design

Create spacecraft from reusable components:

- Engines
- Fuel tanks
- Payloads
- Landing gear
- RCS systems
- Solar arrays
- Batteries
- Avionics
- Power systems

Each component can contain:

- Mass properties
- Operational limits
- Geometry
- Attachment information
- Provenance metadata

Designs are saved as versioned JSON spacecraft definitions.

---

### Interactive 3D Visualization

An OpenGL-powered viewport provides:

- Real-time spacecraft visualization
- Orbit camera controls
- Component selection and highlighting
- Exploded views
- Mass-property visualization
- Center-of-mass indicators
- Manual component placement
- Attachment-based positioning

Visualization is generated from engineering data and is intended as an engineering aid rather than a CAD system.

---

### Engineering Analysis

Vehicle definitions are analyzed continuously as they are edited.

Current metrics include:

- Dry mass
- Wet mass
- Fuel mass
- Thrust
- TWR
- Burn duration
- Delta-v
- Power generation
- Power consumption
- Electrical margins
- Battery capacity
- Static stability metrics

---

### Mission Analysis

Current mission tools support:

- Mission feasibility assessment
- Lunar reachability analysis
- Date-specific transfer screening
- Earth-to-Moon trajectory checks
- Lambert transfer solutions
- DE440s ephemeris integration
- Closest-approach analysis

Mission simulations evaluate whether a trajectory reaches the Moon's sphere of influence using propagated Earth-Moon-Sun dynamics.

---

### Design Advisor

A deterministic engineering advisor evaluates:

- Thrust-to-weight limitations
- Delta-v shortfalls
- Propellant issues
- Power-system deficits
- Readiness gaps
- Traceability issues
- Mission bottlenecks

Each finding includes:

- Severity
- Supporting evidence
- Recommended action

---

### Engineering Readiness Assessment

Vehicle definitions are continuously evaluated for:

- Missing engineering data
- Traceability issues
- Missing sources
- Unknown operational limits
- Missing mass properties
- Landing-certification blockers

Unknown values remain unknown.

The system intentionally avoids replacing missing engineering data with assumptions.

---

### Provenance and Traceability

Every vehicle and component supports source tracking.

Supported quality levels:

- `measured`
- `published`
- `estimated`
- `illustrative`

Reference data includes:

- Source information
- Revision information
- Uncertainty metadata
- Engineering notes

---

### Aerospace Reference Data

The project includes source-backed aerospace reference datasets.

Current examples include:

- Apollo Lunar Module
- Apollo 11 mission references
- Lunar landing site data
- Gravity-model references
- Terrain-model references
- Historical mission timelines

Reference packages are independent of user-created spacecraft designs and are intended for validation, benchmarking, and engineering study.

---

## Project Philosophy

Celeste SpaceWorks is guided by four core principles:

### Unknown Does Not Mean Zero

Unknown values remain:

```python
None
```

The software should not silently invent engineering data.

---

### Traceability Over Completeness

A dataset with:

```text
10 supported values
20 documented unknowns
```

is preferable to:

```text
30 undocumented guesses
```

---

### Data-Driven Growth

The project should scale primarily through:

```text
New Data
+ New Vehicles
+ New Components
+ New Missions
+ New Celestial Bodies
+ New Validation Datasets
```

rather than major changes to simulation code.

---

### Engineering Transparency

Simulation results should explain:

- What is known
- What is assumed
- What is estimated
- What is unknown

so users can judge model fidelity appropriately.

---

# Roadmap

## Assembly System

The current placement system provides:

- Attachment nodes
- Parent-child relationships
- Placement offsets
- Rotational alignment
- Symmetry groups

Future work will evolve this into a full assembly framework.

Planned features include:

- Structured assembly graphs
- Constraint-based assembly
- Node compatibility rules
- Radial symmetry placement
- Attachment validation

---

## Viewport Gizmos

Planned editor improvements include:

- Translation gizmos
- Rotation gizmos
- Scale gizmos
- Snap-to-node assembly tools
- Attachment previews
- Assembly overlays

The long-term goal is to move from coordinate-based placement toward engineering assembly workflows.

---

## Aerospace Reference Library

Future datasets are expected to include:

### Launch Sites

- LC‑39A
- LC‑39B
- Vandenberg
- Boca Chica
- Baikonur
- Guiana Space Centre
- Additional launch facilities

### Historical Vehicles

- Apollo CSM
- Saturn V
- Falcon 9
- Falcon Heavy
- Starship
- SLS
- Orion
- Space Shuttle
- Blue Moon

### Celestial Bodies

- Earth
- Moon
- Mars
- Venus
- Mercury
- Europa
- Titan

### Missions

- Apollo Program
- Artemis Program
- Luna Program
- Surveyor Program
- Viking
- Mars Pathfinder
- Chang'e Program

---

## Landing Simulation

The long-term goal of the project is verified lunar touchdown assessment.

Development areas include:

- Powered descent
- Terrain interaction
- Landing-gear dynamics
- Surface certification
- Historical validation
- Monte Carlo analysis

See:

- `docs/LUNAR_LANDING_ROADMAP.md`
- `docs/LUNAR_MISSION_PHYSICS_AND_DEMO_SCENARIOS.md`

for additional detail.

---

## Project Structure

```text
core/           Infrastructure and eventing
ui/             User interface
viewport/       Camera and visualization workflows
rendering/      OpenGL rendering backend
spacecraft/     Engineering and aerospace domain logic
presets/        Example spacecraft definitions
docs/           Documentation
tests/          Automated tests
```

### Planned Architecture

```text
core/
engineering/
aerospace/
knowledge/
rendering/
viewport/
ui/
```

where:

- `engineering/` contains domain-independent engineering systems
- `aerospace/` contains spacecraft and mission logic
- `knowledge/` contains reference data packages

---

## Contributing

See:

- `CONTRIBUTING.md`
- `docs/DATA-CONTRIBUTION.md`

before submitting changes.

Contributors should favor:

- documented facts over assumptions
- provenance over convenience
- uncertainty over false precision
- reusable architecture over quick fixes

