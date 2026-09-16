# Simple Python Password Tools

* `password_generator.py` - Generates random passwords. You can pick the length and choose whether you want uppercase letters, lowercase, numbers, or symbols.
* `password_checker.py` - Takes a password, tests it, and gives you a score and some quick tips on how to make it stronger.
* `password_vault.py` - A basic local encrypted vault. It's locked behind a master password so you can store and look up passwords when you need them. It also calls the generator script if you want to make a new password on the spot.

# Setup
The vault script uses the cryptography library to keep things encrypted. You'll need to install that first if you haven't yet:

```bash
pip install cryptography