#%%
import unittest
import deloqv as dlq
from deloqv import Algorithme
from deloqv import MAP


#%%
# %%

class SimpleTest(unittest.TestCase):
    def test_nb_de_gare_sur_trajet(self):
        self.assertAlmostEqual(Algorithme.nb_de_gare_sur_trajet(3,35), 19)

    def test_chemin_moins_cher(self):
        self.AssertionError(Algorithme.chemin_moins_cher(3,15,3))

    def test_map(self):
        self.AssertionError(MAP.map)


# %%
