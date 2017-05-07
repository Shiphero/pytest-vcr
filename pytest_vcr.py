# -*- coding: utf-8 -*-
import os
import pytest
from vcr import VCR


def pytest_addoption(parser):
    group = parser.getgroup('vcr')
    group.addoption(
        '--vcr-record-mode',
        action='store',
        dest='vcr_record_mode',
        default=None,
        choices=['once', 'new_episodes', 'none', 'all'],
        help='Set the recording mode for VCR.py.'
    )


@pytest.fixture(autouse=True)
def _vcr_marker(request):
    marker = request.node.get_marker('vcr')
    if marker:
        request.getfixturevalue('vcr_cassette')


@pytest.yield_fixture
def vcr_cassette(request, vcr_config, vcr_cassette_path):
    """Wrap a test in a VCR.py cassette"""
    vcr = VCR(
        path_transformer=VCR.ensure_suffix(".yaml"),
        **vcr_config)
    with vcr.use_cassette(vcr_cassette_path) as cassette:
        yield cassette


@pytest.fixture
def vcr_cassette_name(request):
    """Name of the VCR cassette"""
    f = request.function
    if hasattr(f, '__self__'):
        return f.__self__.__class__.__name__ + '.' + f.__name__
    return f.__name__


@pytest.fixture
def vcr_cassette_path(request, vcr_cassette_name):
    test_dir = request.node.fspath.dirname
    return os.path.join(test_dir, '_cassettes', vcr_cassette_name)


@pytest.fixture
def vcr_config():
    """Custom configuration for VCR.py"""
    return {}
