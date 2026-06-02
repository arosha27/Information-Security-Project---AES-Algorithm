"""
AES Visualization Module
Provides visualization of AES transformation steps for educational purposes:
- SubBytes (S-Box substitution)
- ShiftRows (Row shifting)
- MixColumns (Column mixing)
- AddRoundKey (XOR with round key)
"""

import numpy as np
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap


class AESVisualizer:
    """
    Visualizes AES transformation steps with diagrams and explanations.
    """
    
    # AES S-Box (Substitution Box)
    S_BOX = [
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
    ]
    
    # Inverse S-Box for decryption
    INV_S_BOX = [
        0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
    ]
    
    def __init__(self):
        """Initialize the AES visualizer."""
        pass
    
    def text_to_state(self, text: str) -> np.ndarray:
        """
        Convert text to AES state matrix (4x4).
        
        Args:
            text: Input text (must be 16 characters for one block)
            
        Returns:
            4x4 numpy array representing the state
        """
        # Pad or truncate to 16 bytes
        text_bytes = text.encode('utf-8')[:16]
        if len(text_bytes) < 16:
            text_bytes = text_bytes + b'\x00' * (16 - len(text_bytes))
        
        # Create 4x4 state matrix (column-major order)
        state = np.zeros((4, 4), dtype=int)
        for i in range(16):
            state[i % 4, i // 4] = text_bytes[i]
        
        return state
    
    def sub_bytes(self, state: np.ndarray) -> np.ndarray:
        """
        SubBytes transformation: substitute each byte using S-Box.
        
        Args:
            state: 4x4 state matrix
            
        Returns:
            Transformed state matrix
        """
        result = np.zeros_like(state)
        for i in range(4):
            for j in range(4):
                result[i, j] = self.S_BOX[state[i, j]]
        return result
    
    def shift_rows(self, state: np.ndarray) -> np.ndarray:
        """
        ShiftRows transformation: shift each row left by its index.
        
        Args:
            state: 4x4 state matrix
            
        Returns:
            Transformed state matrix
        """
        result = np.zeros_like(state)
        for i in range(4):
            for j in range(4):
                result[i, j] = state[i, (j + i) % 4]
        return result
    
    def mix_columns(self, state: np.ndarray) -> np.ndarray:
        """
        MixColumns transformation: mix each column using matrix multiplication.
        
        Args:
            state: 4x4 state matrix
            
        Returns:
            Transformed state matrix
        """
        # MixColumns matrix in GF(2^8)
        mix_matrix = np.array([
            [2, 3, 1, 1],
            [1, 2, 3, 1],
            [1, 1, 2, 3],
            [3, 1, 1, 2]
        ])
        
        result = np.zeros_like(state)
        for col in range(4):
            for row in range(4):
                val = 0
                for k in range(4):
                    val ^= self.gf_multiply(mix_matrix[row, k], state[k, col])
                result[row, col] = val
        
        return result
    
    def gf_multiply(self, a: int, b: int) -> int:
        """
        Galois Field multiplication for AES.
        
        Args:
            a: First operand
            b: Second operand
            
        Returns:
            Product in GF(2^8)
        """
        result = 0
        for _ in range(8):
            if b & 1:
                result ^= a
            a <<= 1
            if a & 0x100:
                a ^= 0x11b
            b >>= 1
        return result & 0xff
    
    def add_round_key(self, state: np.ndarray, round_key: np.ndarray) -> np.ndarray:
        """
        AddRoundKey transformation: XOR state with round key.
        
        Args:
            state: 4x4 state matrix
            round_key: 4x4 round key matrix
            
        Returns:
            Transformed state matrix
        """
        return state ^ round_key
    
    def visualize_state(self, state: np.ndarray, title: str = "State Matrix") -> str:
        """
        Create a visual representation of the state matrix.
        
        Args:
            state: 4x4 state matrix
            title: Title for the visualization
            
        Returns:
            ASCII representation of the state
        """
        output = [f"\n{title}"]
        output.append("-" * 50)
        for i in range(4):
            row_str = "| "
            for j in range(4):
                row_str += f"{state[i, j]:02X} | "
            output.append(row_str)
        output.append("-" * 50)
        return "\n".join(output)
    
    def demonstrate_round(self, text: str, round_key: str) -> Dict[str, str]:
        """
        Demonstrate a complete AES round with all transformations.
        
        Args:
            text: Input text (16 characters)
            round_key: Round key as hex string (32 characters)
            
        Returns:
            Dictionary with visualization of each step
        """
        # Convert inputs
        state = self.text_to_state(text)
        key_bytes = bytes.fromhex(round_key)
        key_state = np.zeros((4, 4), dtype=int)
        for i in range(16):
            key_state[i % 4, i // 4] = key_bytes[i]
        
        results = {}
        
        # Initial state
        results['initial'] = self.visualize_state(state, "Initial State")
        
        # SubBytes
        state_sub = self.sub_bytes(state)
        results['subbytes'] = self.visualize_state(state_sub, "After SubBytes")
        
        # ShiftRows
        state_shift = self.shift_rows(state_sub)
        results['shiftrows'] = self.visualize_state(state_shift, "After ShiftRows")
        
        # MixColumns
        state_mix = self.mix_columns(state_shift)
        results['mixcolumns'] = self.visualize_state(state_mix, "After MixColumns")
        
        # AddRoundKey
        state_final = self.add_round_key(state_mix, key_state)
        results['addroundkey'] = self.visualize_state(state_final, "After AddRoundKey")
        
        return results
    
    def get_step_explanation(self, step: str) -> str:
        """
        Get detailed explanation of an AES transformation step.
        
        Args:
            step: Name of the step (initial, subbytes, shiftrows, mixcolumns, addroundkey)
            
        Returns:
            Explanation string
        """
        explanations = {
            'initial': """
**Initial State**

The Initial State represents the plaintext data arranged in a 4×4 matrix format.
Each cell contains one byte (8 bits) of the input data.

- Data is filled column by column (not row by row)
- Total size: 16 bytes = 128 bits = one AES block
- This is the starting point before any transformations are applied

For example, if the input is "ABCDEFGHIJKLMNOP":
- Column 0: A, E, I, M
- Column 1: B, F, J, N
- Column 2: C, G, K, O
- Column 3: D, H, L, P
            """,
            
            'subbytes': """
**SubBytes Transformation**

The SubBytes step is a non-linear substitution operation that replaces each byte 
in the state matrix with a corresponding byte from the AES S-Box (Substitution Box).

- Each byte is treated as two hexadecimal digits (high nibble and low nibble)
- The high nibble selects the row, low nibble selects the column in the S-Box
- The byte at that position becomes the new value

This provides confusion - making the relationship between ciphertext and key 
complex and non-linear.
            """,
            
            'shiftrows': """
**ShiftRows Transformation**

The ShiftRows step cyclically shifts the rows of the state matrix:
- Row 0: No shift
- Row 1: Shift left by 1 byte
- Row 2: Shift left by 2 bytes
- Row 3: Shift left by 3 bytes

This provides diffusion - spreading the influence of each plaintext byte over 
multiple ciphertext bytes.
            """,
            
            'mixcolumns': """
**MixColumns Transformation**

The MixColumns step mixes the data in each column using matrix multiplication 
in the Galois Field GF(2^8).

Each column is multiplied by a fixed matrix:
[2 3 1 1]
[1 2 3 1]
[1 1 2 3]
[3 1 1 2]

This further enhances diffusion by ensuring that changing a single input byte 
affects all four output bytes of the column.
            """,
            
            'addroundkey': """
**AddRoundKey Transformation**

The AddRoundKey step performs a bitwise XOR between the state matrix and a 
round key derived from the encryption key.

- The round key is the same size as the state (16 bytes)
- XOR is used because it's its own inverse (A XOR B XOR B = A)
- This step incorporates the key material into the encryption process

This is the only step that uses the key, making it crucial for security.
            """
        }
        
        return explanations.get(step.lower(), "Unknown step")
    
    def create_comparison_diagram(self, plaintext: str, key: str) -> str:
        """
        Create a text-based comparison diagram showing ECB vs CBC modes.
        
        Args:
            plaintext: Input text
            key: Encryption key
            
        Returns:
            ASCII diagram showing the comparison
        """
        diagram = f"""
{'='*70}
ECB vs CBC Mode Comparison
{'='*70}

Input Plaintext: {plaintext[:30]}...
Key: {key[:16]}...

{'='*70}
ECB (Electronic Codebook) Mode:
{'='*70}
[Block 1] [Block 2] [Block 3] [Block 4]
    |        |        |        |
    v        v        v        v
[Encrypt] [Encrypt] [Encrypt] [Encrypt]
    |        |        |        |
    v        v        v        v
[Cipher1] [Cipher2] [Cipher3] [Cipher4]

Issue: Identical plaintext blocks produce identical ciphertext blocks!

{'='*70}
CBC (Cipher Block Chaining) Mode:
{'='*70}
[Block 1] [Block 2] [Block 3] [Block 4]
    |        |        |        |
    v        v        v        v
[ XOR ]  [ XOR ]  [ XOR ]  [ XOR ]
  | ^       | ^       | ^       | ^
  v |       v |       v |       v |
[IV] |    [C1] |    [C2] |    [C3] |
  |       |       |       |       |
  v       v       v       v       v
[Encrypt] [Encrypt] [Encrypt] [Encrypt]
  |       |       |       |       |
  v       v       v       v       v
[Cipher1] [Cipher2] [Cipher3] [Cipher4]

Advantage: Each block depends on the previous one, preventing patterns!
        """
        return diagram


def create_heatmap(state: np.ndarray, title: str = "State Matrix"):
    """
    Create a heatmap visualization of the state matrix.
    
    Args:
        state: 4x4 state matrix
        title: Title for the heatmap
        
    Returns:
        Matplotlib figure
    """
    fig, ax = plt.subplots(figsize=(6, 5))
    
    # Create custom colormap
    colors = ['#000033', '#000066', '#000099', '#0000CC', '#0000FF', 
              '#3333FF', '#6666FF', '#9999FF', '#CCCCFF', '#FFFFFF']
    cmap = LinearSegmentedColormap.from_list('aes', colors)
    
    # Plot heatmap
    im = ax.imshow(state, cmap=cmap, vmin=0, vmax=255)
    
    # Add text annotations
    for i in range(4):
        for j in range(4):
            text = ax.text(j, i, f'{state[i, j]:02X}',
                          ha="center", va="center", color="white" if state[i, j] < 128 else "black",
                          fontsize=12, fontweight='bold')
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Byte Value (0-255)', rotation=270, labelpad=20)
    
    plt.tight_layout()
    return fig
