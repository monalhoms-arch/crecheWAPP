import os

env_path = '.env'
new_public_key = 'test_pk_VpQGDUnbsjLCEFggtkchQaG9VzNpj9vS47bBG2fS'
new_secret_key = 'test_sk_Sp9zY1jA6a4twJoYT92uvmvGoVPKJ3kKXc8XzYPY'

with open(env_path, 'r') as f:
    lines = f.readlines()

with open(env_path, 'w') as f:
    for line in lines:
        if line.startswith('CHARGILY_API_KEY='):
            f.write(f'CHARGILY_API_KEY={new_public_key}\n')
        elif line.startswith('CHARGILY_SECRET_KEY='):
            f.write(f'CHARGILY_SECRET_KEY={new_secret_key}\n')
        else:
            f.write(line)

print("Updated .env successfully")
