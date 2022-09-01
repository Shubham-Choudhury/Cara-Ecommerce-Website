# from werkzeug.security import generate_password_hash, check_password_hash

# f1 = generate_password_hash('a')
# print(f1)
# print(check_password_hash(f1, 'a'))

# f2 = generate_password_hash('a')
# print(f2)
# print(check_password_hash(f2, 'a'))

txt = "abc@example.com"

x = txt.split("@")

txt = x[0] + "@google.com"

print(txt) 