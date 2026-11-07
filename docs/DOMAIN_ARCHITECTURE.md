# Spacecraft Domain Architecture

The `spacecraft` package is the core engineering domain of Celeste SpaceWorks.

Unlike the rendering and UI layers, the domain package owns vehicle modeling, physics analysis, mission simulation, engineering traceability, readiness assessment, reference data, landing assessment, and decision support.

---

# Domain Philosophy

A foundational architectural principle appears throughout the entire system:

```text
Unknown data is explicitly represented.

Unknown != Zero
Unknown != Assumed
Unknown != Estimated
```

The system intentionally fails closed.

Examples:

```python
None = Unknown
```

rather than:

```python
None -> 0
```

or

```python
None -> Default Value
```

Several calculations raise:

```python
MissingDataError
```

instead of silently inventing values.

This is a deliberate engineering-assurance decision.

---

# Domain Capability Map

```text
spacecraft
│
├── Vehicle Definition
│
├── Performance Analysis
│
├── Mission Analysis
│
├── Trajectory Simulation
│
├── Landing Assessment
│
├── Engineering Data Governance
│
├── Provenance / Traceability
│
├── Historical Reference Data
│
├── Design Intelligence
│
├── Geometry Generation
│
└── Persistence
```

---

# Architectural Context

```text
                    ┌─────────────────┐
                    │      UI         │
                    │  DearPyGui      │
                    └────────┬────────┘
                             │
                             ▼

            ┌───────────────────────────────────┐
            │      Spacecraft Domain Layer      │
            └───────────────────────────────────┘
                             │

 ┌─────────────┬─────────────┼──────────────┬────────────┐
 │             │             │              │            │
 ▼             ▼             ▼              ▼            ▼

Vehicle    Analysis     Mission      Readiness      Geometry
Modeling               Simulation   & Assurance    Generation

 │             │             │              │            │
 └─────────────┴──────┬──────┴──────────────┘            │
                      │                                 │
                      ▼                                 ▼

              Design Advisor                    Rendering
                                                   Layer
```

---

# 1. Vehicle Definition System

Files:

```text
vehicle.py
components.py
placement.py
propulsion.py
appearance.py
```

## Purpose

Represents a spacecraft as a structured engineering model.

## Aggregate Root

```python
Spacecraft
```

owns:

```text
Components
Appearance
Landing Gear
Attitude Limits
Provenance
Revision Information
Layout Metadata
```

All engineering workflows operate against a `Spacecraft` aggregate.

---

# Component Architecture

## Base Type

```python
Component
```

## Component Hierarchy

```text
Component
│
├── Engine
├── FuelTank
├── Payload
├── PowerSystem
├── LandingLeg
├── RcsThruster
├── SolarPanel
├── Battery
└── Avionics
```

---

## Component Characteristics

Every component can contain:

```text
Mass
Geometry
Center of Mass
Inertia
Placement
Stage Assignment
Engineering Parameters
Provenance
```

---

## Placement System

Implemented in:

```text
placement.py
```

Supports:

```text
Parent Child Attachments
Attach Nodes
Symmetry Groups
Offsets
Rotations
Kerbal-Style Assembly
```

Attachment nodes include:

```text
top
bottom
side
mount
```

---

# 2. Propulsion Architecture

Files:

```text
propulsion.py
components.py
```

The propulsion subsystem models engine operating envelopes rather than simple thrust values.

---

## Throttle Model

```python
ThrottleSpec
```

Represents:

```text
Minimum Throttle
Maximum Throttle
Throttle Curves
Mass Flow Curves
Isp Curves
Non-Operating Regions
```

Example:

```text
Apollo LM
65%-92.5%
Excluded Operating Region
```

may be represented explicitly.

---

## Ignition Model

```python
IgnitionLimits
```

Captures:

```text
Maximum Ignitions
Restart Capability
Minimum Burn Duration
Maximum Burn Duration
Minimum Impulse Bit
Shutdown Tail-off
```

---

## Gimbal Model

```python
Gimbal
```

Captures:

```text
Gimbal Authority
Gimbal Rate Limits
```

---

## Architectural Observation

The subsystem models:

```text
Operational Envelope
```

instead of:

```text
Nominal Performance
```

This enables future fidelity without changing the architecture.

---

# 3. Engineering Analysis Architecture

Files:

```text
analysis.py
mass_properties.py
```

---

## Vehicle Performance Analysis

Primary Service:

```python
analyze_spacecraft()
```

Produces:

```python
SpacecraftAnalysis
```

including:

```text
Dry Mass
Wet Mass
Fuel Mass
Thrust
RCS Thrust
Specific Impulse
Delta-V
TWR
Burn Duration
Power Generation
Power Draw
Power Margin
Battery Storage
```

---

## Mission Assessment

Produces:

```python
MissionAssessment
```

Evaluates:

```text
Mission Feasibility
Delta-V Margin
TWR Requirements
Mission Constraints
```

against predefined mission profiles.

---

## Mass Properties Analysis

Produces:

```python
MassProperties
```

including:

```text
Center Of Mass
Inertia
Mass Distribution
Missing Data Reports
```

---

## Stability Analysis

Provides:

```python
static_tip_over_angle_deg()
```

Used for:

```text
Landing Stability
Ground Stability
Static Tipping Limits
```

---

# 4. Mission Analysis Architecture

Mission functionality exists at two fidelity levels.

---

## Level 1: Mission Budgeting

File:

```text
lunar.py
```

Provides:

```python
estimate_lunar_orbit_budget()
```

Produces:

```python
LunarOrbitBudget
```

using:

```text
Astropy
DE440s
Patched-Conic Methods
Lunar Constants
```

---

## Lunar Reachability Analysis

Produces:

```python
LunarReachability
```

Evaluates:

```text
Available Delta-V
Required Delta-V
Mission Margin
Launch Feasibility
```

---

# 5. High Fidelity Mission Simulation

File:

```text
mission.py
```

Provides:

```python
run_lunar_flyby_simulation()
```

---

## Mission Pipeline

```text
Launch Date
      │
      ▼

DE440s Ephemeris Query
      │
      ▼

Moon State Determination
      │
      ▼

Lambert Solution
      │
      ▼

Injection Analysis
      │
      ▼

Numerical Propagation
      │
      ▼

Closest Approach Analysis
      │
      ▼

SOI Encounter Evaluation
```

---

## Numerical Models

### Lambert Solver

```python
lambert_universal()
```

Provides:

```text
Transfer Velocity
Arrival Velocity
Boundary Value Solution
```

---

### Propagation

Uses:

```python
solve_ivp()
```

with:

```text
Earth Gravity
Moon Gravity
Sun Gravity
```

forming an:

```text
N-Body Lunar Encounter Screening Model
```

---

## Current Success Definition

Mission success currently means:

```text
The propagated trajectory enters
the Moon's sphere of influence.
```

Success does NOT imply:

```text
Orbit Capture
Lunar Orbit Insertion
Powered Descent
Landing
Safe Touchdown
```

---

# 6. Engineering Data Governance

Files:

```text
provenance.py
readiness.py
```

This subsystem is one of the defining features of the platform.

---

## Provenance System

Primary Type:

```python
DataProvenance
```

Tracks:

```text
Quality
Source
Revision
Uncertainty
Units
Notes
```

---

## Quality Levels

```text
Measured
Published
Estimated
Illustrative
```

---

## Traceability Rules

Measured and published data require:

```text
Source Citation
Revision Information
```

Unknown uncertainty remains unknown and is never silently substituted.

---

## Architectural Pattern

```text
Evidence-Based Modeling
```

rather than:

```text
Simulation-Only Modeling
```

---

# 7. Readiness Assessment Architecture

File:

```text
readiness.py
```

Produces:

```python
DefinitionReport
```

which functions as an engineering readiness review.

---

## Gap Classification

```text
Blocking
Warning
```

---

## Example Readiness Checks

### Vehicle Definition

```text
Revision
Vehicle Provenance
```

### Landing System

```text
Landing Gear Geometry
Engine Clearance
Touchdown Speed Ratings
```

### Attitude

```text
Maximum Tilt
Maximum Angular Rate
```

### Engines

```text
Throttle Ranges
Ignition Limits
Gimbal Authority
Exit Area
```

### Mass Properties

```text
Center Of Mass
Inertia
```

---

## Readiness States

```text
TRACEABLE DATA
```

and

```text
PROTOTYPE DATA
```

The system intentionally prevents unsupported landing-certification claims.

---

# 8. Design Intelligence Architecture

File:

```text
advisor.py
```

This is a dedicated subsystem rather than a utility.

---

## Purpose

Transform engineering outputs into actionable recommendations.

---

## Inputs

