"""Circuit breaker helper."""

from datetime import timedelta
from typing import Any, Callable, List, Optional

from asyncio_requests.utils.constants import (CIRCUIT_BREAKER_DELAY,
                                              CIRCUIT_BREAKER_MAX_DELAY,
                                              CIRCUIT_BREAKER_RETRY,
                                              CIRCUIT_BREAKER_TIMEOUT)
from failsafe import Backoff, CircuitBreaker, Delay, Failsafe, RetryPolicy


class CircuitBreakerHelper(object):
    """Helper for using pyfailsafe's circuit breaker."""

    def __init__(self, *args, **kwargs):
        """Initializer for CircuitBreakerHelper."""
        retries = kwargs.get('maximum_failures', None) or CIRCUIT_BREAKER_RETRY
        timeout = kwargs.get('timeout') or CIRCUIT_BREAKER_TIMEOUT

        # circuit breaker
        self.circuit_breaker = CircuitBreaker(
            maximum_failures=retries,
            reset_timeout_seconds=timeout)

        # retry policy
        retry_policy = kwargs.get('retry_policy')

        self.failsafe = Failsafe(
            circuit_breaker=self.circuit_breaker,
            retry_policy=retry_policy)

    @staticmethod
    async def get_retry_policy(
            name: Optional[str],
            **kwargs: Any) -> Optional[RetryPolicy]:
        """Get retry policy."""
        allowed_retries = kwargs['allowed_retries']
        retriable_exceptions: List[Callable] = kwargs.get(
            'retriable_exceptions', None)
        abortable_exceptions: List[Callable] = kwargs.get(
            'abortable_exceptions', None)
        on_retries_exhausted: Callable = kwargs.get(
            'on_retries_exhausted', None)
        on_failed_attempt: Callable = kwargs.get(
            'on_failed_attempt', None)
        on_abort: Callable = kwargs.get('on_abort', None)

        delay = kwargs['delay'] if \
            isinstance(kwargs.get('delay'), int) else \
            CIRCUIT_BREAKER_DELAY
        if name == 'backoff':

            max_delay: int = kwargs['max_delay'] if \
                isinstance(kwargs.get('max_delay'), int) else \
                CIRCUIT_BREAKER_MAX_DELAY
            jitter: bool = kwargs.get('jitter', False)
            backoff = Backoff(
                delay=timedelta(seconds=delay),
                max_delay=timedelta(seconds=max_delay),
                jitter=jitter)

        else:
            backoff = Delay(timedelta(seconds=delay))

        return RetryPolicy(allowed_retries=allowed_retries,
                           backoff=backoff,
                           retriable_exceptions=retriable_exceptions,
                           abortable_exceptions=abortable_exceptions,
                           on_retries_exhausted=on_retries_exhausted,
                           on_failed_attempt=on_failed_attempt,
                           on_abort=on_abort
                           )
