"""
Utilities Module
Provides helper functions for file operations, QR code generation,
and encryption benchmarking.
"""

import os
import time
import io
import qrcode
from typing import Tuple, Dict
import streamlit as st


class FileHandler:
    """
    Handles file encryption/decryption operations with download support.
    """
    
    @staticmethod
    def encrypt_file_upload(uploaded_file, key: bytes, iv: bytes = None, mode: str = 'CBC') -> Tuple[bytes, str]:
        """
        Encrypt an uploaded file.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            key: AES key
            iv: Initialization vector (for CBC mode)
            mode: Encryption mode ('ECB' or 'CBC')
            
        Returns:
            Tuple of (encrypted_data, filename)
        """
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from modules.aes_core import AESCipher
        
        # Read file data
        file_data = uploaded_file.read()
        
        # Encrypt
        cipher = AESCipher(key_size=len(key) * 8, mode=mode)
        encrypted_data, generated_iv = cipher.encrypt_file(file_data, key)
        
        # For CBC mode, prepend IV to encrypted data
        if mode == 'CBC' and generated_iv:
            final_data = generated_iv + encrypted_data
        else:
            final_data = encrypted_data
        
        # Create new filename
        original_name = uploaded_file.name
        encrypted_name = f"encrypted_{original_name}"
        
        return final_data, encrypted_name
    
    @staticmethod
    def decrypt_file_upload(uploaded_file, key: bytes, mode: str = 'CBC') -> Tuple[bytes, str]:
        """
        Decrypt an uploaded file.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            key: AES key
            mode: Encryption mode ('ECB' or 'CBC')
            
        Returns:
            Tuple of (decrypted_data, filename)
        """
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from modules.aes_core import AESCipher
        
        # Read file data
        file_data = uploaded_file.read()
        
        # Extract IV if CBC mode
        if mode == 'CBC':
            iv = file_data[:16]
            encrypted_data = file_data[16:]
        else:
            iv = None
            encrypted_data = file_data
        
        # Decrypt
        cipher = AESCipher(key_size=len(key) * 8, mode=mode)
        decrypted_data = cipher.decrypt_file(encrypted_data, key, iv)
        
        # Create new filename
        original_name = uploaded_file.name
        if original_name.startswith("encrypted_"):
            decrypted_name = original_name.replace("encrypted_", "decrypted_", 1)
        else:
            decrypted_name = f"decrypted_{original_name}"
        
        return decrypted_data, decrypted_name
    
    @staticmethod
    def get_file_info(uploaded_file) -> Dict[str, str]:
        """
        Get information about an uploaded file.
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Dictionary with file information
        """
        return {
            'name': uploaded_file.name,
            'size': f"{uploaded_file.size / 1024:.2f} KB",
            'type': uploaded_file.type
        }


class QRCodeGenerator:
    """
    Generates QR codes for key sharing.
    """
    
    @staticmethod
    def generate_key_qr(key: str, key_name: str = "AES Key") -> bytes:
        """
        Generate a QR code for an AES key.
        
        Args:
            key: AES key as hexadecimal string
            key_name: Name/label for the key
            
        Returns:
            QR code image as bytes
        """
        # Create QR code with key data
        qr_data = f"{key_name}: {key}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()
    
    @staticmethod
    def generate_key_qr_with_metadata(key: str, key_size: int, mode: str) -> bytes:
        """
        Generate a QR code with complete key metadata.
        
        Args:
            key: AES key as hexadecimal string
            key_size: Key size in bits
            mode: Encryption mode
            
        Returns:
            QR code image as bytes
        """
        metadata = f"AES-{key_size}-{mode}|{key}"
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(metadata)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()


