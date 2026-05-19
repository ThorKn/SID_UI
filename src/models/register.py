from dataclasses import dataclass

@dataclass(frozen=True)
class RegisterDefinition:
    """
    Represents the static definition of a hardware register.
    """
    address: int
    name: str
    description: str
    group: str