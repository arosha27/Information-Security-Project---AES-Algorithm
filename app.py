"""
AES Encryption/Decryption Web Application
Main Streamlit application with modern UI
"""

import streamlit as st
import sys
import os

# Add modules directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from aes_core import AESCipher, compare_modes
from aes_visualization import AESVisualizer, create_heatmap
from utils import (
    FileHandler, QRCodeGenerator, EncryptionBenchmark,
    ThemeManager, ValidationHelper, EducationalContent
)

# Page configuration
st.set_page_config(
    page_title="AES Crypto Dashboard",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'current_key' not in st.session_state:
    st.session_state.current_key = None
if 'current_key_size' not in st.session_state:
    st.session_state.current_key_size = 256
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = 'CBC'

# Apply theme
ThemeManager.apply_theme()

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    section[data-testid="stSidebar"] {
    # background-color: #E8C37D;
    
}
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #1E2130;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        color: white;
    }
    .current-key-box {
    background-color: blue;
    border: 2px solid #6366F1;
    padding: 1rem;
    border-radius: 12px;
    color: white;
}
    .success-box {
        background-color: #0D3B2E;
        border-left: 4px solid #00C853;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: white;
        border-left: 4px solid #FFD600;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #1E2130;
        padding: 1.5rem;
        border-radius: 0.75rem;
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #888;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function."""
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔐 AES Crypto Dashboard")
        
        # Theme toggle
        if st.button(f"🌙 {'Light' if st.session_state.theme == 'dark' else 'Dark'} Mode"):
            ThemeManager.toggle_theme()
            st.rerun()
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigate",
            ["🏠 Dashboard", "📝 Text Encryption", "📁 File Encryption", 
             "📊 Visualization", "📚 Education", "⚡ Benchmark", "🔑 Key Management"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Global settings
        st.markdown("### ⚙️ Settings")
        st.session_state.current_key_size = st.selectbox(
            "Key Size",
            [128, 192, 256],
            index=2,
            help="AES key size in bits"
        )
        
        st.session_state.current_mode = st.selectbox(
            "Encryption Mode",
            ["CBC", "ECB"],
            index=0,
            help="CBC is more secure than ECB"
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        **AES Crypto Dashboard**
        
        A comprehensive tool for AES encryption/decryption with educational visualization.
        
        Version: 1.0.0
        """)
    
    # Main content area
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📝 Text Encryption":
        show_text_encryption()
    elif page == "📁 File Encryption":
        show_file_encryption()
    elif page == "📊 Visualization":
        show_visualization()
    elif page == "📚 Education":
        show_education()
    elif page == "⚡ Benchmark":
        show_benchmark()
    elif page == "🔑 Key Management":
        show_key_management()


def show_dashboard():
    """Show the main dashboard."""
    st.markdown('<h1 class="main-header">AES Encryption Dashboard</h1>', unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">3</div>
            <div class="metric-label">Key Sizes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">2</div>
            <div class="metric-label">Modes</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">4</div>
            <div class="metric-label">AES Steps</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">∞</div>
            <div class="metric-label">Security</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick actions
    st.markdown('<h2 class="sub-header">Quick Actions</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔑 Generate New Key", use_container_width=True):
            cipher = AESCipher(key_size=st.session_state.current_key_size, mode=st.session_state.current_mode)
            key = cipher.generate_key()
            st.session_state.current_key = key
            st.success(f"Generated {st.session_state.current_key_size}-bit key: {cipher.format_key(key)}")
    
    with col2:
        if st.button("📝 Encrypt Text", use_container_width=True):
            st.session_state.navigate_to = "📝 Text Encryption"
            st.rerun()
    
    with col3:
        if st.button("📁 Encrypt File", use_container_width=True):
            st.session_state.navigate_to = "📁 File Encryption"
            st.rerun()
    
    st.markdown("---")
    
    # Current key display
    if st.session_state.current_key:
        cipher = AESCipher(key_size=st.session_state.current_key_size, mode=st.session_state.current_mode)
        st.markdown('<h2 class="sub-header">Current Key</h2>', unsafe_allow_html=True)
        st.markdown(f"""
<div class="current-key-box">
    <strong>Key Size:</strong> {st.session_state.current_key_size} bits<br>
    <strong>Key (Hex):</strong> {cipher.format_key(st.session_state.current_key)}
</div>
""", unsafe_allow_html=True)
        
        # QR code
        qr_generator = QRCodeGenerator()
        qr_image = qr_generator.generate_key_qr_with_metadata(
            cipher.format_key(st.session_state.current_key),
            st.session_state.current_key_size,
            st.session_state.current_mode
        )
        st.image(qr_image, caption="QR Code for Key Sharing", width=200)
    else:
        st.markdown('<h2 class="sub-header">Current Key</h2>', unsafe_allow_html=True)
        st.markdown("""
        <div class="warning-box">
            No key generated yet. Click "Generate New Key" to create one.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Information
    st.markdown('<h2 class="sub-header">About AES</h2>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    <strong>Advanced Encryption Standard (AES)</strong> is a symmetric block cipher 
    that was established by the U.S. National Institute of Standards and Technology (NIST) in 2001.
    
    It operates on 128-bit blocks of data and supports key sizes of 128, 192, or 256 bits.
    AES is widely used worldwide for secure data encryption in various applications.
    </div>
    """, unsafe_allow_html=True)


def show_text_encryption():
    """Show text encryption/decryption interface."""
    st.markdown('<h1 class="main-header">Text Encryption/Decryption</h1>', unsafe_allow_html=True)
    
    # Key management
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔑 Generate New Key"):
            cipher = AESCipher(key_size=st.session_state.current_key_size, mode=st.session_state.current_mode)
            key = cipher.generate_key()
            st.session_state.current_key = key
            st.success(f"Generated {st.session_state.current_key_size}-bit key")
    
    with col2:
        key_input = st.text_input("Or enter key (hex)", placeholder="Enter 32/48/64 hex characters")
        if key_input:
            if ValidationHelper.validate_key(key_input, st.session_state.current_key_size):
                cipher = AESCipher(key_size=st.session_state.current_key_size, mode=st.session_state.current_mode)
                st.session_state.current_key = cipher.parse_key(key_input)
                st.success("Key loaded successfully")
            else:
                st.error(f"Invalid key. Must be {st.session_state.current_key_size // 4} hex characters.")
    
    # Display current key
    if st.session_state.current_key:
        cipher = AESCipher(key_size=st.session_state.current_key_size, mode=st.session_state.current_mode)
        st.info(f"Current Key: {cipher.format_key(st.session_state.current_key)}")
    
    st.markdown("---")
    
    # Encryption/Decryption tabs
    tab1, tab2 = st.tabs(["🔒 Encrypt", "🔓 Decrypt"])
    
    with tab1:
        st.markdown('<h2 class="sub-header">Encrypt Text</h2>', unsafe_allow_html=True)
        
        plaintext = st.text_area("Enter plaintext", height=150, placeholder="Enter text to encrypt...")
        
        if st.button("Encrypt", type="primary"):
            if not st.session_state.current_key:
                st.error("Please generate or enter a key first")
            elif not plaintext:
                st.error("Please enter text to encrypt")
            else:
                try:
                    cipher = AESCipher(key_size=st.session_state.current_key_size, mode=st.session_state.current_mode)
                    ciphertext, iv = cipher.encrypt_text(plaintext, st.session_state.current_key)
                    
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown("**Encrypted Text (Base64):**")
                    st.code(ciphertext, language="text")
                    if iv:
                        st.markdown(f"**IV (Hex):** {iv.hex().upper()}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Copy button
                    if st.button("📋 Copy Ciphertext"):
                        st.session_state.clipboard = ciphertext
                        st.success("Copied to clipboard!")
                    
                except Exception as e:
                    st.error(f"Encryption error: {str(e)}")
    
    with tab2:
        st.markdown('<h2 class="sub-header">Decrypt Text</h2>', unsafe_allow_html=True)
        
        ciphertext = st.text_area("Enter ciphertext (Base64)", height=100, placeholder="Enter Base64-encoded ciphertext...")
        iv_input = st.text_input("IV (Hex) - Required for CBC mode", placeholder="Enter IV as hex string")
        
        if st.button("Decrypt", type="primary"):
            if not st.session_state.current_key:
                st.error("Please generate or enter a key first")
            elif not ciphertext:
                st.error("Please enter ciphertext to decrypt")
            elif st.session_state.current_mode == 'CBC' and not iv_input:
                st.error("IV is required for CBC mode")
            else:
                try:
                    cipher = AESCipher(key_size=st.session_state.current_key_size, mode=st.session_state.current_mode)
                    iv = bytes.fromhex(iv_input) if iv_input else None
                    plaintext = cipher.decrypt_text(ciphertext, st.session_state.current_key, iv)
                    
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.markdown("**Decrypted Text:**")
                    st.code(plaintext, language="text")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Decryption error: {str(e)}")


def show_file_encryption():
    """Show file encryption/decryption interface."""
    st.markdown('<h1 class="main-header">File Encryption/Decryption</h1>', unsafe_allow_html=True)
    
    # Key management
    if st.button("🔑 Generate New Key"):
        cipher = AESCipher(key_size=st.session_state.current_key_size, mode=st.session_state.current_mode)
        key = cipher.generate_key()
        st.session_state.current_key = key
        st.success(f"Generated {st.session_state.current_key_size}-bit key")
    
    # Display current key
    if st.session_state.current_key:
        cipher = AESCipher(key_size=st.session_state.current_key_size, mode=st.session_state.current_mode)
        st.info(f"Current Key: {cipher.format_key(st.session_state.current_key)}")
    
    st.markdown("---")
    
    # Encryption/Decryption tabs
    tab1, tab2 = st.tabs(["🔒 Encrypt File", "🔓 Decrypt File"])
    
    with tab1:
        st.markdown('<h2 class="sub-header">Encrypt File</h2>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose a file to encrypt",
            type=None,
            help="Upload any file for encryption"
        )
        
        if uploaded_file:
            file_info = FileHandler.get_file_info(uploaded_file)
            st.markdown(f"""
            <div class="info-box">
            <strong>File Name:</strong> {file_info['name']}<br>
            <strong>File Size:</strong> {file_info['size']}<br>
            <strong>File Type:</strong> {file_info['type']}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Encrypt File", type="primary"):
                if not st.session_state.current_key:
                    st.error("Please generate a key first")
                else:
                    try:
                        encrypted_data, encrypted_name = FileHandler.encrypt_file_upload(
                            uploaded_file,
                            st.session_state.current_key,
                            mode=st.session_state.current_mode
                        )
                        
                        st.success(f"File encrypted successfully!")
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Encrypted File",
                            data=encrypted_data,
                            file_name=encrypted_name,
                            mime="application/octet-stream"
                        )
                        
                    except Exception as e:
                        st.error(f"Encryption error: {str(e)}")
    
    with tab2:
        st.markdown('<h2 class="sub-header">Decrypt File</h2>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Choose an encrypted file to decrypt",
            type=None,
            help="Upload an encrypted file"
        )
        
        if uploaded_file:
            file_info = FileHandler.get_file_info(uploaded_file)
            st.markdown(f"""
            <div class="info-box">
            <strong>File Name:</strong> {file_info['name']}<br>
            <strong>File Size:</strong> {file_info['size']}
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Decrypt File", type="primary"):
                if not st.session_state.current_key:
                    st.error("Please generate a key first")
                else:
                    try:
                        decrypted_data, decrypted_name = FileHandler.decrypt_file_upload(
                            uploaded_file,
                            st.session_state.current_key,
                            mode=st.session_state.current_mode
                        )
                        
                        st.success(f"File decrypted successfully!")
                        
                        # Download button
                        st.download_button(
                            label="📥 Download Decrypted File",
                            data=decrypted_data,
                            file_name=decrypted_name,
                            mime="application/octet-stream"
                        )
                        
                    except Exception as e:
                        st.error(f"Decryption error: {str(e)}")


def show_visualization():
    """Show AES step visualization."""
    st.markdown('<h1 class="main-header">AES Step Visualization</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    This section demonstrates the individual transformation steps in AES encryption.
    Each step transforms the state matrix in a specific way to achieve security.
    """)
    
    # Input
    col1, col2 = st.columns(2)
    
    with col1:
        text_input = st.text_input(
            "Enter text (16 characters)",
            max_chars=16,
            value="AESVisualization",
            help="Enter exactly 16 characters for one AES block"
        )
    
    with col2:
        key_input = st.text_input(
            "Round Key (32 hex characters)",
            max_chars=32,
            value="2b7e151628aed2a6abf7158809cf4f3c",
            help="Enter 32 hex characters for the round key"
        )
    
    if st.button("🔍 Visualize Steps", type="primary"):
        if len(text_input) != 16:
            st.error("Please enter exactly 16 characters")
        elif len(key_input) != 32:
            st.error("Please enter exactly 32 hex characters")
        else:
            visualizer = AESVisualizer()
            results = visualizer.demonstrate_round(text_input, key_input)
            
            # Display each step
            for step, visualization in results.items():
                st.markdown(f"### {step.replace('_', ' ').title()}")
                st.code(visualization, language="text")
                
                # Add explanation
                explanation = visualizer.get_step_explanation(step)
                with st.expander(f"Learn about {step.replace('_', ' ').title()}"):
                    st.markdown(explanation)
                
                st.markdown("---")
            
            # Create heatmap
            st.markdown("### State Matrix Heatmap")
            state = visualizer.text_to_state(text_input)
            fig = create_heatmap(state, "Initial State Matrix")
            st.pyplot(fig)


def show_education():
    """Show educational content."""
    st.markdown('<h1 class="main-header">Educational Resources</h1>', unsafe_allow_html=True)
    
    edu_content = EducationalContent()
    
    # Tabs for different topics
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔑 Symmetric Key Crypto",
        "⚙️ AES Principles",
        "🛡️ Security",
        "🌍 Applications"
    ])
    
    with tab1:
        st.markdown(edu_content.get_symmetric_key_cryptography_info())
    
    with tab2:
        st.markdown(edu_content.get_aes_working_principles())
    
    with tab3:
        st.markdown(edu_content.get_security_considerations())
    
    with tab4:
        st.markdown(edu_content.get_real_world_applications())


def show_benchmark():
    """Show encryption benchmarking."""
    st.markdown('<h1 class="main-header">Encryption Benchmark</h1>', unsafe_allow_html=True)
    
    if not st.session_state.current_key:
        st.warning("Please generate a key first from the Dashboard or Key Management")
        return
    
    # Benchmark settings
    col1, col2 = st.columns(2)
    
    with col1:
        benchmark_type = st.selectbox(
            "Benchmark Type",
            ["Text Encryption", "File Encryption"]
        )
    
    with col2:
        iterations = st.slider(
            "Iterations",
            min_value=10,
            max_value=1000,
            value=100,
            step=10
        )
    
    st.markdown("---")
    
    if benchmark_type == "Text Encryption":
        st.markdown('<h2 class="sub-header">Text Encryption Benchmark</h2>', unsafe_allow_html=True)
        
        test_text = st.text_area(
            "Test Text",
            value="This is a test text for benchmarking AES encryption performance. " * 10,
            height=100
        )
        
        if st.button("🚀 Run Benchmark", type="primary"):
            with st.spinner("Running benchmark..."):
                benchmark = EncryptionBenchmark()
                results = benchmark.benchmark_text_encryption(
                    test_text,
                    st.session_state.current_key,
                    st.session_state.current_mode,
                    iterations
                )
                
                st.markdown('<h3 class="sub-header">Results</h3>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "Encryption Time",
                        f"{results['encrypt_time_ms']:.3f} ms",
                        help="Average time per encryption operation"
                    )
                    st.metric(
                        "Encryption Throughput",
                        f"{results['encrypt_ops_per_sec']:.1f} ops/sec",
                        help="Number of encryption operations per second"
                    )
                
                with col2:
                    st.metric(
                        "Decryption Time",
                        f"{results['decrypt_time_ms']:.3f} ms",
                        help="Average time per decryption operation"
                    )
                    st.metric(
                        "Decryption Throughput",
                        f"{results['decrypt_ops_per_sec']:.1f} ops/sec",
                        help="Number of decryption operations per second"
                    )
    
    else:
        st.markdown('<h2 class="sub-header">File Encryption Benchmark</h2>', unsafe_allow_html=True)
        
        file_size = st.slider(
            "File Size (KB)",
            min_value=1,
            max_value=1024,
            value=100,
            step=10
        )
        
        if st.button("🚀 Run Benchmark", type="primary"):
            with st.spinner("Running benchmark..."):
                benchmark = EncryptionBenchmark()
                results = benchmark.benchmark_file_encryption(
                    file_size,
                    st.session_state.current_key,
                    st.session_state.current_mode,
                    iterations
                )
                
                st.markdown('<h3 class="sub-header">Results</h3>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric(
                        "Encryption Time",
                        f"{results['encrypt_time_sec']:.3f} sec",
                        help="Total encryption time"
                    )
                    st.metric(
                        "Encryption Throughput",
                        f"{results['encrypt_throughput_mbps']:.2f} MB/s",
                        help="Encryption speed in megabytes per second"
                    )
                
                with col2:
                    st.metric(
                        "Decryption Time",
                        f"{results['decrypt_time_sec']:.3f} sec",
                        help="Total decryption time"
                    )
                    st.metric(
                        "Decryption Throughput",
                        f"{results['decrypt_throughput_mbps']:.2f} MB/s",
                        help="Decryption speed in megabytes per second"
                    )


def show_key_management():
    """Show key management interface."""
    st.markdown('<h1 class="main-header">Key Management</h1>', unsafe_allow_html=True)
    
    # Generate key
    st.markdown('<h2 class="sub-header">Generate New Key</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        key_size = st.selectbox(
            "Key Size",
            [128, 192, 256],
            index=2
        )
    
    with col2:
        if st.button("🔑 Generate Key", type="primary"):
            cipher = AESCipher(key_size=key_size, mode=st.session_state.current_mode)
            key = cipher.generate_key()
            st.session_state.current_key = key
            st.session_state.current_key_size = key_size
            st.success(f"Generated {key_size}-bit key")
    
    # Display current key
    if st.session_state.current_key:
        cipher = AESCipher(key_size=st.session_state.current_key_size, mode=st.session_state.current_mode)
        key_hex = cipher.format_key(st.session_state.current_key)
        
        st.markdown('<h2 class="sub-header">Current Key</h2>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="info-box">
        <strong>Key Size:</strong> {st.session_state.current_key_size} bits<br>
        <strong>Mode:</strong> {st.session_state.current_mode}<br>
        <strong>Key (Hex):</strong> {key_hex}
        </div>
        """, unsafe_allow_html=True)
        
        # QR Code
        st.markdown('<h2 class="sub-header">QR Code for Key Sharing</h2>', unsafe_allow_html=True)
        qr_generator = QRCodeGenerator()
        qr_image = qr_generator.generate_key_qr_with_metadata(
            key_hex,
            st.session_state.current_key_size,
            st.session_state.current_mode
        )
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(qr_image, caption="Scan to share key", width=200)
        with col2:
            st.markdown("""
            <div class="info-box">
            Scan this QR code to share the AES key securely.
            The QR code contains the key along with metadata about key size and mode.
            </div>
            """, unsafe_allow_html=True)
        
        # Download options
        st.markdown('<h2 class="sub-header">Download Key</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📥 Download as Text",
                data=key_hex,
                file_name=f"aes_key_{st.session_state.current_key_size}bit.txt",
                mime="text/plain"
            )
        
        with col2:
            st.download_button(
                label="📥 Download QR Code",
                data=qr_image,
                file_name=f"aes_key_{st.session_state.current_key_size}bit_qr.png",
                mime="image/png"
            )
        
        # Password-based key derivation
        st.markdown("---")
        st.markdown('<h2 class="sub-header">Password-Based Key Derivation</h2>', unsafe_allow_html=True)
        
        password = st.text_input("Enter password", type="password")
        
        if st.button("🔐 Derive Key from Password"):
            if password:
                cipher = AESCipher(key_size=st.session_state.current_key_size, mode=st.session_state.current_mode)
                derived_key, salt = cipher.key_from_password(password)
                st.session_state.current_key = derived_key
                
                st.markdown(f"""
                <div class="success-box">
                <strong>Derived Key:</strong> {cipher.format_key(derived_key)}<br>
                <strong>Salt:</strong> {salt.hex().upper()}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Please enter a password")


if __name__ == "__main__":
    main()
