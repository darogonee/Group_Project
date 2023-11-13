PRIMES = [702085535438096506588889820143, 524902178649231079293636409829]
def _hash(x):
    return((x + 1) * PRIMES[0]) % PRIMES[1]

def password_hash(password, salt):
    value = 1
    password += salt
    for char in password:
        value = _hash(value + ord(char))
    return value

# this is not the best hash function
# for more secruity you should probaly use a libary
