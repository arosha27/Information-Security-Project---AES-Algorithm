"""
Sample Test Cases for AES Crypto Application
Comprehensive unit tests for AES encryption/decryption functionality
"""

import sys
import os
import unittest

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.aes_core import AESCipher, compare_modes
from modules.aes_visualization import AESVisualizer
from modules.utils import ValidationHelper


class TestAESCipher(unittest.TestCase):
    """Test cases for AESCipher class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cipher_128 = AESCipher(key_size=128, mode='CBC')
        self.cipher_192 = AESCipher(key_size=192, mode='CBC')
        self.cipher_256 = AESCipher(key_size=256, mode='CBC')
        self.cipher_ecb = AESCipher(key_size=256, mode='ECB')
    
    def test_key_generation(self):
        """Test key generation for different sizes."""
        key_128 = self.cipher_128.generate_key()
        key_192 = self.cipher_192.generate_key()
        key_256 = self.cipher_256.generate_key()
        
        self.assertEqual(len(key_128), 16)  # 128 bits = 16 bytes
        self.assertEqual(len(key_192), 24)  # 192 bits = 24 bytes
        self.assertEqual(len(key_256), 32)  # 256 bits = 32 bytes
        
        # Keys should be different
        self.assertNotEqual(key_128, key_192)
        self.assertNotEqual(key_192, key_256)
    
    def test_text_encryption_decryption_cbc(self):
        """Test text encryption and decryption in CBC mode."""
        key = self.cipher_256.generate_key()
        plaintext = "Hello, World! This is a test message."
        
        ciphertext, iv = self.cipher_256.encrypt_text(plaintext, key)
        decrypted = self.cipher_256.decrypt_text(ciphertext, key, iv)
        
        self.assertEqual(plaintext, decrypted)
        self.assertIsNotNone(iv)
        self.assertEqual(len(iv), 16)  # IV is 16 bytes
    
    def test_text_encryption_decryption_ecb(self):
        """Test text encryption and decryption in ECB mode."""
        key = self.cipher_ecb.generate_key()
        plaintext = "Hello, World! This is a test message."
        
        ciphertext, iv = self.cipher_ecb.encrypt_text(plaintext, key)
        decrypted = self.cipher_ecb.decrypt_text(ciphertext, key, iv)
        
        self.assertEqual(plaintext, decrypted)
        self.assertIsNone(iv)  # ECB doesn't use IV
    
    def test_file_encryption_decryption(self):
        """Test file encryption and decryption."""
        key = self.cipher_256.generate_key()
        file_data = b"This is test file content for encryption testing."
        
        encrypted_data, iv = self.cipher_256.encrypt_file(file_data, key)
        decrypted_data = self.cipher_256.decrypt_file(encrypted_data, key, iv)
        
        self.assertEqual(file_data, decrypted_data)
    
    def test_password_key_derivation(self):
        """Test password-based key derivation."""
        password = "secure_password_123"
        
        derived_key, salt = self.cipher_256.key_from_password(password)
        
        self.assertEqual(len(derived_key), 32)  # 256 bits
        self.assertEqual(len(salt), 16)  # Salt is 16 bytes
        
        # Same password with same salt should produce same key
        derived_key_2, _ = self.cipher_256.key_from_password(password, salt)
        self.assertEqual(derived_key, derived_key_2)
    
    def test_key_formatting(self):
        """Test key formatting and parsing."""
        key = self.cipher_256.generate_key()
        
        # Format to hex
        key_hex = self.cipher_256.format_key(key)
        self.assertEqual(len(key_hex), 64)  # 32 bytes = 64 hex chars
        
        # Parse back
        parsed_key = self.cipher_256.parse_key(key_hex)
        self.assertEqual(key, parsed_key)
    
    def test_invalid_key_size(self):
        """Test that invalid key sizes raise errors."""
        with self.assertRaises(ValueError):
            AESCipher(key_size=64, mode='CBC')
        
        with self.assertRaises(ValueError):
            AESCipher(key_size=512, mode='CBC')
    
    def test_invalid_mode(self):
        """Test that invalid modes raise errors."""
        with self.assertRaises(ValueError):
            AESCipher(key_size=256, mode='GCM')
    
    def test_wrong_key_size_error(self):
        """Test that wrong key size raises error."""
        key_128 = self.cipher_128.generate_key()
        
        with self.assertRaises(ValueError):
            self.cipher_256.encrypt_text("test", key_128)


class TestAESVisualization(unittest.TestCase):
    """Test cases for AESVisualizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.visualizer = AESVisualizer()
    
    def test_text_to_state(self):
        """Test text to state matrix conversion."""
        text = "AESVisualization"
        state = self.visualizer.text_to_state(text)
        
        self.assertEqual(state.shape, (4, 4))
    
    def test_sub_bytes(self):
        """Test SubBytes transformation."""
        state = self.visualizer.text_to_state("TestText12345678")
        result = self.visualizer.sub_bytes(state)
        
        self.assertEqual(result.shape, (4, 4))
    
    def test_shift_rows(self):
        """Test ShiftRows transformation."""
        state = self.visualizer.text_to_state("TestText12345678")
        result = self.visualizer.shift_rows(state)
        
        self.assertEqual(result.shape, (4, 4))
    
    def test_mix_columns(self):
        """Test MixColumns transformation."""
        state = self.visualizer.text_to_state("TestText12345678")
        result = self.visualizer.mix_columns(state)
        
        self.assertEqual(result.shape, (4, 4))
    
    def test_add_round_key(self):
        """Test AddRoundKey transformation."""
        state = self.visualizer.text_to_state("TestText12345678")
        key_state = self.visualizer.text_to_state("KeyKeyKey1234567")
        result = self.visualizer.add_round_key(state, key_state)
        
        self.assertEqual(result.shape, (4, 4))
    
    def test_gf_multiply(self):
        """Test Galois Field multiplication."""
        result = self.visualizer.gf_multiply(0x53, 0xCA)
        self.assertIsInstance(result, int)
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 255)
    
    def test_demonstrate_round(self):
        """Test complete round demonstration."""
        text = "AESVisualization"
        round_key = "2b7e151628aed2a6abf7158809cf4f3c"
        
        results = self.visualizer.demonstrate_round(text, round_key)
        
        self.assertIn('initial', results)
        self.assertIn('subbytes', results)
        self.assertIn('shiftrows', results)
        self.assertIn('mixcolumns', results)
        self.assertIn('addroundkey', results)


