import datetime
import hashlib
import sys

MASTER_SALT = "ARVIND_KUMAR_CSE15_SECRET_2026"

def get_daily_key(date=None):
    if date is None:
        date = datetime.date.today()
    date_str = date.strftime("%Y-%m-%d")
    h = hashlib.sha256(f"{date_str}:{MASTER_SALT}".encode()).hexdigest()
    month_day = date.strftime("%b%d").upper()
    code = h[:5].upper()
    return f"CSE15-{month_day}-{code}"

def xor_encrypt(text, key):
    key_hash = hashlib.sha256(key.encode()).digest()
    result = []
    for i, char in enumerate(text.encode()):
        result.append(char ^ key_hash[i % len(key_hash)])
    return bytes(result).hex()

if __name__ == '__main__':
    # Ensure UTF-8 output on Windows
    sys.stdout.reconfigure(encoding='utf-8')
    today = datetime.date.today()
    today_key = get_daily_key(today)
    print("=" * 55)
    print("      CSE-15 AKINATOR DEVELOPER KEY GENERATOR")
    print("=" * 55)
    print(f"Date:               {today.strftime('%A, %d %B %Y')}")
    print(f"Today's Access Key: {today_key}")
    print("Expiry:             Midnight (23:59:59) tonight")
    print("Telegram Channel:   https://t.me/+SNXgNiPCwMAxMjdl")
    print("=" * 55)
    print("\nCopy & post this message to your Telegram channel:")
    print("-" * 55)
    print(f"🔑 CSE 15 Akinator Access Key for {today.strftime('%d %b %Y')}:")
    print(f"👉 {today_key}")
    print("(Valid today only. Use this key to unlock contact info in the game!)")
    print("-" * 55)
