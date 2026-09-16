import random
import string

def generate_password():
    print("\n--- Secure Password Generator ---")
    
    while True:
        try:
            length = int(input("Enter password length (minimum 4): "))
            if length >= 4:
                break
            print("Password length must be at least 4 for good security.")
        except ValueError:
            print("Please enter a valid number.")
            
    use_upper = input("Include uppercase letters (A-Z)? (y/n): ").strip().lower() == 'y'
    use_lower = input("Include lowercase letters (a-z)? (y/n): ").strip().lower() == 'y'
    use_nums = input("Include numbers (0-9)? (y/n): ").strip().lower() == 'y'
    use_special = input("Include special characters (!@#$%)? (y/n): ").strip().lower() == 'y'
    
    char_pool = ""
    if use_upper: char_pool += string.ascii_uppercase
    if use_lower: char_pool += string.ascii_lowercase
    if use_nums: char_pool += string.digits
    if use_special: char_pool += string.punctuation
        
    if not char_pool:
        print("\n Error: You must select at least one character type!")
        return None
        
    password_chars = []
    if use_upper: password_chars.append(random.choice(string.ascii_uppercase))
    if use_lower: password_chars.append(random.choice(string.ascii_lowercase))
    if use_nums: password_chars.append(random.choice(string.digits))
    if use_special: password_chars.append(random.choice(string.punctuation))
    
    remaining_length = length - len(password_chars)
    for _ in range(max(0, remaining_length)):
        password_chars.append(random.choice(char_pool))
        
    random.shuffle(password_chars)
    final_password = "".join(password_chars[:length])
    
    print(f"\n Generated Password: {final_password}")
    return final_password

if __name__ == "__main__":
    generate_password()