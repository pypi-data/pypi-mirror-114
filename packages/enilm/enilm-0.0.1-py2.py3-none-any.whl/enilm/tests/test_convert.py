from unittest import TestCase
import enilm


class TestConvert(TestCase):
    def test_convert(self):
        self.assertEqual(
            enilm.convert.size(1, enilm.constants.MemUnit.GiB, enilm.constants.MemUnit.B),
            1024 ** 3,
        )

        self.assertEqual(
            enilm.convert.size(1, enilm.convert.MemUnit.KiB, enilm.constants.MemUnit.KB),
            1.024,
        )

        self.assertAlmostEqual(
            enilm.convert.size(1234, enilm.convert.MemUnit.MiB, enilm.constants.MemUnit.GiB),
            1.205078,
            places=4,
        )
