import os
import json
import base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import passGen  # Imports your generator file!

VAULT_FILE = "secure_vault.enc"

def derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def load_vault(master_password: str):
    if not os.path.exists(VAULT_FILE):
        return {}
    try:
        with open(VAULT_FILE, "rb") as f:
            data = json.load(f)
            salt = base64.b64decode(data["salt"])
            encrypted_data = base64.b64decode(data["encrypted_data"])
            
        key = derive_key(master_password, salt)
        f_cipher = Fernet(key)
        decrypted_data = f_cipher.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
    except (InvalidToken, KeyError):
        return None

def save_vault(vault_data: dict, master_password: str, salt: bytes = None):
    if salt is None:
        salt = os.urandom(16)
    key = derive_key(master_password, salt)
    f_cipher = Fernet(key)
    
    json_data = json.dumps(vault_data).encode()
    encrypted_data = f_cipher.encrypt(json_data)
    
    data_to_save = {
        "salt": base64.b64encode(salt).decode(),
        "encrypted_data": base64.b64encode(encrypted_data).decode()
    }
    with open(VAULT_FILE, "w") as f:
        json.dump(data_to_save, f)

def main():
    print("--- Encrypted Password Vault ---")
    master_password = input("Enter your Master Password to unlock: ").strip()
    
    if os.path.exists(VAULT_FILE):
        vault = load_vault(master_password)
        if vault is None:
            print("\n Incorrect master password!")
            return
        print(" Vault unlocked successfully!")
    else:
        print("No existing vault found. Creating a new encrypted vault with this Master Password.")
        vault = {}
        save_vault(vault, master_password)

    while True:
        print("\n--- Vault Menu ---")
        print("1. View stored services")
        print("2. Get a password")
        print("3. Add/Update a password")
        print("4. Exit Vault")
        
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == '1':
            if not vault:
                print("\nYour vault is currently empty.")
            else:
                print("\nStored Services:")
                for service in vault.keys():
                    print(f"- {service}")
                    
        elif choice == '2':
            service = input("Enter service name (e.g., gmail, github): ").strip().lower()
            if service in vault:
                print(f"\n[+] {service} -> Username: {vault[service]['username']} | Password: {vault[service]['password']}")
            else:
                print(f"\n No credentials found for '{service}'.")
                
        elif choice == '3':
            service = input("Enter service name: ").strip().lower()
            username = input("Enter username/email: ").strip()
            
            gen_choice = input("Would you like to auto-generate a strong password? (y/n): ").strip().lower()
            if gen_choice == 'y':
                password = passGen.generate_password()
                if not password:
                    continue
            else:
                password = input("Enter password: ").strip()
            
            vault[service] = {"username": username, "password": password}
            
            with open(VAULT_FILE, "r") as f:
                existing_data = json.load(f)
                salt = base64.b64decode(existing_data["salt"])
                
            save_vault(vault, master_password, salt)
            print(f"\nCredentials for '{service}' saved and encrypted securely!")
            
        elif choice == '4':
            print("\nClosing vault. Stay safe!")
            break
        else:
            print("Invalid choice. Please select 1 through 4.")

if __name__ == "__main__":
    main()