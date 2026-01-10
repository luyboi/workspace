import requests
import os
import sys

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('BOT_CHAT')

SUSFSCI = os.environ.get('SUSFSCI', 'false')
VFS = os.environ.get('VFS', 'false')
KPM = os.environ.get('KPM', 'false')
ZRAM = os.environ.get('ZRAM', 'false')
KERNELNAME = os.environ.get('KERNELNAME', 'unknown')
UTSVERSION = os.environ.get('UTSVERSION', 'unknown')
KSUVERSION = os.environ.get('KSUVERSION', 'unknown')

def get_caption():
    caption = f"""
```
SukiSU Ultra Build:
KSU: v{KSUVERSION}
KERNEL: {KERNELNAME}
UTS: {UTSVERSION}
SUSFS CI: {SUSFSCI}
VFS: {VFS}
KPM: {KPM}
ZRAM: {ZRAM}
```
[Workflow run]({run_url})
"""
    return caption.strip()

def send_telegram_message(file_path: str):
    if not BOT_TOKEN:
        raise ValueError("Missing BOT_TOKEN env")
    if not os.path.isfile(file_path):
        raise ValueError(f"File not found: {file_path}")
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    caption = get_caption()
    print("Caption:", caption)
    print("---")
    print("Sending...")
    
    with open(file_path, 'rb') as f:
        files = {'document': f}
        data = {
            'chat_id': CHAT_ID,
            'caption': caption,
            'parse_mode': 'Markdown'
        }
        response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        print("Success!")
    else:
        print(f"Error: {response.text}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python bot.py <file>")
        sys.exit(1)
    send_telegram_message(sys.argv[1])
