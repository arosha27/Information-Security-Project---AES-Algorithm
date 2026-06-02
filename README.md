# AES Crypto Dashboard

A comprehensive Python-based web application for AES (Advanced Encryption Standard) encryption and decryption with an interactive Streamlit interface. This project provides educational visualization of AES transformation steps and practical tools for secure data encryption.

## Features

### Core Functionality
- **AES Encryption/Decryption**: Support for text and file encryption/decryption
- **Multiple Key Sizes**: 128-bit, 192-bit, and 256-bit AES keys
- **Encryption Modes**: CBC (Cipher Block Chaining) and ECB (Electronic Codebook) modes
- **Secure Key Generation**: Cryptographically secure random key generation
- **Password-Based Key Derivation**: PBKDF2-HMAC-SHA256 for deriving keys from passwords
- **Padding Handling**: Automatic PKCS7 padding for block alignment
- **Base64 Encoding**: Convenient Base64 output format for ciphertext

### Advanced Features
- **QR Code Generation**: Generate QR codes for secure key sharing
- **Encryption Benchmarking**: Performance testing for encryption/decryption operations
- **Dark/Light Mode**: Toggle between dark and light themes
- **File Download**: Download encrypted/decrypted files directly
- **Real-time Operations**: Instant encryption and decryption results

### Educational Features
- **Step-by-Step Visualization**: Visual demonstration of AES transformation steps:
  - SubBytes (S-Box substitution)
  - ShiftRows (Row permutation)
  - MixColumns (Column mixing)
  - AddRoundKey (Key addition)
- **Interactive Diagrams**: ASCII and heatmap visualizations of state matrices
- **Comprehensive Documentation**: Educational content on:
  - Symmetric key cryptography principles
  - AES working principles and structure
  - Security considerations and best practices
  - Real-world applications

## Project Structure

```
aes_crypto_app/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── modules/                    # Core modules
│   ├── __init__.py
│   ├── aes_core.py            # AES encryption/decryption core
│   ├── aes_visualization.py   # AES step visualization
│   └── utils.py               # Utility functions
├── static/                    # Static assets (if needed)
├── tests/                     # Test files
│   └── test_aes.py           # Unit tests
└── docs/                      # Documentation
    └── project_structure.md  # Detailed structure docs
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or download the project**:
   ```bash
   cd "e:/IS Project/aes_crypto_app"
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Unix/MacOS
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**:
   The application will automatically open at `http://localhost:8501`

## Usage Guide

### Dashboard
- **Generate Key**: Create a new random AES key
- **View Current Key**: See the active key and its QR code
- **Quick Actions**: Fast access to encryption features

### Text Encryption
1. Generate or enter an AES key
2. Enter plaintext in the text area
3. Click "Encrypt" to get Base64-encoded ciphertext
4. For decryption, enter ciphertext and IV (for CBC mode)
5. Click "Decrypt" to retrieve original plaintext

### File Encryption
1. Generate or enter an AES key
2. Upload a file using the file uploader
3. Click "Encrypt File" to encrypt the file
4. Download the encrypted file
5. For decryption, upload the encrypted file and click "Decrypt"

### Visualization
1. Enter exactly 16 characters of text
2. Enter a 32-character hex round key
3. Click "Visualize Steps" to see each AES transformation
4. View explanations for each step
5. See heatmap visualization of the state matrix

### Benchmark
1. Ensure a key is generated
2. Select benchmark type (text or file)
3. Adjust iterations as needed
4. Click "Run Benchmark" to see performance metrics
5. View encryption/decryption throughput

### Key Management
1. Generate new keys with different sizes
2. View current key details
3. Generate QR codes for key sharing
4. Download keys as text or QR code images
5. Derive keys from passwords using PBKDF2

### Education
- Browse comprehensive documentation on:
  - Symmetric key cryptography
  - AES principles and structure
  - Security considerations
  - Real-world applications

## Module Documentation

### aes_core.py
Core AES encryption/decryption module.

**Key Classes**:
- `AESCipher`: Main cipher class for encryption/decryption operations

**Key Methods**:
- `generate_key()`: Generate random AES key
- `key_from_password()`: Derive key from password using PBKDF2
- `encrypt_text()`: Encrypt text with AES
- `decrypt_text()`: Decrypt text with AES
- `encrypt_file()`: Encrypt file data
- `decrypt_file()`: Decrypt file data
- `compare_modes()`: Compare ECB vs CBC modes

### aes_visualization.py
AES transformation step visualization module.

**Key Classes**:
- `AESVisualizer`: Visualizes AES transformation steps

