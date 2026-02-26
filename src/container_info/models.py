from dataclasses import dataclass, field


@dataclass
class ContainerInfo:
    is_container: bool
    container_id: str | None = None
    container_type_description: str | None = None
    container_type: list[str] = field(default_factory=list)

    @property
    def is_osg(self) -> bool:
        return bool(self.container_id and "osg" in self.container_id.lower())
