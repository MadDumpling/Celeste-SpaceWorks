from engineering.readiness.report import DefinitionReport
from engineering.readiness.provenance import check_provenance

from aerospace.components import Engine, FuelTank
from aerospace.mass_properties import mass_properties

from .engine_rules import check_engine


def assess_spacecraft_definition(spacecraft):

    report = DefinitionReport()

    check_provenance(
        report,
        spacecraft.name,
        spacecraft.provenance,
        "vehicle-level data",
    )

    _check_landing_gear(report, spacecraft)

    _check_attitude_limits(report, spacecraft)

    _check_mass_properties(report, spacecraft)

    _check_components(report, spacecraft)

    return report