```python
Spacecraft
SpacecraftAnalysis
MissionProfile
MissionSimulationResult
DefinitionReport
```

---

## Output

```python
AdviceItem
```

Structure:

```text
Severity
Title
Evidence
Suggested Action
```

---

## Severity Levels

```text
CRITICAL
HIGH
MEDIUM
LOW
```

---

## Rule Categories

### Vehicle Feasibility

```text
Missing Engines
Insufficient TWR
Missing Propellant
Propellant Mismatch
```

### Mission Budget

```text
Delta-V Shortfalls
```

### Trajectory Analysis

```text
SOI Miss
Transfer Failure
Predicted Impact
```

### Electrical Power

```text
Generation Deficits
Load Imbalances
```

### Readiness

```text
Missing COM
Missing Landing Data
Missing Touchdown Inputs
```

### Traceability

```text
Illustrative Data
Estimated Data
```

---

## Architectural Pattern

```text
Rule-Based Expert System
```

Characteristics:

```text
Deterministic
Explainable
Evidence-Based
Traceable
Human Readable
```

---

# 9. Landing Certification Architecture

Files:

```text
touchdown.py
reference_data.py
```

---

## Current State

The platform does not yet perform full descent simulation.

Instead it provides:

```python
assess_touchdown()
```

which classifies touchdown conditions.

---

## Inputs

```text
Latitude
Longitude
Vertical Velocity
Horizontal Velocity
Tilt
Angular Rate
Terrain Contact Status
```

---

## Outputs

```text
Success
Failure
Reasons
```

---

## Certification Philosophy

The subsystem intentionally fails closed.

Example:

```text
Unknown Touchdown Tilt Limit
      ↓
Landing Not Certifiable
```

rather than:

```text
Unknown Touchdown Tilt Limit
      ↓
Assume Safe
```

---

# 10. Reference Data Architecture

Files:

```text
apollo_lm.py
apollo11_reference.py
reference_data.py
```

These files form an embedded engineering knowledge base.

---

## Apollo LM Reference Vehicle

Provides:

```text
Source-backed Vehicle Definition
Reference Parameters
Known Data Gaps
Traceable Assumptions
```

---

## Apollo 11 Reference Mission

Provides:

```text
Mission Events
Trajectory Anchors
Launch Information
Historical Flight Data
```

---

## Lunar Landing Reference Database

Provides:

```text
Landing Site Data
Gravity Models
Terrain Models
Descent Profiles
Touchdown Reconstructions
Validation Targets
Certification Statistics
```

---

## Data Gap Register

Current reference-data roadmap maintains explicit gap tracking:

```text
G1 - Touchdown Tilt Limits
G2 - Stage Mass Data
G3 - Apollo Touchdown Mass
G4 - Engine Throttle Curves
G5 - Ambient Pressure Effects
...
G20 - Validation Flight Histories
```

---

# 11. Geometry Architecture

File:

```text
geometry.py
```

This is not a rendering subsystem.

It is a vehicle-assembly and geometry-generation subsystem.

---

## Responsibilities

Produces:

```text
Vehicle Layouts
Primitive Meshes
Part Placement
Bounding Volumes
COM Markers
Vehicle Extents
Flags and Markings
Attachment Geometry
```

---

## Architectural Role

```text
Domain Geometry Engine
```

Consumes:

```text
Vehicle Definitions
```

Produces:

```text
Render-Ready Geometry
```

without depending on OpenGL.

---

# 12. Persistence Architecture

File:

```text
presets.py
```

Provides:

```text
JSON Persistence
Versioned Schemas
Validation
Typed Reconstruction
```

---

## Current Schema

```text
Schema Version 2
```

Supports:

```text
Backward Compatibility
Forward Evolution
Strict Validation
```

---

# Architectural Characterization

Celeste SpaceWorks is best described as:

```text
Engineering Decision Support Platform
for Spacecraft Design,
Mission Screening,
Landing Certification,
and Engineering Traceability.
```

Its primary bounded contexts are:

```text
1. Vehicle Definition
2. Engineering Analysis
3. Mission Simulation
4. Landing Certification
5. Data Governance
6. Design Intelligence
7. Reference Knowledge
```

The most distinctive aspect of the architecture is that simulation, traceability, readiness assessment, provenance management, and engineering decision support are all first-class subsystems rather than supporting utilities.

# Target Architecture Direction

## Problem

The current `spacecraft` package contains both:

### Generic Engineering Platform Logic

