# Copyright PA Knowledge Ltd 2021
import unittest
import pysisl
from pysisl import sisl_wrapper
from binascii import unhexlify


class SislWrapperTests(unittest.TestCase):

    def test_simple_unwrapping_with_key(self):
        wrapped_data = b"\xd1\xdf\x5f\xff\x00\x01\x00\x00\x00\x00\x00\x30\x00\x00\x00\x01" \
                       b"\x00\x03\x00\x08\x80\x7f\xd4\x1f\x1b\x51\x27\xa9\x00\x00\x00\x00" \
                       b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\x5f\xdf\xd1" \
                       b"\xe8\x1a\xb8\x73\x74"
        self.assertEqual(b'hello', pysisl.unwraps(wrapped_data))

    def test_wrapping_byte_string_then_unwrap_returns_original_data(self):
        data = b'hello'
        wrapped_data = pysisl.wraps(data)
        unwrapped_data = pysisl.unwraps(wrapped_data)
        self.assertEqual(data, unwrapped_data)

    def test_wrapping_bytearray_then_unwrap_returns_original_data(self):
        data = bytearray('hello', encoding='utf-8')
        wrapped_data = pysisl.wraps(data)
        unwrapped_data = pysisl.unwraps(wrapped_data)
        self.assertEqual(data, unwrapped_data)

    def test_wrapped_payload_includes_cloaked_dagger_header(self):
        data = b'hello'
        wrapped_data = pysisl.wraps(data)
        sisl_wrapper.CloakDagger.check_valid_cloaked_dagger_header(wrapped_data)

    def test_empty_payload_returns_only_cloaked_dagger_header(self):
        data = b''
        wrapped_data = pysisl.wraps(data)
        self.assertEqual(self.expected_wrapped_data_size(data), len(wrapped_data))
        sisl_wrapper.CloakDagger.check_valid_cloaked_dagger_header(wrapped_data)

    def test_one_char_payload_returns_wrapped_string(self):
        data = b'a'
        wrapped_data = pysisl.wraps(data)
        self.assertEqual(self.expected_wrapped_data_size(data), len(wrapped_data))
        sisl_wrapper.CloakDagger.check_valid_cloaked_dagger_header(wrapped_data)

    def test_throws_error_when_unwrapping_not_wrapped_payload(self):
        self.assertRaises(sisl_wrapper.InvalidHeaderError, pysisl.unwraps, b'abcdef')

    def test_throws_error_when_unwrapping_not_wrapped_empty_payload(self):
        self.assertRaises(sisl_wrapper.InvalidHeaderError, pysisl.unwraps, b'')

    def test_throw_error_when_wrapping_payload_of_invalid_type(self):
        self.assertRaises(TypeError, pysisl.wraps, {1: 3})

    def test_throws_error_when_unwrapping_empty_payload_of_invalid_type(self):
        self.assertRaises(TypeError, pysisl.unwraps, '')

    def test_throws_error_when_unwrapping_file_with_invalid_header(self):
        wrapped_data = b"\xd1\xdf\x5f\xff\x00\x01\x00\x00\x00\x00\x00\x30\x00\x00\x00\x01" \
                       b"\x00\x03\x00\x08\x80\x7f\xd4\x1f\x1b\x51\x27\xa9\x00\x00\x00\x00" \
                       b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1f\x5f\xdf\xd1" \
                       b"\xe8\x1a\xb8\x73\x74"
        self.assertRaises(sisl_wrapper.InvalidHeaderError, pysisl.unwraps, wrapped_data)

    def test_key_generator_does_not_include_0(self):
        for i in range(10):
            self.assertTrue(b'\x00' not in sisl_wrapper.SislWrapper.key_generation())

    @staticmethod
    def fake_key():
        return unhexlify(b"0123456789ABCDEF")

    @staticmethod
    def expected_wrapped_data_size(data):
        return sisl_wrapper.SislWrapper().headerLen + len(data)


if __name__ == '__main__':
    unittest.main()
