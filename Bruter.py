"""
BruteForce Password Generator - Optimized and Fixed Version
"""
import time
import colorama
import os
from typing import List, Generator

colorama.init(autoreset=True)
os.system('cls' if os.name == 'nt' else 'clear')

class PasswordGenerator:
    def __init__(self):
        self.base_words: List[str] = []
        self.suffixes: List[str] = ['123', '@123', 'abc', '321', '@abc', '@321']
        self.passwords_generated: int = 0

    def display_banner(self) -> None:
        """Display program banner"""
        print(colorama.Fore.YELLOW + r"""
  ____                     _   ______                              
 |  _ \                   | | |  ____|                             
 | |_) |_ __ ___  __ _  __| | | |__ __ _ _ __   __ _  ___ _ __ ___ 
 |  _ <| '__/ _ \/ _` |/ _` | |  __/ _` | '_ \ / _` |/ _ \ '__/ __|
 | |_) | | |  __/ (_| | (_| | | | | (_| | | | | (_| |  __/ |  \__ \
 |____/|_|  \___|\__,_|\__,_| |_|  \__,_|_| |_|\__, |\___|_|  |___/
                                                 __/ |              
                                                |___/               
        """)

    def get_valid_input(self, prompt: str, valid_options: list) -> str:
        """Get and validate user input"""
        while True:
            user_input = input(prompt).strip()
            if user_input in valid_options:
                return user_input
            print(colorama.Fore.RED + f"Invalid option. Please choose from {valid_options}")

    def collect_personal_info(self) -> None:
        """Collect personal information for password generation"""
        fields = {
            'first name': '',
            'surname': '',
            'nickname': '',
            'birth date (DDMMYY)': '',
            "partner's name": '',
            "partner's nickname": '',
            "pet's name": ''
        }

        print(colorama.Fore.CYAN + "\n[+] Personal Information Collection")
        for field in fields:
            fields[field] = input(f"  > {field.title()}: " + colorama.Fore.WHITE).strip()

        self.base_words.extend(value for value in fields.values() if value)
        self.base_words = list(set(self.base_words))  # Remove duplicates

    def load_wordlist(self, path: str) -> None:
        """Load wordlist from file"""
        try:
            with open(path, 'r', errors='ignore') as f:
                self.base_words = [line.strip() for line in f if line.strip()]
            print(colorama.Fore.GREEN + f"\n[+] Loaded {len(self.base_words)} base words from wordlist")
        except Exception as e:
            print(colorama.Fore.RED + f"\n[!] Error loading wordlist: {str(e)}")
            raise

    def configure_suffixes(self) -> None:
        """Handle suffix configuration"""
        print(colorama.Fore.CYAN + "\n[+] Suffix Configuration")
        options = {
            '1': 'Use default suffixes',
            '2': 'Load suffixes from file',
            '3': 'Enter custom suffixes'
        }
        
        choice = self.get_valid_input(
            "\n".join([f"{k}. {v}" for k, v in options.items()]) + "\nChoose option: ",
            ['1', '2', '3']
        )

        if choice == '2':
            self.load_suffix_file()
        elif choice == '3':
            self.get_custom_suffixes()

    def load_suffix_file(self) -> None:
        """Load suffixes from file"""
        path = input("Enter suffix file path: ").strip()
        try:
            with open(path, 'r') as f:
                self.suffixes = [line.strip() for line in f if line.strip()]
            print(colorama.Fore.GREEN + f"[+] Loaded {len(self.suffixes)} suffixes")
        except Exception as e:
            print(colorama.Fore.RED + f"[!] Error loading suffixes: {str(e)}")
            raise

    def get_custom_suffixes(self) -> None:
        """Get custom suffixes from user"""
        custom = input("Enter suffixes (space-separated): ").strip().split()
        self.suffixes = list(set(custom))  # Remove duplicates
        print(colorama.Fore.GREEN + f"[+] Using {len(self.suffixes)} custom suffixes")

    def generate_combinations(self) -> Generator[str, None, None]:
        """Generate password combinations"""
        for word in self.base_words:
            # Original word variations
            for suffix in self.suffixes:
                self.passwords_generated += 1
                yield f"{word}{suffix}"
                
            # Capitalized word variations
            for suffix in self.suffixes:
                self.passwords_generated += 1
                yield f"{word.capitalize()}{suffix}"

    def save_passwords(self, filename: str) -> None:
        """Save generated passwords to file"""
        try:
            with open(filename, 'w') as f:
                for pwd in self.generate_combinations():
                    f.write(f"{pwd}\n")
            print(colorama.Fore.GREEN + f"\n[+] Saved {self.passwords_generated} passwords to {filename}")
        except Exception as e:
            print(colorama.Fore.RED + f"\n[!] Error saving file: {str(e)}")
            raise

    def show_preview(self) -> None:
        """Show password generation preview"""
        print(colorama.Fore.CYAN + "\n[+] Password Preview")
        preview_generator = self.generate_combinations()
        
        try:
            for _ in range(5):
                print(next(preview_generator))
        except StopIteration:
            print(colorama.Fore.RED + "[!] Not enough combinations to show preview")

    def main_flow(self) -> None:
        """Main program workflow"""
        try:
            self.display_banner()
            
            # Operation mode selection
            mode = self.get_valid_input(
                colorama.Fore.CYAN + "[1] Use existing wordlist\n[2] Create new wordlist\nChoose option (1/2): ",
                ['1', '2']
            )

            if mode == '1':
                path = input("Enter wordlist path: ").strip()
                self.load_wordlist(path)
            else:
                self.collect_personal_info()
                if not self.base_words:
                    raise ValueError("No valid personal information provided")

            # Configure suffixes
            self.configure_suffixes()
            
            # Show generation statistics
            print(colorama.Fore.CYAN + "\n[+] Generation Parameters")
            print(f"Base words: {len(self.base_words)}")
            print(f"Suffixes: {len(self.suffixes)}")
            print(f"Estimated combinations: {len(self.base_words) * len(self.suffixes) * 2}")

            # Preview and save
            self.show_preview()
            
            if input(colorama.Fore.CYAN + "\n[+] Generate and save passwords? (y/n): ").lower() == 'y':
                filename = input("Enter output filename: ").strip()
                self.save_passwords(filename)

        except KeyboardInterrupt:
            print(colorama.Fore.RED + "\n[!] Operation cancelled by user")
        except Exception as e:
            print(colorama.Fore.RED + f"\n[!] Error: {str(e)}")
        finally:
            print(colorama.Fore.YELLOW + "\n[+] Password generation process completed")

if __name__ == "__main__":
    generator = PasswordGenerator()
    generator.main_flow()