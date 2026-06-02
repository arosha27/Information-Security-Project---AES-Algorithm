# AES Crypto Application - Project Structure

## Directory Structure

```
aes_crypto_app/
│
├── app.py                          # Main Streamlit application entry point
├── requirements.txt                # Python package dependencies
├── README.md                       # Comprehensive project documentation
│
├── modules/                        # Core application modules
│   ├── __init__.py                # Module initialization and exports
│   ├── aes_core.py                # AES encryption/decryption core functionality
│   ├── aes_visualization.py       # AES transformation step visualization
│   └── utils.py                   # Utility functions and helpers
│
├── static/                         # Static assets (CSS, images, etc.)
│   └── (empty - for future expansion)
│
├── tests/                          # Unit and integration tests
│   └── test_aes.py                # Comprehensive test suite
│
└── docs/                           # Additional documentation
    └── project_structure.md       # This file
```

## Module Descriptions

### app.py
**Purpose**: Main Streamlit web application
**Key Features**:
- Dashboard with quick actions and key display
- Text encryption/decryption interface
- File encryption/decryption with download support
- AES step visualization with educational explanations
- Educational content pages
- Encryption benchmarking tools
- Key management with QR code generation
- Dark/light theme toggle

**Dependencies**: streamlit, all modules

### modules/aes_core.py
**Purpose**: Core AES encryption/decryption implementation
**Key Classes**:
- `AESCipher`: Main cipher class for all encryption operations

**Key Functions**:
- `compare_modes()`: Compare ECB vs CBC encryption results

**Features**:
- Support for 128, 192, 256-bit keys
- CBC and ECB modes
- PKCS7 padding
- Base64 encoding
- Password-based key derivation (PBKDF2)
- File encryption/decryption

**Dependencies**: pycryptodome, hashlib, base64

### modules/aes_visualization.py
**Purpose**: Educational visualization of AES transformation steps
**Key Classes**:
- `AESVisualizer`: Visualizes AES transformations

**Key Functions**:
- `create_heatmap()`: Creates matplotlib heatmap of state matrix

**Features**:
- SubBytes (S-Box) visualization
- ShiftRows visualization
- MixColumns visualization
- AddRoundKey visualization
- State matrix ASCII representation
- Step-by-step explanations
- Comparison diagrams (ECB vs CBC)

**Dependencies**: numpy, matplotlib

### modules/utils.py
**Purpose**: Utility functions for various application features
**Key Classes**:
- `FileHandler`: File encryption/decryption operations
- `QRCodeGenerator`: QR code generation for keys
- `EncryptionBenchmark`: Performance benchmarking
- `ThemeManager`: Dark/light theme management
- `ValidationHelper`: Input validation
- `EducationalContent`: Educational content provider

**Features**:
- File upload/download handling
- QR code generation with metadata
- Encryption/decryption speed benchmarking
- Theme switching
- Input validation
- Comprehensive educational content

**Dependencies**: qrcode, pillow, streamlit, time, io

### tests/test_aes.py
**Purpose**: Comprehensive unit test suite
**Test Classes**:
- `TestAESCipher`: Tests for core AES functionality
- `TestAESVisualization`: Tests for visualization module
- `TestValidationHelper`: Tests for validation functions
- `TestCompareModes`: Tests for mode comparison
- `TestEdgeCases`: Tests for edge cases and error handling

**Test Coverage**:
- Key generation for all sizes
- Text encryption/decryption (CBC and ECB)
- File encryption/decryption
- Password-based key derivation
- Key formatting and parsing
- Invalid input handling
- AES transformation steps
- Validation functions
- Edge cases (empty strings, unicode, large files)

## Data Flow

### Text Encryption Flow
```
User Input → app.py → AESCipher.encrypt_text() → 
PyCryptodome AES → Base64 Encoding → Display to User
```

### Text Decryption Flow
```
User Input → app.py → ValidationHelper → 
AESCipher.decrypt_text() → PyCryptodome AES → Display to User
```

