import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# -----------------------------
# INTEGRITY: Hashing
# -----------------------------

def sha256_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

data = b"Critical lab result: Potassium = 6.1"
print("SHA-256 Hash:", sha256_hash(data))

# -----------------------------
# INTEGRITY: Digital Signatures
# -----------------------------

# Generate RSA keys
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

message = b"Medication order updated"

# Sign the message
signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

print("Signature:", signature)

# Verify the signature
public_key.verify(
    signature,
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

print("Signature verified successfully!")
