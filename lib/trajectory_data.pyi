"""Type stubs for Booster SDK trajectory data types."""

from typing import List


class JointState:
    """State of a single joint."""

    name: str
    position: float | None
    velocity: float | None
    effort: float | None
    extras: dict[str,Any] | None

    def __init__(
        self,
		name: str = ...
        position: float|None = ...,
        velocity: float|None = ...,
        effort: float|None = ...,
        extras: dict[str,Any] | None = ...,
    ) -> None: ...


class JointTrajectoryPoint:
    """A single point in a joint trajectory."""

    time_from_start: float
	joints: list[JointState]

    def __init__(
        self,
        time_from_start: float = ...,
        joints: list[JointState] = ...
    ) -> None: ...


class TrajectoryMeta:
    """Metadata for a trajectory."""

    joint_names: List[str]
    duration: float

    def __init__(
        self,
        joint_names: List[str] = ...,
        duration: float = ...,
    ) -> None: ...


class TrajectoryData:
    """A complete trajectory for robot execution."""

    meta: TrajectoryMeta
    points: List[JointTrajectoryPoint]

    def __init__(
        self,
        meta: TrajectoryMeta = ...,
        points: List[JointTrajectoryPoint] = ...,
    ) -> None: ...