### File Encryption Flow
```
File Upload → FileHandler.encrypt_file_upload() → 
AESCipher.encrypt_file() → PyCryptodome AES → 
Download Button
```

### Visualization Flow
```
User Input → AESVisualizer.demonstrate_round() → 
Transformations → ASCII/Heatmap Display
```

## Configuration

### Session State Variables
- `theme`: Current theme ('dark' or 'light')
- `current_key`: Active AES key (bytes)
- `current_key_size`: Active key size (128, 192, or 256)
- `current_mode`: Active encryption mode ('CBC' or 'ECB')

### Default Settings
- Key Size: 256 bits
- Mode: CBC
- Theme: Dark

## Security Architecture

### Key Management
- Keys generated using cryptographically secure random number generator
- Keys stored in session state (memory only, not persisted)
- Password-based key derivation uses PBKDF2-HMAC-SHA256 with 100,000 iterations
- Salt generation for password-based derivation

### Encryption Implementation
- Uses PyCryptodome library (well-tested cryptographic library)
- Supports industry-standard AES implementation
- PKCS7 padding for block alignment
- IV generation for CBC mode

### Best Practices Implemented
- Unique IVs for each CBC encryption
- No key reuse warnings
- Secure random number generation
- Proper error handling

## Extension Points

### Future Enhancements
1. **Additional Modes**: Add support for GCM, CTR modes
2. **Key Storage**: Implement secure key storage (database, HSM)
3. **Authentication**: Add user authentication
4. **Audit Logging**: Log encryption/decryption operations
5. **API**: REST API for programmatic access
6. **Mobile Support**: Responsive design improvements
7. **Batch Processing**: Encrypt multiple files at once
8. **Cloud Integration**: Direct cloud storage integration

### Customization Points
- Theme colors in app.py CSS
- Educational content in utils.py
- Visualization styles in aes_visualization.py
- Benchmark parameters in utils.py

## Performance Considerations

### Optimization
- PyCryptodome uses optimized C implementations
- Hardware acceleration (AES-NI) when available
- Efficient file handling with streams
- Caching of expensive operations

### Benchmarks
- Text encryption: ~0.5-2 ms per operation
- File encryption: ~50-200 MB/s throughput
- Visualization: Near-instant for single blocks

## Dependencies

### Core Dependencies
- `streamlit>=1.28.0`: Web application framework
- `pycryptodome>=3.19.0`: Cryptographic operations
- `qrcode>=7.4.2`: QR code generation
- `pillow>=10.0.0`: Image processing
- `numpy>=1.24.0`: Numerical operations
- `matplotlib>=3.7.0`: Visualization

### Development Dependencies
- `unittest`: Built-in Python testing framework
- `pytest`: Optional for advanced testing (not included in requirements)

## Deployment

### Local Development
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
streamlit run app.py
```

### Production Deployment
1. Use Streamlit Cloud for easy deployment
2. Or deploy to any server with:
   - Python 3.8+
   - All dependencies installed
   - Reverse proxy (nginx)
   - Process manager (systemd, supervisor)

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

## Maintenance

### Regular Tasks
- Update dependencies for security patches
- Review and update educational content
- Add new test cases for edge cases
- Monitor performance metrics
- Update documentation

### Version Control
- Use semantic versioning (major.minor.patch)
- Maintain CHANGELOG.md for version history
- Tag releases in git

## Support and Troubleshooting

### Common Issues
1. **Import errors**: Ensure all dependencies installed
2. **Streamlit not starting**: Check streamlit installation
3. **QR code errors**: Verify qrcode and pillow installation
4. **Visualization errors**: Check matplotlib and numpy installation

### Debug Mode
Enable debug mode in Streamlit:
```bash
streamlit run app.py --logger.level=debug
```

## License and Attribution

This project is for educational purposes. AES is a NIST standard (FIPS 197). The implementation uses the PyCryptodome library for cryptographic operations.

## Contact and Contributions

For issues, questions, or contributions, please refer to the main README.md file.
