import sys
from typing import Any, Collection, ContextManager, Mapping, Optional, TypeVar

if sys.version_info < (3, 8):
    from typing_extensions import Protocol
else:
    from typing import Protocol

from di._utils.types import FusedContextManager
from di.api.dependencies import DependantBase, DependencyType
from di.api.providers import DependencyProvider, DependencyProviderType
from di.api.scopes import Scope
from di.api.solved import SolvedDependant

ContainerType = TypeVar("ContainerType")


class ContainerProtocol(Protocol):
    @property
    def scopes(self) -> Collection[Scope]:
        ...

    def bind(
        self,
        provider: DependantBase[DependencyType],
        dependency: DependencyProviderType[DependencyType],
    ) -> ContextManager[None]:
        """Bind a new dependency provider for a given dependency.

        This can be used as a function (for a permanent bind, cleared when `scope` is exited)
        or as a context manager (the bind will be cleared when the context manager exits).

        Binds are only identified by the identity of the callable and do not take into account
        the scope or any other data from the dependency they are replacing.
        """
        ...

    def solve(
        self,
        dependency: DependantBase[DependencyType],
    ) -> SolvedDependant[DependencyType]:
        """Solve a dependency.

        Returns a SolvedDependant that can be executed to get the dependency's value.
        """
        ...

    def enter_scope(
        self: ContainerType, scope: Scope
    ) -> FusedContextManager[ContainerType]:
        """Enter a scope and get back a new BaseContainer in that scope"""
        ...

    def execute_sync(
        self,
        solved: SolvedDependant[DependencyType],
        *,
        values: Optional[Mapping[DependencyProvider, Any]] = None,
    ) -> DependencyType:
        """Execute an already solved dependency.

        This method is synchronous and uses a synchronous executor,
        but the executor may still be able to execute async dependencies.
        """
        ...

    async def execute_async(
        self,
        solved: SolvedDependant[DependencyType],
        *,
        values: Optional[Mapping[DependencyProvider, Any]] = None,
    ) -> DependencyType:
        """Execute an already solved dependency."""
        ...
