import ipaddress
import itertools
import random

import pytest

import randog.factory
from randog.exceptions import FactoryConstructionError


def test__random_ipv4():
    factory = randog.factory.randipv4()

    value = factory.next()

    assert isinstance(value, ipaddress.IPv4Address)


@pytest.mark.parametrize(
    ("network", "expected_values"),
    [
        ("192.168.0.3/32", ["192.168.0.3"]),
        ("192.168.0.2/31", ["192.168.0.2", "192.168.0.3"]),
        ("192.168.0.0/30", ["192.168.0.1", "192.168.0.2"]),
    ],
)
def test__random_ipv4__with_network(network, expected_values):
    factory = randog.factory.randipv4(ipaddress.ip_network(network))

    values = set(factory.iter(200))

    assert values == set(ipaddress.ip_address(a) for a in expected_values)


def test__random_ipv4_with_network_exclude():
    n1 = ipaddress.ip_network("192.0.2.0/28")
    n2 = ipaddress.ip_network("192.0.2.1/32")
    networks = list(n1.address_exclude(n2))
    expected_values = set(itertools.chain(*(n.hosts() for n in networks)))

    factory = randog.factory.randipv4(networks)

    values = set(factory.iter(200))

    assert values <= expected_values


@pytest.mark.parametrize(
    ("network", "expected_values"),
    [
        ("192.168.0.3/32", ["192.168.0.3"]),
        ("192.168.0.2/31", ["192.168.0.2", "192.168.0.3"]),
        ("192.168.0.0/30", ["192.168.0.1", "192.168.0.2"]),
    ],
)
def test__random_ipv4__or_none(network, expected_values):
    factory = randog.factory.randipv4(ipaddress.ip_network(network)).or_none(0.5)

    values = set(factory.iter(200))

    assert values == {None, *(ipaddress.ip_address(a) for a in expected_values)}


@pytest.mark.parametrize(
    ("network", "expected_values"),
    [
        ("192.168.0.3/32", ["192.168.0.3"]),
        ("192.168.0.2/31", ["192.168.0.2", "192.168.0.3"]),
        ("192.168.0.0/30", ["192.168.0.1", "192.168.0.2"]),
    ],
)
def test__random_ipv4__or_none_0(network, expected_values):
    factory = randog.factory.randipv4(ipaddress.ip_network(network)).or_none(0)

    values = set(factory.iter(200))

    assert values == set(ipaddress.ip_address(a) for a in expected_values)


def test__random_int_error_with_empty_network():
    with pytest.raises(FactoryConstructionError) as e_ctx:
        randog.factory.randipv4([])
    e = e_ctx.value

    assert e.message == "empty address space for randipv4"


@pytest.mark.parametrize(
    ("rnd1", "rnd2", "expect_same_output"),
    [
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(12)}, True),
        (lambda: {"rnd": random.Random(12)}, lambda: {"rnd": random.Random(13)}, False),
        (lambda: {"rnd": random.Random(12)}, lambda: {}, False),
        (lambda: {}, lambda: {}, False),
    ],
)
@pytest.mark.parametrize(
    ("network",),
    [
        ("192.168.0.2/31",),
        ("192.168.0.0/30",),
    ],
)
def test__random_ipv4__seed(rnd1, rnd2, expect_same_output, network):
    repeat = 20
    factory1 = randog.factory.randipv4(ipaddress.ip_network(network), **rnd1())
    factory2 = randog.factory.randipv4(ipaddress.ip_network(network), **rnd2())

    generated1 = list(factory1.iter(repeat))
    generated2 = list(factory2.iter(repeat))

    if expect_same_output:
        assert generated1 == generated2
    else:
        assert generated1 != generated2
