import os


def pytest_generate_tests(metafunc):
    os.environ['PYTEST'] = 'True'


pytest_plugins = [
    'tests.fixtures.fixture_user',
]