class TestValidationHelper(unittest.TestCase):
    """Test cases for ValidationHelper class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = ValidationHelper()
    
    def test_validate_key_128(self):
        """Test 128-bit key validation."""
        valid_key = "2b7e151628aed2a6abf7158809cf4f3c"  # 32 hex chars
        invalid_key = "2b7e1516"  # Too short
        
        self.assertTrue(self.validator.validate_key(valid_key, 128))
        self.assertFalse(self.validator.validate_key(invalid_key, 128))
    
    def test_validate_key_256(self):
        """Test 256-bit key validation."""
        valid_key = "2b7e151628aed2a6abf7158809cf4f3c2b7e151628aed2a6abf7158809cf4f3c"  # 64 hex chars
        invalid_key = "2b7e151628aed2a6abf7158809cf4f3c"  # Too short
        
        self.assertTrue(self.validator.validate_key(valid_key, 256))
        self.assertFalse(self.validator.validate_key(invalid_key, 256))
    
    def test_validate_plaintext(self):
        """Test plaintext validation."""
        self.assertTrue(self.validator.validate_plaintext("Hello"))
        self.assertFalse(self.validator.validate_plaintext(""))
        self.assertFalse(self.validator.validate_plaintext(None))
    
    def test_validate_ciphertext(self):
        """Test ciphertext validation."""
        import base64
        valid_ciphertext = base64.b64encode(b"test").decode('utf-8')
        invalid_ciphertext = "not_base64!!!"
        
        self.assertTrue(self.validator.validate_ciphertext(valid_ciphertext))
        self.assertFalse(self.validator.validate_ciphertext(invalid_ciphertext))


class TestCompareModes(unittest.TestCase):
    """Test cases for mode comparison."""
    
    def test_compare_modes(self):
        """Test ECB vs CBC mode comparison."""
        plaintext = "Test message for mode comparison"
        cipher = AESCipher(key_size=256, mode='CBC')
        key = cipher.generate_key()
        
        results = compare_modes(plaintext, key)
        
        self.assertIn('ecb', results)
        self.assertIn('cbc', results)
        self.assertIn('ciphertext', results['ecb'])
        self.assertIn('ciphertext', results['cbc'])
        
        # ECB and CBC should produce different ciphertexts
        self.assertNotEqual(results['ecb']['ciphertext'], results['cbc']['ciphertext'])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def test_empty_plaintext(self):
        """Test encryption of empty string."""
        cipher = AESCipher(key_size=256, mode='CBC')
        key = cipher.generate_key()
        
        ciphertext, iv = cipher.encrypt_text("", key)
        decrypted = cipher.decrypt_text(ciphertext, key, iv)
        
        self.assertEqual("", decrypted)
    
    def test_unicode_plaintext(self):
        """Test encryption of unicode text."""
        cipher = AESCipher(key_size=256, mode='CBC')
        key = cipher.generate_key()
        plaintext = "Hello 世界 🌍"
        
        ciphertext, iv = cipher.encrypt_text(plaintext, key)
        decrypted = cipher.decrypt_text(ciphertext, key, iv)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_large_file(self):
        """Test encryption of large file data."""
        cipher = AESCipher(key_size=256, mode='CBC')
        key = cipher.generate_key()
        
        # Create 1MB of data
        large_data = b"A" * (1024 * 1024)
        
        encrypted_data, iv = cipher.encrypt_file(large_data, key)
        decrypted_data = cipher.decrypt_file(encrypted_data, key, iv)
        
        self.assertEqual(large_data, decrypted_data)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAESCipher))
    suite.addTests(loader.loadTestsFromTestCase(TestAESVisualization))
    suite.addTests(loader.loadTestsFromTestCase(TestValidationHelper))
    suite.addTests(loader.loadTestsFromTestCase(TestCompareModes))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
