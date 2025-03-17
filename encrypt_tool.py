import argparse
import json
from src.utils.encryption_utils import EncryptionUtils

def parse_args():
    parser = argparse.ArgumentParser(description='Encrypt or decrypt API keys')
    parser.add_argument('--action', '-a',
                       choices=['encrypt', 'decrypt'],
                       required=True,
                       help='Action to perform: encrypt or decrypt')
    parser.add_argument('--key', '-k',
                       required=True,
                       help='API key to encrypt or encrypted API key to decrypt')
    parser.add_argument('--password', '-p',
                       required=True,
                       help='Password for encryption/decryption')
    return parser.parse_args()

def run_tool():
    args = parse_args()
    
    if args.action == 'encrypt':
        result = EncryptionUtils.encrypt_api_key(args.key, args.password)
        print("\nEncrypted API key:")
        print(result)
    elif args.action == 'decrypt':  # decrypt
        result = EncryptionUtils.decrypt_api_key(args.key, args.password)
        print("\nDecrypted API key:")
        print(result)
            
    else:
        print("No matching action")
    
    return 0

if __name__ == "__main__":
    run_tool()