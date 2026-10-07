import pandas as pd
import hashlib
import json

MASTER_SALT = "ARVIND_KUMAR_CSE15_SECRET_2026"

def xor_encrypt(text, key):
    key_hash = hashlib.sha256(key.encode('utf-8')).digest()
    return bytes([b ^ key_hash[i % len(key_hash)] for i, b in enumerate(str(text).encode('utf-8'))]).hex()

df = pd.read_csv('students.csv')

# Ensure Bhavya Singh is F
df.loc[df['Name'].str.strip() == 'Bhavya Singh', 'Gender'] = 'F'

records = []
for _, row in df.iterrows():
    name = row['Name'].strip()
    roll = str(row['Roll No']).strip()
    phone = str(row['Student Mobile No']).strip()
    
    first_letter = name[0].upper()
    second_letter = name[1].upper() if len(name) > 1 else ''
    words = len(name.split())
    last_digit = int(roll[-1])
    
    # Encrypt phone number using MASTER_SALT + roll
    enc_phone = xor_encrypt(phone, f"{MASTER_SALT}:{roll}")
    
    records.append({
        'roll_no': roll,
        'name': name,
        'gender': row['Gender'],
        'first_letter': first_letter,
        'second_letter': second_letter,
        'words_count': words,
        'roll_last': last_digit,
        'prev_section': row['Previous Section'],
        'new_section': row['New Section'],
        'enc_phone': enc_phone
    })

with open('students.json', 'w', encoding='utf-8') as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print(f"Generated secure students.json with {len(records)} students.")
