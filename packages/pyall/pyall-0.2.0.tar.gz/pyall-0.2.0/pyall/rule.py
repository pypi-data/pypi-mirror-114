from __future__ import annotations

import ast
import functools
from dataclasses import dataclass
from typing import Callable, ClassVar, Iterator, NamedTuple, cast

from pyall import constants as C
from pyall.relate import first_occurrence

__all__ = ["Rule"]


class InvalidRuleFunctionError(BaseException):  # pyall: not-public
    ...


class _DefineRule(NamedTuple):
    nodes: tuple[ast.AST, ...]
    function: Callable[[ast.AST], bool]


@dataclass
class Rule:
    rules: ClassVar[list[_DefineRule]] = []

    @classmethod
    def register(cls, nodes: tuple[ast.AST, ...]) -> C.Function:
        def f(function: C.Function) -> None:
            cls.validate_rule(function)
            cls.rules.append(_DefineRule(nodes=nodes, function=function))

        return cast(C.Function, f)

    @classmethod
    def filter_by_node(
        cls, node: tuple[ast.AST, ...]
    ) -> Iterator[Callable[[ast.AST], bool]]:
        for rule in cls.rules:
            if isinstance(node, rule.nodes):  # type: ignore
                yield rule.function  # type: ignore

    @classmethod
    def apply(cls, func: C.Function) -> C.Function:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> None:
            obj = args[0]
            node = args[1]

            check_rules = all(rule(node) for rule in cls.filter_by_node(node))
            if check_rules:
                func(*args, **kwargs)
            else:
                obj.generic_visit(node)

        return cast(C.Function, wrapper)

    @classmethod
    def validate_rule(cls, function: Callable[[ast.AST], bool]) -> bool:
        if not function.__name__.startswith("_rule_"):
            raise InvalidRuleFunctionError(
                "Rule function name must start with '_rule_'."
            )
        elif not function.__code__.co_argcount == 1:
            raise InvalidRuleFunctionError(
                "Rule function only gets one argument."
            )
        elif not function.__code__.co_varnames[0] == "node":
            raise InvalidRuleFunctionError(
                "The parameter name must be 'node'."
            )
        else:
            return True


def _rule_node_add(node) -> bool:
    return node.add is True if hasattr(node, "add") else False


@Rule.register(  # type: ignore
    (  # type: ignore
        ast.ClassDef,
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.Name,
    )
)
def _rule_node_skip(node) -> bool:
    return node.skip is False


@Rule.register(  # type: ignore
    (  # type: ignore
        ast.ClassDef,
        ast.FunctionDef,
        ast.AsyncFunctionDef,
        ast.Name,
    )
)
def _rule_parent_not_def(node) -> bool:
    return not first_occurrence(
        node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
    )


@Rule.register(  # type: ignore
    (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)  # type: ignore
)
def _rule_underscore_name(node) -> bool:
    is_underscore = node.name.startswith("_")
    is_add = _rule_node_add(node)

    return not is_underscore or is_add


@Rule.register((ast.Name,))  # type: ignore
def _rule_name_name(node) -> bool:
    is_upper = node.id.isupper()
    is_underscore = node.id.startswith("_")
    is_add = _rule_node_add(node)

    return (is_upper and not is_underscore) or is_add


@Rule.register((ast.Name,))  # type: ignore
def _rule_name_ctx(node) -> bool:
    return isinstance(node.ctx, ast.Store) or _rule_node_add(node)


@Rule.register((ast.Assign,))  # type: ignore
def _rule_node_is_all(node) -> bool:
    return getattr(node.targets[0], "id", None) == "__all__" and isinstance(
        node.value, (ast.List, ast.Tuple, ast.Set)
    )


@Rule.register((ast.Expr,))  # type: ignore
def _rule_node_is_all_item(node) -> bool:
    return (
        isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Attribute)
        and isinstance(node.value.func.value, ast.Name)
        and node.value.func.value.id == "__all__"
    )
