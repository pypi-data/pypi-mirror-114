from curvenote.latex.TaggedContentCollection import TaggedContentCollection


def test_init():
    c = TaggedContentCollection()
    assert list(c.keys()) == []

def test_add():
    c = TaggedContentCollection()

    c.add('a', 'b')
    assert c['a'] == 'b\n'

    c.add('a', 'c')
    assert c['a'] == 'b\n\nc\n'

def test_merge():
    c1 = TaggedContentCollection({'a': 'b\n', 'b': 'c\n'})
    c2 = TaggedContentCollection({'a': 'd\n', 'c': 'e\n'})

    c1.merge(c2)

    assert c1['a'] == 'b\n\nd\n'
    assert c1['b'] == 'c\n'
    assert c1['c'] == 'e\n'
