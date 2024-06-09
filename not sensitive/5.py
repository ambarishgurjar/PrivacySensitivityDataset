def test_scorer():
    np.random.seed(42)

    mols = list(oddt.toolkit.readfile('sdf', actives_sdf))

    values = [0]*5 + [1]*5
    test_values = [0, 0, 1, 1, 0]

    if oddt.toolkit.backend == 'ob':
        fp = 'fp2'
    else:
        fp = 'rdkit'

    simple_scorer = scorer(neuralnetwork(), fingerprints(fp))
    simple_scorer.fit(mols[:10], values)
    predictions = simple_scorer.predict(mols[10:15])
    assert_array_almost_equal(predictions, [0, 1, 0, 1, 0])

    score = simple_scorer.score(mols[10:15], test_values)
    assert_almost_equal(score, 0.6)

    scored_mols = [simple_scorer.predict_ligand(mol) for mol in mols[10:15]]
    single_predictions = [float(mol.data['score']) for mol in scored_mols]
    assert_array_almost_equal(predictions, single_predictions)

    scored_mols_gen = simple_scorer.predict_ligands(mols[10:15])
    assert isinstance(scored_mols_gen, GeneratorType)
    gen_predictions = [float(mol.data['score']) for mol in scored_mols_gen]
    assert_array_almost_equal(predictions, gen_predictions)


def test_ensemble_descriptor():
    mols = list(oddt.toolkit.readfile('sdf', actives_sdf))[:10]
    list(map(lambda x: x.addh(), mols))

    rec = next(oddt.toolkit.readfile('pdb', receptor_pdb))
    rec.protein = True
    rec.addh()

    desc1 = rfscore(version=1).descriptor_generator
    desc2 = oddt_vina_descriptor()
    ensemble = ensemble_descriptor((desc1, desc2))

    ensemble.set_protein(rec)
    assert len(ensemble) == len(desc1) + len(desc2)

    # set protein
    assert desc1.protein == rec
    assert desc2.protein == rec

    ensemble_scores = ensemble.build(mols)
    scores1 = desc1.build(mols)
    scores2 = desc2.build(mols)
    assert_array_almost_equal(ensemble_scores, np.hstack((scores1, scores2)))