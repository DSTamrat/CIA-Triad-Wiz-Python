from cryptography.fernet import Fernet

# -----------------------------
# CONFIDENTIALITY: Encryption
# -----------------------------

# Generate and store key securely (Vault, KMS, Azure Key Vault)
key = Fernet.generate_key()
cipher = Fernet(key)

data = b"Patient record: John Doe, ICU, Medication X"
encrypted = cipher.encrypt(data)
decrypted = cipher.decrypt(encrypted)

print("Encrypted:", encrypted)
print("Decrypted:", decrypted)


# -----------------------------
# CONFIDENTIALITY: Multi-Factor Authentication (MFA)
# -----------------------------

import pyotp

# Generate a secret for the user (store securely!)
mfa_secret = pyotp.random_base32()
totp = pyotp.TOTP(mfa_secret)

print("MFA Secret (store in user profile):", mfa_secret)
print("Current MFA Code:", totp.now())

# Example MFA validation function
def validate_mfa(secret, user_code):
    totp = pyotp.TOTP(secret)
    return totp.verify(user_code)

# Simulate user entering MFA code
user_input_code = totp.now()  # In real life, user enters this from Google Authenticator
print("MFA Valid:", validate_mfa(mfa_secret, user_input_code))

# -----------------------------
# CONFIDENTIALITY: AES Example
# -----------------------------

key2 = Fernet.generate_key()
cipher2 = Fernet(key2)
enc = cipher2.encrypt(b"Sensitive Data")
print(enc)

# -----------------------------
# CONFIDENTIALITY: RBAC
# -----------------------------

class AccessControl:
    def __init__(self):
        self.roles = {
            "doctor": ["read_patient", "update_medication"],
            "nurse": ["read_patient"],
            "pharmacist": ["read_patient", "update_medication"],
            "guest": []
        }

    def allowed(self, role, action):
        return action in self.roles.get(role, [])

ac = AccessControl()
print(ac.allowed("doctor", "update_medication"))  # True
print(ac.allowed("guest", "read_patient"))        # False
