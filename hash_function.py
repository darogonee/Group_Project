PRIMES = [2347692443, 88763557]

def random_hash(x):
    return((x + 1) * PRIMES[0]) % PRIMES[1]

def password_hash(password):
    value = 1
    for char in password:
        value = random_hash(value) + ord(char)
    return value

print(password_hash("ABC"))
print(password_hash("BCA"))