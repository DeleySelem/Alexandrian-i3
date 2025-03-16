Alexandrian: Scientific Research AI v.10.3

Alexandrian is an interactive command-line application designed to provide enhanced responses to user queries through a combination of hexagram-based visualization and scientific research capabilities. The program integrates real-time data retrieval from APIs, Wikipedia, dictionary services, and other sources, while offering an engaging hexagram grid interface.
Features
1. Hexagram Grid Interface

    Displays a dynamic 8x8 grid of I Ching hexagrams during the session.
    Hexagrams contain lines that can be either "open" (○) or "closed" (-).
    The grid evolves based on user interactions and premonitions derived from recent conversations.

2. Enhanced Response Generation

    Fetches relevant information about user queries from:
        Wikipedia (filtered for readability, removing [, ], and [<number>]).
        Dictionary API for definitions of specific words.
        Additional APIs for trivia, quotes, and random facts (via the enhanced_responses3 and enhanced_responses modules).
    Displays a step-by-step thinking process using dark blue font to indicate how responses are generated.

3. User Feedback Integration

    Stores user feedback on unsatisfactory responses to improve future interactions.
    Saves feedback locally in JSON files (inputs.json and responses.json).

4. Premonitions and Predictions

    Generates premonitions about potential future topics based on conversation logs.
    Updates the hexagram grid visualization based on the accuracy of premonitions.

5. Customizable Behavior

    Explains the word "explain" only when explicitly requested by typing explain explain.

Prerequisites

    Python 3.8+
    The following Python libraries:
        requests
        bs4 (BeautifulSoup)
        colorama
        concurrent.futures

Install the required libraries using:
bash

pip install requests beautifulsoup4 colorama

How to Run

    Clone or download the repository containing this program.

    Navigate to the directory containing server_hexpre3.py.

    Run the program using:
    bash

    python server_hexpre3.py

    The program will display the hexagram grid interface and wait for user input.

    Type your query or command and press Enter. For example:
        Query: "What is genome integration?"
        Command: "explain explain"

    The AI will process your query, display its thinking process, and generate a response.

Example Usage
Startup Screen
excel

========= A L E X A N D R I A N =========
   >>>Scientific Research AI v.10.3<<<        
Hexagram Interface Initialized

User Interaction

    Input:

>: What is dark matter?

Output:
applescript

    Processing Query:
    >> Dark matter is a type of matter thought to account for approximately 85% of the matter in the universe.
    >> It does not interact with electromagnetic radiation, making it invisible to the entire electromagnetic spectrum.
    >> Its presence is inferred from its gravitational effects on visible matter.

    Response:
    Dark matter is a type of matter thought to account for approximately 85% of the matter in the universe. It does not interact with electromagnetic radiation, making it invisible to the entire electromagnetic spectrum. Its presence is inferred from its gravitational effects on visible matter.

angelscript


---

## Key Files

- **`server_hexpre3.py`**: The main program file.
- **`enhanced_responses.py`**: Module for fetching data from DuckDuckGo, dictionary APIs, and other external sources.
- **`enhanced_responses3.py`**: Advanced response engine with linguistic processing and contextual scoring.
- **`conversation.log`**: Log file for storing user interactions.
- **`inputs.json` / `responses.json`**: Local databases for storing user inputs and responses.

---

## Customization

1. **Add More APIs**: Extend the `enhanced_responses3.py` or `enhanced_responses.py` modules to fetch data from additional APIs.
2. **Hexagram Colors**: Modify the `color_map` in the `HexagramGrid` class to customize hexagram colors.
3. **Premonition Logic**: Adjust the `generate_premonitions` function to incorporate more sophisticated predictions.

---

## Known Limitations

- Requires an active internet connection for API calls and Wikipedia access.
- Responses depend on the quality of external data sources.
- The program prioritizes brevity and clarity, which may omit detailed explanations.

---

## Feedback and Contribution

We welcome contributions to improve Alexandrian! If you encounter bugs or have suggestions for new features, feel free to raise an issue or submit a pull request.

---

## License

This program is released under the MIT License. See the `LICENSE` file for details.

--- 

Happy exploring with Alexandrian!