class EncryptionBenchmark:
    """
    Benchmarks encryption/decryption performance.
    """
    
    @staticmethod
    def benchmark_text_encryption(plaintext: str, key: bytes, mode: str, iterations: int = 100) -> Dict[str, float]:
        """
        Benchmark text encryption speed.
        
        Args:
            plaintext: Text to encrypt
            key: AES key
            mode: Encryption mode
            iterations: Number of iterations
            
        Returns:
            Dictionary with benchmark results
        """
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from modules.aes_core import AESCipher
        
        cipher = AESCipher(key_size=len(key) * 8, mode=mode)
        
        # Warm-up
        cipher.encrypt_text(plaintext, key)
        
        # Benchmark encryption
        start_time = time.time()
        for _ in range(iterations):
            cipher.encrypt_text(plaintext, key)
        encrypt_time = time.time() - start_time
        
        # Get ciphertext for decryption benchmark
        ciphertext, iv = cipher.encrypt_text(plaintext, key)
        
        # Benchmark decryption
        start_time = time.time()
        for _ in range(iterations):
            cipher.decrypt_text(ciphertext, key, iv)
        decrypt_time = time.time() - start_time
        
        return {
            'encrypt_time_ms': (encrypt_time / iterations) * 1000,
            'decrypt_time_ms': (decrypt_time / iterations) * 1000,
            'encrypt_ops_per_sec': iterations / encrypt_time,
            'decrypt_ops_per_sec': iterations / decrypt_time
        }
    
    @staticmethod
    def benchmark_file_encryption(file_size_kb: int, key: bytes, mode: str, iterations: int = 10) -> Dict[str, float]:
        """
        Benchmark file encryption speed.
        
        Args:
            file_size_kb: File size in KB
            key: AES key
            mode: Encryption mode
            iterations: Number of iterations
            
        Returns:
            Dictionary with benchmark results
        """
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        from modules.aes_core import AESCipher
        
        cipher = AESCipher(key_size=len(key) * 8, mode=mode)
        
        # Generate test data
        test_data = os.urandom(file_size_kb * 1024)
        
        # Warm-up
        cipher.encrypt_file(test_data, key)
        
        # Benchmark encryption
        start_time = time.time()
        for _ in range(iterations):
            cipher.encrypt_file(test_data, key)
        encrypt_time = time.time() - start_time
        
        # Get encrypted data for decryption benchmark
        encrypted_data, iv = cipher.encrypt_file(test_data, key)
        
        # Benchmark decryption
        start_time = time.time()
        for _ in range(iterations):
            cipher.decrypt_file(encrypted_data, key, iv)
        decrypt_time = time.time() - start_time
        
        data_size_mb = (file_size_kb * iterations) / 1024
        
        return {
            'encrypt_time_sec': encrypt_time,
            'decrypt_time_sec': decrypt_time,
            'encrypt_throughput_mbps': data_size_mb / encrypt_time,
            'decrypt_throughput_mbps': data_size_mb / decrypt_time
        }


