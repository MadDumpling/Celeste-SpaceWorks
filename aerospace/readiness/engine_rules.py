from aerospace.components import Engine


def check_engine(report, engine: Engine):

    if engine.effective_exit_area() is None:
        report.add_gap(
            "blocking",
            engine.name,
            "exit area or sea-level thrust unknown",
        )

    if (
        engine.throttle.min_fraction is None
        or engine.throttle.max_fraction is None
    ):
        report.add_gap(
            "blocking",
            engine.name,
            "throttle range unknown",
        )

    elif (
        engine.throttle.is_throttleable
        and not engine.throttle.curve
    ):
        report.add_gap(
            "warning",
            engine.name,
            "no throttle curve; ideal throttle assumptions used",
        )

    if engine.ignition.max_ignitions is None:
        report.add_gap(
            "blocking",
            engine.name,
            "ignition/restart limit unknown",
        )

    if engine.gimbal.half_angle_deg is None:
        report.add_gap(
            "blocking",
            engine.name,
            "gimbal authority unknown",
        )

    elif (
        engine.gimbal.half_angle_deg > 0.0
        and engine.gimbal.rate_dps is None
    ):
        report.add_gap(
            "warning",
            engine.name,
            "gimbal rate unknown",
        )

    if engine.chamber_pressure_pa is None:
        report.add_gap(
            "warning",
            engine.name,
            "chamber pressure unknown",
        )

    if engine.ignition.min_impulse_ns is None:
        report.add_gap(
            "warning",
            engine.name,
            "minimum impulse unknown",
        )

    if (
        engine.ignition.tail_off_time_s is None
        or engine.ignition.tail_off_impulse_ns is None
    ):
        report.add_gap(
            "warning",
            engine.name,
            "shutdown tail-off behaviour unknown",
        )