**Key Methods**:
- `text_to_state()`: Convert text to state matrix
- `sub_bytes()`: SubBytes transformation
- `shift_rows()`: ShiftRows transformation
- `mix_columns()`: MixColumns transformation
- `add_round_key()`: AddRoundKey transformation
- `demonstrate_round()`: Demonstrate complete AES round
- `get_step_explanation()`: Get step explanations

### utils.py
Utility functions for file operations, QR codes, benchmarking, and education.

**Key Classes**:
- `FileHandler`: File encryption/decryption operations
- `QRCodeGenerator`: QR code generation for keys
- `EncryptionBenchmark`: Performance benchmarking
- `ThemeManager`: Dark/light theme management
- `ValidationHelper`: Input validation
- `EducationalContent`: Educational content provider

## Security Considerations

### Best Practices
- **Never reuse IVs** in CBC mode
- **Use unique keys** for different purposes
- **Store keys securely** (consider HSM or key management systems)
- **Use authenticated encryption** (AES-GCM) when possible
- **Rotate keys regularly**
- **Never hardcode keys** in source code

### Mode Selection
- **ECB Mode**: Never use for data longer than one block (patterns remain visible)
- **CBC Mode**: Use with unique IVs, consider adding authentication
- **GCM Mode**: Recommended for most applications (provides authentication)

### Key Management
- Generate keys using cryptographically secure random number generators
- Use password-based key derivation (PBKDF2) when deriving keys from passwords
- Implement proper key storage and rotation policies
- Consider using hardware security modules (HSMs) for production

## Sample Test Cases

### Test Case 1: Text Encryption (AES-256-CBC)
```python
from modules.aes_core import AESCipher

cipher = AESCipher(key_size=256, mode='CBC')
key = cipher.generate_key()
plaintext = "Hello, World!"
ciphertext, iv = cipher.encrypt_text(plaintext, key)
decrypted = cipher.decrypt_text(ciphertext, key, iv)

assert decrypted == plaintext
```

### Test Case 2: File Encryption
```python
from modules.aes_core import AESCipher

cipher = AESCipher(key_size=256, mode='CBC')
key = cipher.generate_key()
file_data = b"This is file content"
encrypted_data, iv = cipher.encrypt_file(file_data, key)
decrypted_data = cipher.decrypt_file(encrypted_data, key, iv)

assert decrypted_data == file_data
```

### Test Case 3: Password-Based Key Derivation
```python
from modules.aes_core import AESCipher

cipher = AESCipher(key_size=256, mode='CBC')
password = "secure_password_123"
derived_key, salt = cipher.key_from_password(password)

assert len(derived_key) == 32  # 256 bits
```

### Test Case 4: Mode Comparison
```python
from modules.aes_core import AESCipher, compare_modes

plaintext = "Test message for mode comparison"
cipher = AESCipher(key_size=256, mode='CBC')
key = cipher.generate_key()

results = compare_modes(plaintext, key)
assert results['ecb']['ciphertext'] != results['cbc']['ciphertext']
```

## Troubleshooting

### Common Issues

**Issue**: Module import errors
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Streamlit not starting
- **Solution**: Check that streamlit is installed: `pip install streamlit`

**Issue**: QR code generation fails
- **Solution**: Ensure qrcode and pillow are installed: `pip install qrcode pillow`

**Issue**: Visualization errors
- **Solution**: Ensure matplotlib and numpy are installed: `pip install matplotlib numpy`

## Performance Benchmarks

Typical performance on modern hardware (AES-256-CBC):

- **Text Encryption**: ~0.5-2 ms per operation
- **Text Decryption**: ~0.5-2 ms per operation
- **File Encryption**: ~50-200 MB/s throughput
- **File Decryption**: ~50-200 MB/s throughput

*Note: Performance varies based on hardware, key size, and data size.*

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is for educational purposes. AES is a widely-used standard, and this implementation uses the PyCryptodome library for cryptographic operations.

## Acknowledgments

- **NIST**: For establishing the AES standard
- **PyCryptodome**: For providing the cryptographic library
- **Streamlit**: For the web application framework
- **QRCode Library**: For QR code generation

## References

- [NIST FIPS 197: AES Specification](https://csrc.nist.gov/publications/detail/fips/197/final)
- [PyCryptodome Documentation](https://www.pycryptodome.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [AES Wikipedia](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)

## Contact

For questions, issues, or suggestions, please open an issue in the project repository.

---

**Version**: 1.0.0  
**Last Updated**: 2026  
**Python Version**: 3.8+