class ThemeManager:
    """
    Manages dark/light theme for the application.
    """
    
    @staticmethod
    def apply_theme():
        """Apply the selected theme to Streamlit."""
        if 'theme' not in st.session_state:
            st.session_state.theme = 'dark'
        
        if st.session_state.theme == 'dark':
            # Dark theme colors
            st.markdown("""
            <style>
            .stApp {
                background-color: #0E1117;
            }
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stSelectbox > div > div > select {
                background-color: #1E2130;
                color: #FAFAFA;
            }
            </style>
            """, unsafe_allow_html=True)
        else:
            # Light theme colors
            st.markdown("""
            <style>
            .stApp {
                background-color: #FFFFFF;
            }
            </style>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def toggle_theme():
        """Toggle between dark and light theme."""
        if 'theme' not in st.session_state:
            st.session_state.theme = 'dark'
        
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'


class ValidationHelper:
    """
    Helper functions for input validation.
    """
    
    @staticmethod
    def validate_key(key_hex: str, key_size: int) -> bool:
        """
        Validate a hexadecimal key string.
        
        Args:
            key_hex: Key as hexadecimal string
            key_size: Expected key size in bits
            
        Returns:
            True if valid, False otherwise
        """
        try:
            key_bytes = bytes.fromhex(key_hex)
            return len(key_bytes) == key_size // 8
        except ValueError:
            return False
    
    @staticmethod
    def validate_plaintext(plaintext: str) -> bool:
        """
        Validate plaintext input.
        
        Args:
            plaintext: Text to validate
            
        Returns:
            True if valid, False otherwise
        """
        return plaintext is not None and len(plaintext) > 0
    
    @staticmethod
    def validate_ciphertext(ciphertext_b64: str) -> bool:
        """
        Validate base64-encoded ciphertext.
        
        Args:
            ciphertext_b64: Base64-encoded ciphertext
            
        Returns:
            True if valid, False otherwise
        """
        try:
            import base64
            decoded = base64.b64decode(ciphertext_b64)
            return len(decoded) > 0
        except Exception:
            return False


class EducationalContent:
    """
    Provides educational content about AES and cryptography.
    """
    
    @staticmethod
    def get_symmetric_key_cryptography_info() -> str:
        """Get information about symmetric key cryptography."""
        return """
# Symmetric Key Cryptography

## What is Symmetric Key Cryptography?

Symmetric key cryptography is a cryptographic system where the same key is used for both encryption and decryption. This means that the sender and receiver must share the same secret key before they can communicate securely.

## Key Characteristics

- **Single Key**: One key serves both encryption and decryption purposes
- **Speed**: Generally faster than asymmetric cryptography
- **Key Distribution**: Requires secure key exchange mechanism
- **Key Management**: Each pair of users needs a unique key

## Common Symmetric Algorithms

1. **AES (Advanced Encryption Standard)** - Current standard, widely used
2. **DES (Data Encryption Standard)** - Older, now considered insecure
3. **3DES (Triple DES)** - Improved DES, still used in some legacy systems
4. **Blowfish** - Fast, flexible block cipher
5. **Twofish** - Successor to Blowfish

## Advantages

- **Performance**: Much faster than asymmetric encryption
- **Efficiency**: Suitable for encrypting large amounts of data
- **Simplicity**: Easier to implement and understand
- **Mature**: Well-studied and standardized

## Limitations

- **Key Distribution**: Secure key exchange is challenging
- **Scalability**: Number of keys grows quadratically with users
- **Key Management**: Requires secure storage and handling of keys

## Real-World Applications

- **File Encryption**: Encrypting sensitive files on disk
- **Database Encryption**: Protecting data at rest
- **Network Communication**: TLS/SSL for secure web browsing
- **Wireless Security**: WPA2/WPA3 for WiFi networks
- **Disk Encryption**: Full disk encryption solutions
        """
    
    @staticmethod
    def get_aes_working_principles() -> str:
        """Get information about AES working principles."""
        return """
# AES Working Principles

## Overview

The Advanced Encryption Standard (AES) is a symmetric block cipher that operates on 128-bit blocks of data using keys of 128, 192, or 256 bits. It was selected by NIST in 2001 to replace DES.

## AES Structure

AES is based on a substitution-permutation network (SPN) structure and consists of:

1. **Initial Round**: AddRoundKey
2. **Main Rounds** (9, 11, or 13 depending on key size):
   - SubBytes
   - ShiftRows
   - MixColumns
   - AddRoundKey
3. **Final Round**:
   - SubBytes
   - ShiftRows
   - AddRoundKey

## Transformation Steps

### 1. SubBytes (Non-linear substitution)
- Replaces each byte with a corresponding byte from the S-Box
- Provides confusion - makes relationship between plaintext and ciphertext complex
- Uses a pre-computed lookup table (S-Box)

### 2. ShiftRows (Permutation)
- Cyclically shifts each row of the state matrix
- Row 0: No shift
- Row 1: Shift left by 1 byte
- Row 2: Shift left by 2 bytes
- Row 3: Shift left by 3 bytes
- Provides diffusion

### 3. MixColumns (Linear transformation)
- Mixes data in each column using matrix multiplication in GF(2^8)
- Each column is multiplied by a fixed matrix
- Enhances diffusion further
- Skipped in the final round

### 4. AddRoundKey (Key addition)
- XORs the state with a round key derived from the encryption key
- Incorporates key material into the encryption process
- Only step that uses the key

## Key Expansion

AES uses a key expansion algorithm to generate round keys from the original key:
- 128-bit key: 11 round keys (1 initial + 10 rounds)
- 192-bit key: 13 round keys (1 initial + 12 rounds)
- 256-bit key: 15 round keys (1 initial + 14 rounds)

## Security Features

- **Confusion**: SubBytes makes the relationship complex
- **Diffusion**: ShiftRows and MixColumns spread information
- **Key Schedule**: Complex key expansion prevents related-key attacks
- **No Weak Keys**: Unlike DES, AES has no known weak keys
        """
    
    @staticmethod
    def get_security_considerations() -> str:
        """Get security considerations for AES."""
        return """
# AES Security Considerations

## Security Strength

AES is considered very secure with no practical attacks against the full algorithm:

- **AES-128**: Security level of 128 bits (2^128 operations to break)
- **AES-192**: Security level of 192 bits
- **AES-256**: Security level of 256 bits

## Known Attacks

### Theoretical Attacks
- **Related-key attacks**: Only affect reduced-round versions
- **Side-channel attacks**: Require physical access to device
- **Cache-timing attacks**: Require careful implementation

### Practical Considerations
- No known attacks against full AES with all rounds
- Brute force is computationally infeasible
- Mathematical attacks have failed

## Best Practices

### Key Management
- Use strong random key generation
- Never reuse keys for different purposes
- Rotate keys regularly
- Store keys securely (HSM, key management systems)

### Implementation
- Use authenticated encryption (AES-GCM) when possible
- Always use unique IVs/Nonces for CBC mode
- Implement constant-time operations to prevent timing attacks
- Use well-tested libraries (not custom implementations)

### Mode Selection
- **ECB**: Never use for data longer than one block
- **CBC**: Use with unique IVs, consider authentication
- **GCM**: Recommended for most applications (provides authentication)
- **CTR**: Good for parallel encryption, requires unique nonce

## Common Pitfalls

1. **Reusing IVs**: Can reveal information about plaintext
2. **Using ECB mode**: Patterns in plaintext remain visible
3. **Weak key generation**: Using predictable keys
4. **Not authenticating**: Vulnerable to tampering attacks
5. **Side-channel leaks**: Implementation vulnerabilities

## Compliance

AES is approved for:
- **US Government**: FIPS 197 standard
- **NSA**: Suite B cryptography (up to Secret level)
- **International**: ISO/IEC 18033 standard
- **Payment Industry**: PCI DSS compliance

## Future Considerations

- **Quantum Computing**: Grover's algorithm could halve the effective security
- **Post-Quantum**: Consider AES-256 for long-term security
- **NIST Competition**: Ongoing post-quantum cryptography standardization
        """
    
    @staticmethod
    def get_real_world_applications() -> str:
        """Get information about real-world AES applications."""
        return """
# Real-World Applications of AES

## Web Security

### HTTPS/TLS
- AES is the primary symmetric cipher in TLS 1.2 and TLS 1.3
- Used in combination with asymmetric cryptography for key exchange
- Protects all web traffic (banking, e-commerce, social media)

### VPNs
- OpenVPN, WireGuard, and IPsec use AES for tunnel encryption
- Secures remote access and site-to-site connections
- AES-256 is commonly used for high-security applications

## Data Protection

### File Encryption
- **Windows**: BitLocker uses AES-256
- **macOS**: FileVault uses AES-256
- **Linux**: LUKS encryption supports AES

### Database Encryption
- Transparent Data Encryption (TDE) in databases
- Column-level encryption for sensitive fields
- Backup encryption

## Wireless Security

### WiFi
- **WPA2**: Uses AES-CCMP for encryption
- **WPA3**: Mandatory AES encryption
- Protects wireless network traffic

### Bluetooth
- Bluetooth Low Energy (BLE) uses AES-CCM
- Secure connections for IoT devices

## Mobile Security

### Smartphone Encryption
- iOS: Full disk encryption with AES-256
- Android: File-based encryption with AES-256
- Secure enclave/keymaster integration

### App Security
- Encrypted app data storage
- Secure communication between app and server
- Payment processing (Apple Pay, Google Pay)

## Payment Systems

### Credit Card Processing
- EMV chip cards use AES for transaction security
- Point-of-sale (POS) terminal encryption
- Payment gateway security

### Cryptocurrency
- Wallet encryption
- Transaction signing (in combination with asymmetric crypto)
- Exchange security

## Cloud Security

### Storage Services
- AWS S3 server-side encryption (AES-256)
- Google Cloud Storage encryption
- Azure Blob Storage encryption

### Database Services
- AWS RDS encryption
- Google Cloud SQL encryption
- Azure SQL Database encryption

## Messaging Applications

### End-to-End Encryption
- Signal Protocol uses AES-CBC
- WhatsApp encryption
- Telegram secret chats

## Government and Military

- **NSA**: Suite B cryptography (up to Secret level)
- **NATO**: Approved for secure communications
- **Defense**: Classified information protection

## IoT and Embedded Systems

- Smart home devices
- Industrial control systems
- Medical devices
- Automotive systems

## Performance Considerations

AES is hardware-accelerated in:
- Intel AES-NI instruction set
- ARM Crypto extensions
- Dedicated crypto processors

This makes it suitable for:
- High-throughput servers
- Low-power embedded devices
- Real-time applications
"""