```text
Component
Engine
FuelTank
Battery
PowerSystem
Provenance
Readiness
Mass Properties
Placement
Geometry
Persistence
```

and

### Aerospace-Specific Logic

```text
Lunar Mission Analysis
Earth-Moon Transfers
Lambert Solver
DE440 Ephemeris
Apollo LM
Apollo 11 Data
Touchdown Certification
TLI Budgets
Lunar Reachability
```

This creates coupling between:

```text
Engineering Framework
```

and

```text
Aerospace Domain
```

---

# Target Separation

## Core Engineering Platform

Reusable, domain-agnostic functionality.

```text
engineering/
│
├── components/
│   ├── component.py
│   ├── propulsion.py
│   ├── power.py
│   └── structures.py
│
├── geometry/
│   ├── placement.py
│   ├── transforms.py
│   └── geometry.py
│
├── analysis/
│   ├── mass_properties.py
│   ├── readiness.py
│   └── provenance.py
│
├── persistence/
│   └── json_store.py
│
└── advisory/
    └── rule_engine.py
```

This layer contains no knowledge of:

```text
Moon
Earth
Apollo
Orbit
Launch
Spacecraft
```

---

# Aerospace Domain

Built on top of the engineering framework.

```text
aerospace/
│
├── vehicles/
│   ├── spacecraft.py
│   ├── spacecraft_components.py
│   └── spacecraft_analysis.py
│
├── astrodynamics/
│   ├── lambert.py
│   ├── propagation.py
│   ├── ephemerides.py
│   └── orbital_mechanics.py
│
├── missions/
│   ├── lunar.py
│   ├── mars.py
│   └── mission_profiles.py
│
├── landing/
│   ├── touchdown.py
│   ├── terrain.py
│   └── certification.py
│
└── advisor/
    └── spacecraft_advisor.py
```

---

# Knowledge Base Layer

Reference data separated from simulation code.

```text
knowledge/
│
├── apollo/
│   ├── apollo_lm.py
│   ├── apollo11.py
│   └── landing_data.py
│
├── reference_vehicles/
│
└── engineering_data/
```

---

# Why This Matters

## Today

```text
Spacecraft
   ↓
Engine
```

The engine model assumes it belongs to a spacecraft.

---

## Future

```text
Engineering Engine
        ↑
        │
 ┌──────┼───────┐
 │      │       │
 ▼      ▼       ▼

Spacecraft
Aircraft
Rover
```

The propulsion model becomes reusable.

---

# Recommendation

Split the architecture into three layers:

```text
Layer 1
-------
Engineering Platform
(Generic)

Layer 2
-------
Aerospace Domain
(Spacecraft specific)

Layer 3
-------
Reference Knowledge
(Apollo, lunar datasets, validation data)
```

A good litmus test:

> If a class can exist in a nuclear plant, aircraft simulator, rover simulator, ship designer, or spacecraft designer, it belongs in the Engineering Platform.

Examples:

```text
DataProvenance
MassProperties
Component
Placement
ThrottleSpec
IgnitionLimits
RuleEngine
Readiness
```

If it knows about:

```text
Orbit
Moon
Earth
TLI
Apollo
Landing Site
Lunar Gravity
```

it belongs in the Aerospace Domain or Knowledge Base.

# Future Development: Assembly, Attachments, and Gizmo Architecture

## Current State

The current assembly system supports:

```text
Parent-Child Attachments
Attachment Nodes
Offsets
Euler Rotations
Symmetry Groups
Automatic Stacking
```

through:

```text
placement.py
geometry.py
transforms.py
```

The placement model already contains the conceptual foundation:

```python
Placement
├── parent_id
├── parent_node
├── node
├── angle_deg
├── offset
├── rotation_deg
└── symmetry_group
```

However, attachment nodes currently exist primarily as logical constructs used during layout generation.

---

# Target Architecture

## Explicit Assembly System

Future development should evolve the placement system into a true assembly framework.

### Goals

```text
Visual Attachment Nodes
Interactive Gizmos
Snap-To-Node Behavior
Assembly Hierarchies
Symmetry Placement
Constraint Validation
```

---

# Assembly Architecture

## Assembly Graph

Current:

```text
Spacecraft
 └─ Components
```

Target:

```text
Spacecraft
    │
    ▼

AssemblyGraph

    Root
      │
      ├── Fuel Tank
      │     │
      │     ├── Engine
      │     ├── Landing Leg
      │     └── Landing Leg
      │
      ├── Payload
      │
      └── Solar Array
```

