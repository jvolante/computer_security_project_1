from unittest import TestCase
import monoalphabetic_cypher_tools


class TestCypher_decriptor(TestCase):
    def test_guess_initial_mappings(self):
        decryptor = monoalphabetic_cypher_tools.cypher_decriptor("shakespear_cal.txt")
        decryptor.guess_initial_mappings("test.txt")
        result = decryptor.decrypt()

    def test_swap_mapping(self):
        decryptor = monoalphabetic_cypher_tools.cypher_decriptor("shakespear_cal.txt")
        decryptor.set_mapping({'a':'b', 'c':'d', 'e':'f'})
        decryptor.swap_mapping('a', 'd')

        self.assertDictEqual(decryptor.get_mapping(), {'a':'d', 'c':'b', 'e':'f'})
