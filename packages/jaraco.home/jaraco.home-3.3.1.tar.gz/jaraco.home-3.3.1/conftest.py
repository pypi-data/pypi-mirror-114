import pytest
from mockproc import mockprocess


collect_ignore = [
    'jaraco/home/relay.py',
]


@pytest.fixture(scope='session', autouse=True)
def hdhomerun_config_mocked():
    # todo: should be jaraco.home.homerun, but for pytest bug
    import home.hdhomerun as hd

    hd.hdhomerun_config = 'hdhomerun_config'
    scripts = mockprocess.MockProc()
    scripts.append('hdhomerun_config', returncode=0, stdout="ch=none ss=80\n")
    with scripts:
        yield