The assembly graph becomes the authoritative representation of vehicle structure.

---

# Attachment Node System

## Current Nodes

```text
top
bottom
side
mount
```

---

## Future Node Definition

Each component may expose multiple attachment points.

Example:

```python
AttachmentNode
{
    id
    name
    position
    normal
    category
    compatibility
}
```

Example:

```text
Fuel Tank

 ┌───────┐
 │       │
 │ Tank  │
 │       │
 └───────┘

   ▲
   │
 top node

   ▼
 bottom node

 ◄       ►
side nodes
```

---

## Node Categories

```text
Structural
Engine
Power
Payload
Landing Gear
RCS
Utility
```

Examples:

```text
Engine Mount

only accepts:

Engine
```

```text
Landing Gear Mount

only accepts:

LandingLeg
```

---

# Interactive Gizmo Architecture

## Purpose

Replace numeric positioning workflows with direct viewport manipulation.

---

## Translation Gizmo

Supports:

```text
Drag X
Drag Y
Drag Z
```

Operations:

```text
Move Component
Adjust Attachment Offset
```

---

## Rotation Gizmo

Supports:

```text
Pitch
Yaw
Roll
```

Operations:

```text
Rotate Component
Adjust Attachment Orientation
```

---

## Scale Gizmo

Future use for:

```text
Procedural Components
Visualization Parameters
```

but should not modify engineering dimensions unless explicitly allowed.

---

# Node Snapping

## Drag-and-Snap Workflow

Example:

```text
User drags engine

      ▼

Engine Mount Node Highlighted

      ▼

Compatible Parent Nodes Highlighted

      ▼

Snap Preview

      ▼

Attachment Created
```

---

## Validation Rules

The assembly system should validate:

```text
Type Compatibility
Node Compatibility
Cycles
Self References
Structural Integrity
```

Examples:

```text
Engine
  attached to
Engine

INVALID
```

```text
Landing Leg
  attached to
Tank Side Node

VALID
```

---

# Symmetry System

Current:

```python
symmetry_group
```

Future:

```text
2-way radial symmetry
3-way radial symmetry
4-way radial symmetry
6-way radial symmetry
8-way radial symmetry
Mirror symmetry
```

Examples:

```text
Add one landing leg

     ▼

Automatically create

4 landing legs
```

with shared editing.

---

# Visual Editing Framework

## Selection Layer

Supports:

```text
Single Selection
Multi-Selection
Hierarchy Selection
```

---

## Hover Layer

Visualizes:

```text
Attachment Nodes
Snap Targets
Parent Relationships
```

---

## Assembly Overlay

Displays:

```text
Parent Links
Attachment Nodes
Symmetry Groups
Alignment Guides
```

---

# Constraint System

Long-term architecture should introduce assembly constraints.

Examples:

```text
Attached
Aligned
Concentric
Radial
Fixed Offset
Fixed Rotation
```

This would replace purely positional editing.

---

# Future Assembly Workflow

## Current

```text
Create Part

    ▼

Enter Numbers

    ▼

Adjust XYZ

    ▼

Adjust Rotation
```

---

## Target

```text
Create Part

    ▼

Drag Into Scene

    ▼

Snap To Node

    ▼

Adjust With Gizmo

    ▼

Constraint Created

    ▼

Assembly Updated
```

---

# Architectural Refactoring Recommendation

Introduce a dedicated assembly subsystem:

```text
engineering/
│
├── assembly/
│   ├── attachment.py
│   ├── assembly_graph.py
│   ├── nodes.py
│   ├── constraints.py
│   └── symmetry.py
```

and separate viewport interactions into:

```text
viewport/
│
├── gizmos/
│   ├── translate_gizmo.py
│   ├── rotate_gizmo.py
│   ├── scale_gizmo.py
│   └── snapping.py
```

This separates:

```text
Engineering Assembly Logic
```

from:

```text
Viewport Editing Tools
```

which keeps the assembly system reusable for future renderers, editor frameworks, and simulation domains.

---

# Long-Term Vision

The placement system should evolve from:

```text
Position-Based Configuration
```

to:

```text
Constraint-Based Vehicle Assembly
```

where components are assembled through attachment nodes, validated through engineering constraints, manipulated using viewport gizmos, and represented internally as a structured assembly graph rather than a collection of independently positioned parts.
