#!/usr/bin/env python3
"""
Encryption/Decryption Program
A simple yet secure program to encrypt and decrypt text and files using AES-256 encryption.
"""

import os
import sys
import base64
import getpass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class Encryptor:
    """Handles encryption and decryption operations using AES-256."""

    def __init__(self, password: str):
        """
        Initialize the encryptor with a password.

        Args:
            password: The password used for encryption/decryption
        """
        self.password = password.encode()

    def _derive_key(self, salt: bytes) -> bytes:
        """
        Derive a cryptographic key from the password using PBKDF2.

        Args:
            salt: Random salt for key derivation

        Returns:
            32-byte key for AES-256
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(self.password)

    def encrypt_text(self, plaintext: str) -> str:
        """
        Encrypt a text string.

        Args:
            plaintext: The text to encrypt

        Returns:
            Base64-encoded encrypted text with salt and IV
        """
        # Generate random salt and IV
        salt = os.urandom(16)
        iv = os.urandom(16)

        # Derive key from password
        key = self._derive_key(salt)

        # Create cipher and encrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()

        # Pad the plaintext to be multiple of 16 bytes
        plaintext_bytes = plaintext.encode()
        padding_length = 16 - (len(plaintext_bytes) % 16)
        padded_plaintext = plaintext_bytes + bytes([padding_length] * padding_length)

        # Encrypt
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

        # Combine salt + iv + ciphertext and encode to base64
        encrypted_data = salt + iv + ciphertext
        return base64.b64encode(encrypted_data).decode()

    def decrypt_text(self, encrypted_text: str) -> str:
        """
        Decrypt an encrypted text string.

        Args:
            encrypted_text: Base64-encoded encrypted text

        Returns:
            Decrypted plaintext
        """
        try:
            # Decode from base64
            encrypted_data = base64.b64decode(encrypted_text.encode())

            # Extract salt, IV, and ciphertext
            salt = encrypted_data[:16]
            iv = encrypted_data[16:32]
            ciphertext = encrypted_data[32:]

            # Derive key from password
            key = self._derive_key(salt)

            # Create cipher and decrypt
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()

            # Decrypt
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            # Remove padding
            padding_length = padded_plaintext[-1]
            plaintext = padded_plaintext[:-padding_length]

            return plaintext.decode()
        except Exception as e:
            raise ValueError("Decryption failed. Wrong password or corrupted data.") from e

    def encrypt_file(self, input_file: str, output_file: str = None):
        """
        Encrypt a file.

        Args:
            input_file: Path to the file to encrypt
            output_file: Path for the encrypted file (defaults to input_file + .enc)
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")

        if output_file is None:
            output_file = input_file + ".enc"

        # Read the file
        with open(input_file, 'rb') as f:
            plaintext = f.read()

        # Generate random salt and IV
        salt = os.urandom(16)
        iv = os.urandom(16)

        # Derive key from password
        key = self._derive_key(salt)

        # Create cipher and encrypt
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()

        # Pad the plaintext
        padding_length = 16 - (len(plaintext) % 16)
        padded_plaintext = plaintext + bytes([padding_length] * padding_length)

        # Encrypt
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()

        # Write salt + iv + ciphertext to output file
        with open(output_file, 'wb') as f:
            f.write(salt + iv + ciphertext)

        print(f"✓ File encrypted successfully: {output_file}")

    def decrypt_file(self, input_file: str, output_file: str = None):
        """
        Decrypt an encrypted file.

        Args:
            input_file: Path to the encrypted file
            output_file: Path for the decrypted file (defaults to input_file without .enc)
        """
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input file not found: {input_file}")

        if output_file is None:
            if input_file.endswith('.enc'):
                output_file = input_file[:-4]
            else:
                output_file = input_file + ".dec"

        try:
            # Read the encrypted file
            with open(input_file, 'rb') as f:
                encrypted_data = f.read()

            # Extract salt, IV, and ciphertext
            salt = encrypted_data[:16]
            iv = encrypted_data[16:32]
            ciphertext = encrypted_data[32:]

            # Derive key from password
            key = self._derive_key(salt)

            # Create cipher and decrypt
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()

            # Decrypt
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            # Remove padding
            padding_length = padded_plaintext[-1]
            plaintext = padded_plaintext[:-padding_length]

            # Write to output file
            with open(output_file, 'wb') as f:
                f.write(plaintext)

            print(f"✓ File decrypted successfully: {output_file}")
        except Exception as e:
            raise ValueError("Decryption failed. Wrong password or corrupted file.") from e


def print_banner():
    """Print a welcome banner."""
    print("\n" + "="*60)
    print("  🔒 ENCRYPTION/DECRYPTION PROGRAM 🔒")
    print("  Secure AES-256 encryption for text and files")
    print("="*60 + "\n")


def print_menu():
    """Print the main menu."""
    print("\nWhat would you like to do?")
    print("  1. Encrypt text")
    print("  2. Decrypt text")
    print("  3. Encrypt file")
    print("  4. Decrypt file")
    print("  5. Exit")
    print()


def main():
    """Main program loop."""
    print_banner()

    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '5':
            print("\n👋 Goodbye! Stay secure!")
            break

        if choice not in ['1', '2', '3', '4']:
            print("❌ Invalid choice. Please try again.")
            continue

        # Get password
        password = getpass.getpass("\n🔑 Enter password: ")
        if not password:
            print("❌ Password cannot be empty.")
            continue

        encryptor = Encryptor(password)

        try:
            if choice == '1':
                # Encrypt text
                text = input("\n📝 Enter text to encrypt: ")
                if not text:
                    print("❌ Text cannot be empty.")
                    continue

                encrypted = encryptor.encrypt_text(text)
                print(f"\n✓ Encrypted text:\n{encrypted}\n")

                # Ask if user wants to save to file
                save = input("Save to file? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("Enter filename: ").strip()
                    if filename:
                        with open(filename, 'w') as f:
                            f.write(encrypted)
                        print(f"✓ Saved to {filename}")

            elif choice == '2':
                # Decrypt text
                print("\n📝 Enter encrypted text (or press Enter to read from file):")
                encrypted = input().strip()

                if not encrypted:
                    filename = input("Enter filename to read from: ").strip()
                    if not filename:
                        print("❌ No input provided.")
                        continue
                    try:
                        with open(filename, 'r') as f:
                            encrypted = f.read().strip()
                    except FileNotFoundError:
                        print(f"❌ File not found: {filename}")
                        continue

                decrypted = encryptor.decrypt_text(encrypted)
                print(f"\n✓ Decrypted text:\n{decrypted}\n")

            elif choice == '3':
                # Encrypt file
                input_file = input("\n📁 Enter file path to encrypt: ").strip()
                output_file = input("Enter output file path (press Enter for default): ").strip()

                if not output_file:
                    output_file = None

                encryptor.encrypt_file(input_file, output_file)

            elif choice == '4':
                # Decrypt file
                input_file = input("\n📁 Enter encrypted file path: ").strip()
                output_file = input("Enter output file path (press Enter for default): ").strip()

                if not output_file:
                    output_file = None

                encryptor.decrypt_file(input_file, output_file)

        except FileNotFoundError as e:
            print(f"\n❌ Error: {e}")
        except ValueError as e:
            print(f"\n❌ Error: {e}")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
