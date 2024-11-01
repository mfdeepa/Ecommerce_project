import random
import string
import base64
import hashlib


def generate_code_verifier_and_challenge():
    code_verifier = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))

    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')
    print("code challenge:", code_challenge)
    print("code_verifier:", code_verifier)
    return code_verifier, code_challenge
