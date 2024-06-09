def test_threads():
    n, f = 10000, 10
    i = AnnoyIndex(f, "euclidean")
    for j in range(n):
        i.add_item(j, numpy.random.normal(size=f))
    i.build(10)

    pool = multiprocessing.pool.ThreadPool()

    def query_f(j):
        i.get_nns_by_item(1, 1000)

    pool.map(query_f, range(n))