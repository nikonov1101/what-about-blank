from providers.storage import Storage


def test_storage(tmpdir):
    tmp = tmpdir.mkdir('test').join('data.json')
    print(tmp)

    s = Storage(tmp)
    data = s.load_all()

    # empty storage must have no keys in it
    assert len(data) == 0

    # empty storage must return None
    # for any key
    v = s.load_key('foo')
    assert v is None

    s.save_key('bar', {'data': 'hello'})
    s.save_key('baz', {'user': 'name'})

    all = s.load_all()
    assert 'bar' in all
    assert 'data' in all['bar']
    assert all['bar']['data'] == 'hello'

    assert 'baz' in all
    assert 'user' in all['baz']
    assert all['baz']['user'] == 'name'
