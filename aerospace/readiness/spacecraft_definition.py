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

    check_landing_gear(report, spacecraft)

    check_attitude_limits(report, spacecraft)

    check_mass_properties(report, spacecraft)

    check_components(report, spacecraft)

    return report