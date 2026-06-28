from passlib.context import CryptContext
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
plain = "TestPassword123"

# Hash with passlib
passlib_hash = pwd_context.hash(plain)
print("Passlib hash:", passlib_hash)

# Verify with raw bcrypt
is_valid = bcrypt.checkpw(plain.encode('utf-8'), passlib_hash.encode('utf-8'))
print("Bcrypt verify passlib hash:", is_valid)

# Hash with raw bcrypt
raw_hash = bcrypt.hashpw(plain.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
print("Raw hash:", raw_hash)

# Verify with passlib
is_valid2 = pwd_context.verify(plain, raw_hash)
print("Passlib verify raw hash:", is_valid2)
