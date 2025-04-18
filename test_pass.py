from helper.crypto_password import generate_key,encrypt_password,decrypt_password,create_key,open_key,verify_password

def create_password():
    key_secret = open_key()
    password = "Password12345!"
    e_pass = encrypt_password(key_secret,password)
    d_pass = decrypt_password(key_secret,e_pass)
    db_pass = "gAAAAABn7SVDm_hAXAVYnYmix7BPHDBjZIaiG3xkkSd6RaOdQn6eY61HGO40F6ESzhf7x8v3BwaW5TFTPsQ6yPpJXAe_x4IsCA=="
    verify = verify_password(key_secret,password,db_pass)
    return e_pass,d_pass,key_secret,verify

epass = create_password()[0]
dpass = create_password()[1]
key = create_password()[2]
verify = create_password()[3]
print(epass)
print(dpass)
print(key)
print(verify)