import string
import re

def check_password_strength(password):
    score = 0
    feedback = []
    
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
        feedback.append("Consider making the password at least 12 characters long.")
    else:
        feedback.append("Password is too short (must be at least 8 characters).")
        
    if re.search(r"[a-z]", password): score += 1
    else: feedback.append("Add lowercase letters (a-z).")
        
    if re.search(r"[A-Z]", password): score += 1
    else: feedback.append("Add uppercase letters (A-Z).")
        
    if re.search(r"\d", password): score += 1
    else: feedback.append("Add numbers (0-9).")
        
    if re.search(f"[{re.escape(string.punctuation)}]", password): score += 1
    else: feedback.append("Add special characters (e.g., !, @, #, $).")
        
    if score >= 5: rating = "Strong"
    elif score >= 3: rating = "Moderate"
    else: rating = "Weak"
        
    return rating, score, feedback

if __name__ == "__main__":
    print("--- Password Strength Checker ---")
    pwd = input("Enter a password to test: ")
    rating, score, feedback = check_password_strength(pwd)
    
    print(f"\nResults:")
    print(f"Strength Rating: {rating} (Score: {score}/6)")
    if feedback:
        print("\nSuggestions to improve:")
        for tip in feedback:
            print(f"- {tip}")
    else:
        print("\nGreat job! This is a robust and secure password.")