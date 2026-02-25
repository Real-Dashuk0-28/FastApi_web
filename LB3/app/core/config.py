import secrets

TOKENS = frozenset(
    secrets.token_hex(16) for _ in range(5)
)

print(TOKENS)