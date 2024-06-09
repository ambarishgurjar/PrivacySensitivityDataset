import os

import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal

import oddt
from oddt.interactions import (close_contacts,
                               hbonds,
                               distance,
                               halogenbonds,
                               halogenbond_acceptor_halogen,
                               pi_stacking,
                               salt_bridges,
                               pi_cation,
                               hydrophobic_contacts)

test_data_dir = os.path.dirname(os.path.abspath(__file__))

mols = list(oddt.toolkit.readfile('sdf', os.path.join(test_data_dir, 'data/dude/xiap/actives_docked.sdf')))
list(map(lambda x: x.addh(only_polar=True), mols))

rec = next(oddt.toolkit.readfile('pdb', os.path.join(test_data_dir, 'data/dude/xiap/receptor_rdkit.pdb')))
rec.protein = True
rec.addh(only_polar=True)


def test_close_contacts():
    """Close contacts test"""
    cc = [len(close_contacts(rec.atom_dict[rec.atom_dict['atomicnum'] != 1],
                             mol.atom_dict[mol.atom_dict['atomicnum'] != 1],
                             cutoff=3)[0]) for mol in mols]
    assert_array_equal(cc,
                       [5, 7, 6, 5, 3, 6, 5, 6, 6, 6, 5, 4, 7, 6, 6, 6, 7, 5,
                        6, 5, 5, 7, 4, 5, 6, 7, 6, 5, 7, 5, 6, 4, 5, 4, 3, 7,
                        6, 6, 3, 5, 4, 3, 1, 7, 3, 2, 4, 1, 2, 7, 4, 4, 6, 4,
                        6, 7, 7, 6, 6, 6, 5, 6, 5, 4, 4, 7, 3, 6, 6, 4, 7, 7,
                        4, 5, 4, 7, 3, 6, 6, 6, 5, 6, 4, 5, 4, 4, 6, 5, 5, 7,
                        6, 2, 6, 5, 1, 8, 6, 5, 7, 4])


def test_hbonds():
    """H-Bonds test"""
    hbonds_count = np.array([hbonds(rec, mol)[2].sum() for mol in mols])
    if oddt.toolkit.backend == 'ob':
        exp_count = [2, 5, 4, 4, 3, 4, 2, 3, 4, 3, 3, 3, 3, 3, 5, 4, 3, 5,
                     4, 5, 5, 3, 4, 6, 3, 4, 4, 4, 3, 3, 4, 3, 4, 3, 3, 3,
                     3, 3, 3, 4, 3, 4, 4, 3, 4, 3, 5, 4, 3, 3, 3, 6, 4, 2,
                     2, 3, 4, 4, 4, 4, 5, 2, 3, 4, 4, 3, 3, 3, 2, 5, 3, 4,
                     3, 3, 5, 2, 3, 2, 2, 3, 5, 3, 3, 2, 3, 4, 2, 4, 3, 3,
                     3, 5, 3, 4, 6, 4, 5, 3, 3, 2]
    else:
        exp_count = [2, 5, 4, 4, 3, 4, 2, 3, 4, 3, 3, 3, 3, 3, 5, 4, 3, 5,
                     4, 5, 5, 3, 4, 6, 3, 4, 4, 4, 3, 3, 4, 3, 4, 3, 3, 3,
                     3, 3, 3, 4, 3, 4, 4, 3, 4, 3, 5, 4, 3, 3, 3, 6, 4, 2,
                     2, 3, 4, 4, 4, 4, 5, 2, 3, 4, 4, 4, 3, 3, 2, 5, 3, 4,
                     3, 3, 5, 2, 3, 2, 2, 3, 5, 3, 3, 2, 3, 4, 2, 4, 3, 3,
                     3, 5, 3, 4, 6, 4, 5, 3, 3, 2]
    assert_array_equal(hbonds_count, exp_count)