# hello-world

"This repository is for practicing the GitHub Flow."
I'm new to this coding and developer stuff trying to learn

## 🔒 Encryption/Decryption Program

A Python program that lets you securely encrypt and decrypt text messages and files using military-grade AES-256 encryption. Perfect for keeping your secrets safe!

### Features

- ✅ **Encrypt text messages** - Hide sensitive text with a password
- ✅ **Decrypt text messages** - Reveal hidden messages with the correct password
- ✅ **Encrypt files** - Protect any file (documents, images, videos, etc.)
- ✅ **Decrypt files** - Restore encrypted files to their original form
- ✅ **Strong security** - Uses AES-256 encryption (same as banks and governments)
- ✅ **Easy to use** - Simple menu-driven interface

### Installation

1. Make sure you have Python 3.7 or higher installed:
   ```bash
   python3 --version
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Run the program:
```bash
python3 encryptor.py
```

You'll see a menu with options:

```
🔒 ENCRYPTION/DECRYPTION PROGRAM 🔒
Secure AES-256 encryption for text and files

What would you like to do?
  1. Encrypt text
  2. Decrypt text
  3. Encrypt file
  4. Decrypt file
  5. Exit
```

### Examples

#### Encrypting Text
1. Choose option `1` from the menu
2. Enter a password (this password will be needed to decrypt later)
3. Type the text you want to encrypt
4. The encrypted text will be displayed
5. Optionally save it to a file

#### Decrypting Text
1. Choose option `2` from the menu
2. Enter the same password you used to encrypt
3. Paste the encrypted text or load it from a file
4. Your original text will be displayed

#### Encrypting a File
1. Choose option `3` from the menu
2. Enter a password
3. Enter the path to the file you want to encrypt (e.g., `secret.txt`)
4. The encrypted file will be saved as `secret.txt.enc`

#### Decrypting a File
1. Choose option `4` from the menu
2. Enter the same password you used to encrypt
3. Enter the path to the encrypted file (e.g., `secret.txt.enc`)
4. The original file will be restored

### Security Notes

- **Keep your password safe!** If you forget your password, you cannot decrypt your data.
- Use strong passwords with a mix of letters, numbers, and symbols
- The program uses AES-256 encryption with PBKDF2 key derivation (100,000 iterations)
- Each encryption uses a unique random salt and IV for maximum security

### How It Works

The program uses:
- **AES-256**: Advanced Encryption Standard with 256-bit keys
- **CBC Mode**: Cipher Block Chaining for secure encryption
- **PBKDF2**: Password-Based Key Derivation Function 2 with SHA-256
- **Random Salt & IV**: Ensures each encryption is unique, even with the same password

### Troubleshooting

**"Decryption failed. Wrong password or corrupted data."**
- Make sure you're using the exact same password you used to encrypt
- Passwords are case-sensitive
- Check that the encrypted data hasn't been modified

**"Module not found: cryptography"**
- Install dependencies: `pip install -r requirements.txt`

**"Permission denied"**
- Make sure you have read/write permissions for the files

### Files in This Repository

- `encryptor.py` - Main encryption/decryption program
- `requirements.txt` - Python dependencies
- `README.md` - This file

---

Stay secure! 🔐
