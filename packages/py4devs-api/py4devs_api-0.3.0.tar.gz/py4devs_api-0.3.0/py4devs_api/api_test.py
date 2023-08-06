from __init__ import *

gen = Generator()

print(f"""
Tests using all available generators:
""")
print(f"CPF: {gen.CPF(True, 'BA')}")
print(f"RG: {gen.RG(True)}")
print(f"CNPJ: {gen.CNPJ(True)}")
print(f"CNH: {gen.CNH()}")
print(f"STATE REGISTRATION: {gen.STATE_REGISTRATION(True, 'BA')}")
print(f"PIS: {gen.PIS(formatting=True)}")
print(f"RENAVAM: {gen.RENAVAM()}")
print(f'''CERTIFICATES:
    BIRTH: {gen.CERTIFICATE(True, "N")}
    MARRIAGE: {gen.CERTIFICATE(True, "C")}
    RELIGIOUS MARRIAGE: {gen.CERTIFICATE(True, "CR")}
    DEATH: {gen.CERTIFICATE(True, "O")}''')
print(f"BANK ACCOUNT: {gen.BANK_ACCOUNT('BA', 'BB')}")
print(f"CREDIT CARD: {gen.CREDIT_CARD(True, 'V16')}")