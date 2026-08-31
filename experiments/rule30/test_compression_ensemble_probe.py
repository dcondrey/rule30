from __future__ import annotations

import unittest

from compression_ensemble_probe import (
    COMPRESSORS,
    ENCODINGS,
    compress_grid,
    decode_sequence,
    encode_sequence,
    pack_bits,
    unpack_bits,
)


class CompressionEnsembleProbeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.side = 8
        self.bits = [((index * 13 + index // 7) >> 2) & 1 for index in range(64)]

    def test_bit_packing_round_trip(self) -> None:
        self.assertEqual(unpack_bits(pack_bits(self.bits), len(self.bits)), self.bits)

    def test_every_encoding_is_exactly_reversible(self) -> None:
        for encoding in ENCODINGS:
            with self.subTest(encoding=encoding):
                encoded = encode_sequence(self.bits, self.side, encoding)
                self.assertEqual(len(encoded), len(self.bits))
                self.assertEqual(decode_sequence(encoded, self.side, encoding), self.bits)

    def test_every_compressor_round_trip(self) -> None:
        packed = pack_bits(self.bits)
        for name, (compress, decompress) in COMPRESSORS.items():
            with self.subTest(compressor=name):
                self.assertEqual(decompress(compress(packed)), packed)

    def test_compress_grid_accepts_all_pipelines(self) -> None:
        for encoding in ENCODINGS:
            for compressor in COMPRESSORS:
                with self.subTest(encoding=encoding, compressor=compressor):
                    self.assertTrue(compress_grid(self.bits, self.side, encoding, compressor))


if __name__ == "__main__":
    unittest.main()
