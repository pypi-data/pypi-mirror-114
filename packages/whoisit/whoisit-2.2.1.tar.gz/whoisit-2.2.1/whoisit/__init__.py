from .bootstrap import Bootstrap
from .query import QueryBuilder, Query
from .parser import parse
from .logger import get_logger


version = '2.2.1'


# Expose class methods as the public API


_bootstrap = Bootstrap()
is_bootstrapped = _bootstrap.is_bootstrapped
clear_bootstrapping = _bootstrap.clear_bootstrapping
bootstrap = _bootstrap.bootstrap
save_bootstrap_data = _bootstrap.save_bootstrap_data
load_bootstrap_data = _bootstrap.load_bootstrap_data
bootstrap_is_older_than = _bootstrap.bootstrap_is_older_than


_query_builder = QueryBuilder(_bootstrap)
build_query = _query_builder.build


# Query helpers


def asn(as_number, rir=None, raw=False, allow_insecure_ssl=False):
    method, url, exact_match = build_query(
        query_type='asn', query_value=as_number, rir=rir)
    q = Query(method, url, allow_insecure_ssl)
    response = q.request()
    return response if raw else parse(_bootstrap, 'autnum', response)


def domain(domain_name, raw=False, allow_insecure_ssl=False):
    method, url, exact_match = build_query(
        query_type='domain', query_value=domain_name)
    q = Query(method, url, allow_insecure_ssl)
    response = q.request()
    return response if raw else parse(_bootstrap, 'domain', response)


def ip(ip_address_or_network, rir=None, raw=False, allow_insecure_ssl=False):
    method, url, exact_match = build_query(
        query_type='ip', query_value=ip_address_or_network, rir=rir)
    q = Query(method, url, allow_insecure_ssl)
    response = q.request()
    return response if raw else parse(_bootstrap, 'ip', response)


def entity(entity_handle, rir=None, raw=False, allow_insecure_ssl=False):
    method, url, exact_match = build_query(
        query_type='entity', query_value=entity_handle, rir=rir)
    q = Query(method, url, allow_insecure_ssl)
    response = q.request()
    return response if raw else parse(_bootstrap, 'entity', response)
