import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class EncryptionUtils:
    @staticmethod
    def _get_key_from_password(password: str) -> bytes:
        # Convert password to encryption key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'static_salt',  # In production, use a proper salt
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
        
    @staticmethod
    def encrypt_api_key(api_key: str, encryption_key: str) -> str:
        """Encrypts an API key using the provided encryption key."""
        try:
            key = EncryptionUtils._get_key_from_password(encryption_key)
            f = Fernet(key)
            encrypted_data = f.encrypt(api_key.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()
        except Exception as e:
            raise ValueError(f"Encryption failed: {str(e)}")
            
    @staticmethod
    def decrypt_api_key(encrypted_api_key: str, encryption_key: str) -> str:
        """Decrypts an encrypted API key using the provided encryption key."""
        try:
            key = EncryptionUtils._get_key_from_password(encryption_key)
            f = Fernet(key)
            encrypted_data = base64.urlsafe_b64decode(encrypted_api_key.encode())
            decrypted_data = f.decrypt(encrypted_data)
            return decrypted_data.decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}") 