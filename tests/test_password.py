from app.core.security import hash_password, verify_password

password = "MyTestPassword123!"

hashed = hash_password(password)

print("Hash: ", hashed)
print("Correct Pswd: ", verify_password(password,hashed))
print("Incorrect Pswd: ", verify_password("Wrongpass",hashed))