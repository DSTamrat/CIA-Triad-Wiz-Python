from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Import from your other modules
from confidentiality import AccessControl
from integrity import generate_keys
from availability import RateLimiter

# -----------------------------
# CIA ENGINE
# -----------------------------

class CIAEngine:
    def __init__(self, cipher, public_key, private_key, rate_limiter, access_control):
        self.cipher = cipher
        self.public_key = public_key
        self.private_key = private_key
        self.rate_limiter = rate_limiter
        self.access_control = access_control

    def secure_process(self, role: str, action: str, data: bytes):
        # Availability: Rate limiting
        if not self.rate_limiter.allow():
            raise Exception("Rate limit exceeded")

        # Confidentiality: RBAC
        if not self.access_control.allowed(role, action):
            raise PermissionError("Access denied")

        # Confidentiality: Encryption
        encrypted = self.cipher.encrypt(data)

        # Integrity: Digital signature
        signature = self.private_key.sign(
            encrypted,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return encrypted, signature


# -----------------------------
# ENGINE TEST
# -----------------------------

if __name__ == "__main__":
    # Confidentiality: Encryption key
    key = Fernet.generate_key()
    cipher = Fernet(key)

    # Integrity: RSA keys
    private_key, public_key = generate_keys()

    # Availability: Rate limiter
    rl = RateLimiter(limit=10, interval=1)

    # Confidentiality: RBAC
    ac = AccessControl()

    # Create engine
    engine = CIAEngine(cipher, public_key, private_key, rl, ac)

    # Test data
    data = b"Patient record: Jane Doe, ER, Medication Y"

    encrypted, signature = engine.secure_process("doctor", "update_medication", data)

    print("Encrypted:", encrypted)
    print("Signature:", signature)
