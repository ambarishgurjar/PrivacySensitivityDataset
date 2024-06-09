def test_basic_conversion():
    f = 100
    i = AnnoyIndex(f, "hamming")
    u = numpy.random.binomial(1, 0.5, f)
    v = numpy.random.binomial(1, 0.5, f)
    i.add_item(0, u)
    i.add_item(1, v)
    u2 = i.get_item_vector(0)
    v2 = i.get_item_vector(1)
    assert numpy.dot(u - u2, u - u2) == pytest.approx(0.0)
    assert numpy.dot(v - v2, v - v2) == pytest.approx(0.0)
    assert i.get_distance(0, 0) == pytest.approx(0.0)
    assert i.get_distance(1, 1) == pytest.approx(0.0)
    assert i.get_distance(0, 1) == pytest.approx(numpy.dot(u - v, u - v))
    assert i.get_distance(1, 0) == pytest.approx(numpy.dot(u - v, u - v))


def test_basic_nns():
    f = 100
    i = AnnoyIndex(f, "hamming")
    u = numpy.random.binomial(1, 0.5, f)
    v = numpy.random.binomial(1, 0.5, f)
    i.add_item(0, u)
    i.add_item(1, v)
    i.build(10)
    assert i.get_nns_by_item(0, 99) == [0, 1]
    assert i.get_nns_by_item(1, 99) == [1, 0]
    rs, ds = i.get_nns_by_item(0, 99, include_distances=True)
    assert rs == [0, 1]
    assert ds[0] == pytest.approx(0)
    assert ds[1] == pytest.approx(numpy.dot(u - v, u - v))


def test_save_load():
    f = 100
    i = AnnoyIndex(f, "hamming")
    u = numpy.random.binomial(1, 0.5, f)
    v = numpy.random.binomial(1, 0.5, f)
    i.add_item(0, u)
    i.add_item(1, v)
    i.build(10)
    i.save("blah.ann")
    j = AnnoyIndex(f, "hamming")
    j.load("blah.ann")
    rs, ds = j.get_nns_by_item(0, 99, include_distances=True)
    assert rs == [0, 1]
    assert ds[0] == pytest.approx(0)
    assert ds[1] == pytest.approx(numpy.dot(u - v, u - v))