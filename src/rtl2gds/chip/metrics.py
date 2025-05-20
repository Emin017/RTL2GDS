"""@TODO"""

from dataclasses import asdict, dataclass, field

import yaml


@dataclass
class TimingMetrics:
    main_freq_mhz: float = 0.0
    critical_path: list[str] = field(default_factory=list)
    longest_logic_level: int = 0
    wns: float = 0.0
    tns: float = 0.0

@dataclass
class PowerMetrics:
    total: float = 0.0
    leakage: float = 0.0
    switch: float = 0.0
    internal: float = 0.0

@dataclass
class AreaMetrics:
    core: float = 0.0
    die: float = 0.0
    cell: float = 0.0
    core_util: float = 0.0
    die_util: float = 0.0

@dataclass
class DesignMetrics:
    """Store and manipulate design PPA (Power, Performance, Area) metrics"""
    # Technology info
    tech: str = "skywater130"

    # Design statistics
    # wirelength: float = 0
    num_instances: int = 0
    # num_seq_cells: int = 0
    # num_comb_cells: int = 0
    # num_instances: int = 0
    # num_equivalent_gates: int = 0

    # Detailed metrics
    performance: TimingMetrics = field(default_factory=TimingMetrics)
    power: PowerMetrics = field(default_factory=PowerMetrics)
    area: AreaMetrics = field(default_factory=AreaMetrics)

    # Signoff violations (0 means no violations)
    drc: int = 0
    lvs: int = 0
    sta: int = 0

    def to_dict(self) -> dict[str, object]:
        """Convert metrics to a flat dictionary structure."""
        metrics_dict = asdict(self)
        # Flatten nested dataclasses
        metrics_dict.update(metrics_dict.pop('performance'))
        metrics_dict.update(metrics_dict.pop('power'))
        metrics_dict.update({f"area_{k}": v for k, v in metrics_dict.pop('area').items()})
        return metrics_dict

    def to_yaml(self, pretty: bool = True) -> str:
        """
        Convert metrics to YAML format.

        Args:
            pretty (bool): If True, use pretty formatting with comments. Defaults to True.

        Returns:
            str: YAML formatted string of metrics
        """
        metrics_dict = self.to_dict()

        if not pretty:
            return yaml.dump(metrics_dict)

        # Group metrics for pretty printing
        sections = {
            "Technology Info": ["tech"],
            "Design Statistics": ["instance", "wirelength", "stdcell"],
            "Performance Metrics": ["main_freq_mhz", "critical_path", "longest_logic_level"],
            "Power Metrics": ["total", "leakage", "switch", "internal"],
            "Area Metrics": ["area_die", "area_core", "area_core_value", "area_stdcell", "area_utilization"],
            "Signoff Status": ["drc", "lvs", "sta"]
        }

        yaml_str = []
        for section, keys in sections.items():
            yaml_str.append(f"# {section}")
            section_dict = {k: metrics_dict[k] for k in keys if k in metrics_dict}
            yaml_str.append(yaml.dump(section_dict, sort_keys=False))

        return "\n".join(yaml_str)

    def print(self) -> None:
        print(self.to_dict())

@dataclass
class EDAMetrics:
    """Store and manipulate EDA tool metrics"""
    tool: str = ""
    version: str = ""
