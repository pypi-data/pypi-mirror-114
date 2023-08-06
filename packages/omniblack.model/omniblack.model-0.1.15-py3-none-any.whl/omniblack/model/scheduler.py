from math import inf
from sys import exc_info, excepthook
from typing import Optional

from anyio import maybe_async
from public import public
from rx.core import typing
from rx.disposable import (
    CompositeDisposable,
    Disposable,
    SingleAssignmentDisposable,
)
from rx.scheduler import periodicscheduler
from trio import CancelScope, open_memory_channel, open_nursery
from trio.lowlevel import spawn_system_task


@public
class TrioScheduler(periodicscheduler.PeriodicScheduler):
    def __init__(self, *args, exception_handler=excepthook, **kwargs):
        super().__init__(*args, **kwargs)
        self.exception_handler = exception_handler
        (send_channel, receive_channel) = open_memory_channel(inf)
        self.send_channel = send_channel
        self.receive_channel = receive_channel
        self.background_scope = CancelScope()
        self.background_task = spawn_system_task(self.__task_runner)

    def __del__(self):
        self.background_scope.cancel()
        self.send_channel.close()
        self.receive_channel.close()

    async def __run_task(
        self,
        func,
        cancel_scope: CancelScope,
        args,
        kwargs,
    ):
        with cancel_scope:
            try:
                return await maybe_async(func(*args, **kwargs))
            except BaseException:
                self.exception_handler(*exc_info())

    async def __task_runner(self):
        with self.background_scope:
            async with open_nursery() as nursery:
                self.task_group = nursery
                async for task in self.receive_channel:
                    self.task_group.start_soon(*task)

    def schedule(
        self,
        action: typing.ScheduledAction,
        state: Optional[typing.TState] = None,
    ) -> typing.Disposable:
        """
        Schedules an action to be executed.

        Args:
            action: Action to be executed.
            state: [Optional sate to be given to the scheduled action.

        Returns:
            The disposable object used to cancel the scheduled action
            (best effort).
        """
        sad = SingleAssignmentDisposable()

        def run() -> None:
            sad.disposable = self.invoke_action(action, state=state)

        cancel_scope = CancelScope()
        self.send_channel.send_nowait((run, cancel_scope, tuple(), {}))

        def dispose() -> None:
            cancel_scope.cancel()

        return CompositeDisposable(sad, Disposable(dispose))
