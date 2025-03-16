import os
import re
import json
import time
import random
import requests
import argparse
from bs4 import BeautifulSoup
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style, init
import enhanced_responses3 as er3
import enhanced_responses as er

# Initialize colorama with custom colors
init(autoreset=True)
Fore.BLUE_DARK = "\033[34m"

HEXAGRAMS = [
    ("䷀", "The Creative"), ("䷁", "The Receptive"), ("䷂", "Difficulty at the Beginning"),
    ("䷃", "Youthful Folly"), ("䷄", "Waiting"), ("䷅", "Conflict"),
    ("䷆", "Army"), ("䷇", "Holding Together"), ("䷈", "Small Taming"),
    ("䷉", "Treading"), ("䷊", "Peace"), ("䷋", "Standstill"),
    ("䷌", "Fellowship"), ("䷍", "Great Possession"), ("䷎", "Modesty"),
    ("䷏", "Enthusiasm"), ("䷐", "Following"), ("䷑", "Work on the Decayed"),
    ("䷒", "Approach"), ("䷓", "Contemplation"), ("䷔", "Biting Through"),
    ("䷕", "Grace"), ("䷖", "Splitting Apart"), ("䷗", "Return"),
    ("䷘", "Innocence"), ("䷙", "Great Taming"), ("䷚", "Nourishment"),
    ("䷛", "Great Excess"), ("䷜", "Water"), ("䷝", "Fire"),
    ("䷞", "Clinging Fire"), ("䷟", "Lake"), ("䷠", "Mountain"),
    ("䷡", "Thunder"), ("䷢", "Wind"), ("䷣", "Water over Fire"),
    ("䷤", "Fire over Water"), ("䷥", "Abundance"), ("䷦", "Traveling"),
    ("䷧", "Wandering"), ("䷨", "Pushing Upward"), ("䷩", "Darkening of the Light"),
    ("䷪", "Family"), ("䷫", "Opposition"), ("䷬", "Obstruction"),
    ("䷭", "Deliverance"), ("䷮", "Decrease"), ("䷯", "Increase"),
    ("䷰", "Breakthrough"), ("䷱", "Coming to Meet"), ("䷲", "Gathering"),
    ("䷳", "Pressing Onward"), ("䷴", "Well"), ("䷵", "Revolution"),
    ("䷶", "Cauldron"), ("䷷", "Shock"), ("䷸", "Gentle"),
    ("䷹", "Joyous"), ("䷺", "Dispersing"), ("䷻", "Limiting"),
    ("䷼", "Inner Truth"), ("䷽", "Small Excess"), ("䷾", "After Completion"),
    ("䷿", "Before Completion")
]

class HexagramGrid:
    def __init__(self):
        self.rows = []
        self.color_map = {"red": Fore.RED, "yellow": Fore.YELLOW, "green": Fore.GREEN}
        self.word_bank = []
        self.init_word_bank()
        self.init_grid()

    def init_word_bank(self):
        if os.path.exists("conversation.log"):
            with open("conversation.log", "r") as f:
                text = f.read().lower()
                self.word_bank = re.findall(r"\w+", text)

    def init_grid(self):
        hexagrams = random.sample(HEXAGRAMS, 64)
        for i in range(8):
            row = []
            for j in range(8):
                symbol, name = hexagrams[i * 8 + j]
                row.append({
                    "symbol": symbol,
                    "name": name,
                    "color": random.choice(list(self.color_map.keys())),
                    "position": (i, j),
                    "lines": [self.create_line() for _ in range(6)]
                })
            self.rows.append(row)

    def create_line(self):
        return {
            "state": "closed" if random.random() < 0.5 else "open",
            "word": random.choice(self.word_bank) if self.word_bank else ""
        }

    def display(self):
        for row in self.rows:
            line = []
            for hexagram in row:
                color = self.color_map[hexagram["color"]]
                symbol = hexagram["symbol"]
                lines = "".join(["-" if l["state"] == "closed" else "○" for l in hexagram["lines"]])
                line.append(f"{color}{symbol} {lines}{Style.RESET_ALL}")
            print("  ".join(line))

def fetch_wikipedia_sentences(word):
    try:
        url = f"https://en.wikipedia.org/wiki/{word.capitalize()}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            sentences = [
                re.sub(r"\s+", " ", p.text.strip())
                for p in soup.find_all("p")
            ]
            # Filter out unwanted patterns
            filtered_sentences = [
                s for s in sentences
                if word.lower() in s.lower() and not re.search(r"[\[\]]|\[\d+\]", s)
            ]
            return filtered_sentences[:5]
    except Exception as e:
        print(f"Error fetching Wikipedia for {word}: {e}")
        return []

def generate_response(user_input):
    words = user_input.split()
    all_sentences = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch_wikipedia_sentences, words))

    for result in results:
        if result:
            all_sentences.extend(result)

    # Integrate thinking process (dark blue font)
    print(f"\n{Fore.BLUE_DARK}Processing Query:")
    for sentence in all_sentences[:3]:
        print(f"{Fore.BLUE_DARK}>> {sentence}")
        time.sleep(0.3)

    if not all_sentences:
        return "I couldn't find enough information on your query."

    return " ".join(all_sentences[:3])  # Return the top 3 most relevant sentences.

def start_user_mode():
    hex_grid = HexagramGrid()
    print("Hexagram Interface Initialized\n")
    hex_grid.display()

    while True:
        try:
            user_input = input(f"\n{Fore.RED}[{Fore.WHITE}<{Fore.RED}]: {Fore.GREEN}").strip()
            if not user_input:
                continue

            if user_input.lower() == "explain explain":
                print(f"{Fore.YELLOW}Definition of 'explain': To make something clear by describing it in detail.")
                continue

            response = generate_response(user_input)
            print(f"\n{Fore.GREEN}Response:\n{response}\n")

            hex_grid.display()

        except KeyboardInterrupt:
            print("\nSession Ended.")
            break

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    print(f"{Fore.RED}========={Fore.WHITE} A L E X A N D R I A N {Fore.RED}=========")
    print(f"{Fore.GREEN} ------< {Fore.WHITE}I N T E L L I G E N C E{Fore.GREEN} >------")
    print(f"{Fore.GREEN}   >>>{Fore.BLUE}Scientific Research AI v.10.3{Fore.GREEN}<<<        ")
    start_user_mode()
	
