from __future__ import annotations

import abc
from typing import Literal, Protocol, NamedTuple, Tuple, Union, Set, Final

BaseVariableType = Literal['bounded', '1hot', '2vec', 'gaussian']


class BaseVariable(Protocol):
    @property
    @abc.abstractmethod
    def type(self) -> BaseVariableType: ...


class Bounded(NamedTuple):
    max: float
    min: float
    type: BaseVariableType = 'bounded'


class OneHot(NamedTuple):
    n_category: int
    type: BaseVariableType = '1hot'


class CatVec(NamedTuple):
    n_category: int
    n_embedding: int
    type: BaseVariableType = '2vec'


class Gaussian(NamedTuple):
    mean: float = 0
    var: float = 1
    type: BaseVariableType = 'gaussian'


class VariableTensor(NamedTuple):
    type: BaseVariable
    dim: Tuple[int, ...]
    positioned: bool = True


class VariablePort(Protocol):
    @property
    @abc.abstractmethod
    def name(self) -> str: ...

    @property
    @abc.abstractmethod
    def variables(self) -> Set[Union[VariableTensor, VariablePort]]: ...


class VariableGroup:
    """
    Because mypy does not support recursive types
    """

    def __init__(self, name: str, variables: Set[Union[VariableTensor, VariablePort]]):
        self.name: Final[str] = name
        self._variables = variables

    @property
    def variables(self) -> Set[Union[VariableTensor, VariablePort]]:
        return self._variables


def named_variable(name: str, variable: VariableTensor):
    return VariableGroup(name, variables={variable})


def named_variables(name: str, variables: Set[Union[VariableTensor, VariablePort]]):
    return VariableGroup(name, variables=variables)


def fmt_var_group(g: VariablePort, indent: int = 0) -> str:
    s = ""
    s += f"{g.name}\n" + (indent * " ") + "{"
    indent += len(s)
    for var in g.variables:
        if isinstance(var, tuple):
            s += f"{var}, "
        else:
            s += fmt_var_group(var, indent)
    s += "}\n"
    return s
