"""
AES Core Module
Implements AES encryption and decryption with support for:
- 128-bit, 192-bit, and 256-bit keys
- ECB and CBC modes
- PKCS7 padding
- Base64 encoding for output
"""

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from typing import Tuple, Union


class AESCipher:
    """
    AES Cipher class for encryption and decryption operations.
    Supports multiple key sizes and encryption modes.
    """
    
    def __init__(self, key_size: int = 256, mode: str = 'CBC'):
        """
        Initialize AES Cipher.
        
        Args:
            key_size: Key size in bits (128, 192, or 256)
            mode: Encryption mode ('ECB' or 'CBC')
        """
        self.key_size = key_size
        self.mode = mode.upper()
        
        if key_size not in [128, 192, 256]:
            raise ValueError("Key size must be 128, 192, or 256 bits")
        
        if self.mode not in ['ECB', 'CBC']:
            raise ValueError("Mode must be 'ECB' or 'CBC'")
    
    def generate_key(self) -> bytes:
        """
        Generate a random AES key of specified size.
        
        Returns:
            Random key as bytes
        """
        return get_random_bytes(self.key_size // 8)
    
    def key_from_password(self, password: str, salt: bytes = None) -> Tuple[bytes, bytes]:
        """
        Derive AES key from password using PBKDF2.
        
        Args:
            password: User password string
            salt: Salt for key derivation (generated if None)
            
        Returns:
            Tuple of (derived_key, salt)
        """
        if salt is None:
            salt = get_random_bytes(16)
        
        # Use PBKDF2-HMAC-SHA256 for key derivation
        derived_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000,  # Number of iterations
            self.key_size // 8
        )
        
        return derived_key, salt
    
    def encrypt_text(self, plaintext: str, key: bytes) -> Tuple[str, bytes]:
        """
        Encrypt text using AES.
        
        Args:
            plaintext: Text to encrypt
            key: AES key (must match key_size)
            
        Returns:
            Tuple of (base64_encoded_ciphertext, iv) or (ciphertext, None for ECB)
        """
        if len(key) != self.key_size // 8:
            raise ValueError(f"Key must be {self.key_size // 8} bytes for {self.key_size}-bit AES")
        
        # Convert plaintext to bytes
        plaintext_bytes = plaintext.encode('utf-8')
        
        # Create cipher
        if self.mode == 'ECB':
            cipher = AES.new(key, AES.MODE_ECB)
            iv = None
        else:  # CBC
            iv = get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Encrypt with padding
        ciphertext = cipher.encrypt(pad(plaintext_bytes, AES.block_size))
        
        # Encode to base64 for display
        ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
        
        return ciphertext_b64, iv
    
    def decrypt_text(self, ciphertext_b64: str, key: bytes, iv: bytes = None) -> str:
        """
        Decrypt text using AES.
        
        Args:
            ciphertext_b64: Base64-encoded ciphertext
            key: AES key
            iv: Initialization vector (required for CBC)
            
        Returns:
            Decrypted plaintext
        """
        if len(key) != self.key_size // 8:
            raise ValueError(f"Key must be {self.key_size // 8} bytes for {self.key_size}-bit AES")
        
        if self.mode == 'CBC' and iv is None:
            raise ValueError("IV is required for CBC mode")
        
        # Decode from base64
        ciphertext = base64.b64decode(ciphertext_b64)
        
        # Create cipher
        if self.mode == 'ECB':
            cipher = AES.new(key, AES.MODE_ECB)
        else:  # CBC
            cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Decrypt and unpad
        plaintext_bytes = unpad(cipher.decrypt(ciphertext), AES.block_size)
        
        return plaintext_bytes.decode('utf-8')
    
    def encrypt_file(self, file_data: bytes, key: bytes) -> Tuple[bytes, bytes]:
        """
        Encrypt file data using AES.
        
        Args:
            file_data: File content as bytes
            key: AES key
            
        Returns:
            Tuple of (encrypted_data, iv) or (encrypted_data, None for ECB)
        """
        if len(key) != self.key_size // 8:
            raise ValueError(f"Key must be {self.key_size // 8} bytes for {self.key_size}-bit AES")
        
        # Create cipher
        if self.mode == 'ECB':
            cipher = AES.new(key, AES.MODE_ECB)
            iv = None
        else:  # CBC
            iv = get_random_bytes(16)
            cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Encrypt with padding
        encrypted_data = cipher.encrypt(pad(file_data, AES.block_size))
        
        return encrypted_data, iv
    
    def decrypt_file(self, encrypted_data: bytes, key: bytes, iv: bytes = None) -> bytes:
        """
        Decrypt file data using AES.
        
        Args:
            encrypted_data: Encrypted file content
            key: AES key
            iv: Initialization vector (required for CBC)
            
        Returns:
            Decrypted file data
        """
        if len(key) != self.key_size // 8:
            raise ValueError(f"Key must be {self.key_size // 8} bytes for {self.key_size}-bit AES")
        
        if self.mode == 'CBC' and iv is None:
            raise ValueError("IV is required for CBC mode")
        
        # Create cipher
        if self.mode == 'ECB':
            cipher = AES.new(key, AES.MODE_ECB)
        else:  # CBC
            cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Decrypt and unpad
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        
        return decrypted_data
    
    def format_key(self, key: bytes) -> str:
        """
        Format key for display (hex string).
        
        Args:
            key: Key as bytes
            
        Returns:
            Hexadecimal string representation
        """
        return key.hex().upper()
    
    def parse_key(self, key_hex: str) -> bytes:
        """
        Parse hex string to bytes.
        
        Args:
            key_hex: Hexadecimal string
            
        Returns:
            Key as bytes
        """
        return bytes.fromhex(key_hex)


def compare_modes(plaintext: str, key: bytes) -> dict:
    """
    Compare ECB and CBC modes encryption results.
    
    Args:
        plaintext: Text to encrypt
        key: AES key
        
    Returns:
        Dictionary with comparison results
    """
    results = {}
    
    # ECB encryption
    ecb_cipher = AESCipher(key_size=256, mode='ECB')
    ecb_ciphertext, _ = ecb_cipher.encrypt_text(plaintext, key)
    
    # CBC encryption
    cbc_cipher = AESCipher(key_size=256, mode='CBC')
    cbc_ciphertext, iv = cbc_cipher.encrypt_text(plaintext, key)
    
    results['ecb'] = {
        'ciphertext': ecb_ciphertext,
        'length': len(ecb_ciphertext)
    }
    
    results['cbc'] = {
        'ciphertext': cbc_ciphertext,
        'iv': iv.hex() if iv else None,
        'length': len(cbc_ciphertext)
    }
    
    return results
