from dataclasses import dataclass, field


@dataclass(frozen=True)
class DataGap:
    severity: str
    subject: str
    message: str


@dataclass
class DefinitionReport:
    gaps: list[DataGap] = field(default_factory=list)
    illustrative_parts: list[str] = field(default_factory=list)
    untraceable_parts: list[str] = field(default_factory=list)

    @property
    def blocking(self) -> list[DataGap]:
        return [gap for gap in self.gaps if gap.severity == "blocking"]

    @property
    def high_confidence(self) -> bool:
        return not self.blocking and not self.untraceable_parts

    @property
    def label(self) -> str:
        if self.high_confidence:
            return "TRACEABLE DATA — no blocking gaps"
        return "PROTOTYPE DATA — not valid for engineering claims"

    def add_gap(self, severity: str, subject: str, message: str):
        self.gaps.append(DataGap(severity, subject, message))

    def summary(self) -> str:
        lines = [
            self.label,
            f"{len(self.blocking)} blocking gap(s), "
            f"{len(self.gaps) - len(self.blocking)} warning(s)",
        ]
        lines.extend(
            f"[{gap.severity.upper()}] {gap.subject}: {gap.message}"
            for gap in self.gaps
        )
        return "\n".join(lines)