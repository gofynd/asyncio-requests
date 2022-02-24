"""Request tracer for aiohttp."""
import aiohttp


def request_tracer():
    """Provide request tracing to aiohttp client sessions.

    Returns:
        trace_config (obj): An aiohttp.TraceConfig object.

    """
    trace_config = aiohttp.TraceConfig()
    trace_config.results_collector = {}

    async def on_request_start(session, context, params):
        context.on_request_start = session.loop.time()
        context.is_redirect = False
        trace_config.results_collector[
            'on_request_start'] = context.on_request_start
        trace_config.results_collector[
            'is_redirect'] = context.is_redirect

    async def on_connection_queued_start(session, context, params):
        context.on_connection_queued_start = \
            session.loop.time() - context.on_request_start
        trace_config.results_collector[
            'on_connection_queued_start'] = context.on_connection_queued_start

    async def on_connection_queued_end(session, context, params):
        context.on_connection_queued_end = \
            session.loop.time() - context.on_request_start
        trace_config.results_collector[
            'on_connection_queued_end'] = context.on_connection_queued_end

    async def on_connection_create_start(session, context, params):
        context.on_connection_create_start = \
            session.loop.time() - context.on_request_start
        trace_config.results_collector[
            'on_connection_create_start'] = context.on_connection_create_start

    async def on_request_redirect(session, context, params):
        context.on_request_redirect = \
            session.loop.time() - context.on_request_start
        context.is_redirect = True
        trace_config.results_collector[
            'on_request_redirect'] = context.on_request_redirect
        trace_config.results_collector[
            'is_redirect'] = context.is_redirect

    async def on_connection_reuseconn(session, context, params):
        context.on_request_start = \
            session.loop.time()
        trace_config.results_collector[
            'on_connection_reuseconn'] = context.on_request_start

    async def on_dns_cache_hit(session, context, params):
        context.on_dns_cache_hit = \
            session.loop.time() - context.on_request_start
        trace_config.results_collector[
            'on_dns_cache_hit'] = context.on_dns_cache_hit

    async def on_dns_cache_miss(session, context, params):
        context.on_dns_cache_miss = \
            session.loop.time() - context.on_request_start
        trace_config.results_collector[
            'on_dns_cache_miss'] = context.on_dns_cache_miss

    async def on_dns_resolvehost_start(session, context, params):
        context.on_dns_resolvehost_start = \
            session.loop.time() - context.on_request_start
        trace_config.results_collector[
            'on_dns_resolvehost_start'] = context.on_dns_resolvehost_start

    async def on_dns_resolvehost_end(session, context, params):
        context.on_dns_resolvehost_end = \
            session.loop.time() - context.on_request_start
        trace_config.results_collector[
            'on_dns_resolvehost_end'] = context.on_dns_resolvehost_end

    async def on_connection_create_end(session, context, params):
        context.on_connection_create_end = \
            session.loop.time() - context.on_request_start
        trace_config.results_collector[
            'on_connection_create_end'] = context.on_connection_create_end

    async def on_request_chunk_sent(session, context, params):
        context.on_request_chunk_sent = \
            session.loop.time() - context.on_request_start
        trace_config.results_collector[
            'on_request_chunk_sent'] = context.on_request_chunk_sent

    async def on_response_chunk_received(session, context, params):
        context.on_response_chunk_received = \
            session.loop.time() - context.on_request_start
        trace_config.results_collector[
            'on_response_chunk_received'] = context.on_response_chunk_received

    async def on_request_exception(session, context, params):
        context.on_request_exception = \
            session.loop.time() - context.on_request_start
        trace_config.results_collector[
            'on_request_exception'] = context.on_request_exception
        trace_config.results_collector[
            'on_request_exception_message'] = params.exception

    async def on_request_end(session, context, params):
        context.on_request_end = session.loop.time() - context.on_request_start
        trace_config.results_collector['on_request_end'] = \
            context.on_request_end

    trace_config.on_request_start.append(on_request_start)
    trace_config.on_connection_queued_start.append(on_connection_queued_start)
    trace_config.on_connection_queued_end.append(on_connection_queued_end)
    trace_config.on_connection_create_start.append(on_connection_create_start)
    trace_config.on_request_redirect.append(on_request_redirect)
    trace_config.on_connection_reuseconn.append(on_connection_reuseconn)
    trace_config.on_dns_cache_hit.append(on_dns_cache_hit)
    trace_config.on_dns_cache_miss.append(on_dns_cache_miss)
    trace_config.on_dns_resolvehost_start.append(on_dns_resolvehost_start)
    trace_config.on_dns_resolvehost_end.append(on_dns_resolvehost_end)
    trace_config.on_connection_create_end.append(on_connection_create_end)
    trace_config.on_request_chunk_sent.append(on_request_chunk_sent)
    trace_config.on_response_chunk_received.append(on_response_chunk_received)
    trace_config.on_request_exception.append(on_request_exception)
    trace_config.on_request_end.append(on_request_end)

    return trace_config
