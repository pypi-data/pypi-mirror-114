"""A package for using complex numbers as 2D vectors."""

__all__ = ["Vector", "angle"]

try:
    from .cvectors import Vector, angle
except ImportError:
    from ._cvectors import Vector, angle
