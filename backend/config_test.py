from backend.config import Config


def test_config_load(tmpdir):
    tmp = tmpdir.mkdir('test').join('config.yaml')
    with open(tmp, 'w') as f:
        f.write("""
backend:
  storage: /tmp/data.json
  endpoint: 127.0.0.1:5000
  
providers:
  github_pulls: username/repo
""")

    cfg = Config(tmp)
    assert cfg.backend_endpoint == '127.0.0.1:5000'
    assert cfg.storage_path == '/tmp/data.json'
    assert cfg.github_repo_path == 'https://api.github.com/repos/username/repo/pulls'
