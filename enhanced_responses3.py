import requests
import re
import random
from collections import defaultdict, OrderedDict
from urllib.parse import quote
from bs4 import BeautifulSoup


class NeuroLinguisticProcessor:
    def __init__(self):
        self.stop_words = self._load_stop_words()
        self.stem_cache = {}
        self.pos_rules = self._load_pos_rules()
        self.connectors = [
            "Furthermore,", "Moreover,", "Specifically,",
            "Additionally,", "Notably,", "Interestingly,"
        ]

    def _load_stop_words(self):
        """Loads a set of stop words to filter out from extracted concepts."""
        return set([
            "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
            "your", "yours", "yourself", "he", "him", "his", "she", "her", "it",
            "its", "they", "them", "their", "what", "which", "who", "this",
            "that", "these", "those", "am", "is", "are", "was", "were", "be",
            "been", "being", "have", "has", "do", "does", "did", "doing", "a",
            "an", "the", "and", "but", "if", "or", "because", "as", "until",
            "while", "of", "at", "by", "for", "with", "about", "against",
            "between", "to", "from", "up", "down", "in", "out", "on", "off",
            "over", "under", "again", "further", "then", "once", "here", "there",
            "when", "where", "why", "how", "all", "any", "both", "each", "few",
            "more", "most", "other", "some", "such", "no", "nor", "not", "only",
            "own", "same", "so", "than", "too", "very", "s", "t", "can", "will",
            "just", "don", "should", "now"
        ])

    def _load_pos_rules(self):
        """Defines basic POS tagging rules based on word suffixes."""
        return {
            "noun_suffixes": ["tion", "ment", "ness", "ity", "ance", "ence", "hood"],
            "verb_suffixes": ["ize", "ate", "ify", "ing", "ed", "en"],
            "adj_suffixes": ["able", "ible", "al", "ant", "ent", "ic", "ical", "ous"],
            "adv_suffixes": ["ly", "ward", "wise"]
        }

    def _stem(self, word):
        """Applies simple stemming rules to reduce words to their base form."""
        if word not in self.stem_cache:
            step1 = re.sub(r"(ss|i)es$", r"\1", word)
            step2 = re.sub(r"(us|ss)$", r"\1", step1)
            step3 = re.sub(r"(?<=[aeiou])ed$", "", step2)
            self.stem_cache[word] = step3.lower()
        return self.stem_cache[word]

    def extract_concepts(self, text):
        """Extracts key concepts from the given text."""
        tokens = re.findall(r"\b\w+(?:'\w+)?\b", text.lower())
        filtered = [t for t in tokens if t not in self.stop_words]
        return list(OrderedDict.fromkeys(filtered))  # Removes duplicates


class OmniSourceResponseEngine:
    def __init__(self):
        self.nlp = NeuroLinguisticProcessor()
        self.resources = [
            # API Endpoints
            ("https://en.wikipedia.org/api/rest_v1/page/summary/{}", self._parse_wikipedia),
            ("https://api.dictionaryapi.dev/api/v2/entries/en/{}", self._parse_dictionary)
        ]

    def _contextual_score(self, sentence, concepts):
        """Calculates a contextual score for a sentence based on concept overlap."""
        tokens = set(self.nlp._stem(word) for word in re.findall(r"\w+", sentence.lower()))
        matched = [concept for concept in concepts if self.nlp._stem(concept) in tokens]
        return len(matched) / len(concepts)

    def _structure_response(self, sentences, concepts):
        """Structures a response by prioritizing sentences that cover multiple concepts."""
        grouped = defaultdict(list)
        for sent in sentences:
            for concept in concepts:
                if concept.lower() in sent.lower():
                    grouped[concept].append(sent)

        response = []
        covered = set()
        for concept in concepts:
            if concept not in covered:
                candidates = [s for s in grouped[concept] if sum(c in s.lower() for c in concepts) >= 2]
                if candidates:
                    best = max(candidates, key=lambda x: sum(c in x.lower() for c in concepts))
                    response.append(best)
                    covered.update(c for c in concepts if c.lower() in best.lower())

        # Add remaining concepts
        remaining = [c for c in concepts if c not in covered]
        for concept in remaining:
            if grouped[concept]:
                response.append(random.choice(grouped[concept]))

        return " ".join(response) if response else None

    def generate_response(self, query):
        concepts = self.nlp.extract_concepts(query)
        original_order = [c for c in concepts if c.lower() in query.lower()]

        # Fetch content from all sources
        all_content = []
        for base_url, handler in self.resources:
            for concept in concepts:
                try:
                    url = base_url.format(quote(concept))
                    response = requests.get(url, timeout=3)
                    if response.status_code == 200:
                        all_content.extend(handler(response))
                except Exception as e:
                    print(f"Error fetching data for {concept}: {e}")

        # Process and score sentences
        scored = []
        for text in all_content:
            for sentence in re.split(r"(?<=[.!?]) +", text):
                clean_sent = re.sub(r"\s+", " ", sentence).strip()
                if len(clean_sent) > 50:
                    score = self._contextual_score(clean_sent, concepts)
                    scored.append((score, clean_sent))

        scored.sort(reverse=True)
        selected = [s for _, s in scored[:len(concepts) * 2]]

        # Generate coherent response
        final_response = self._structure_response(selected, original_order)

        return final_response or "I couldn't find relevant information for your query."

    # Resource Handlers
    def _parse_wikipedia(self, response):
        """Parses content from Wikipedia API."""
        try:
            data = response.json()
            return [data.get("extract", "")[:500] + "..."]
        except Exception as e:
            print(f"Error parsing Wikipedia response: {e}")
            return []

    def _parse_dictionary(self, response):
        """Parses content from Dictionary API."""
        try:
            data = response.json()
            return [f"Definition: {data[0]['meanings'][0]['definitions'][0]['definition']}"]
        except Exception as e:
            print(f"Error parsing Dictionary response: {e}")
            return []


def enhanced_response_generation(user_input):
    engine = OmniSourceResponseEngine()
    return engine.generate_response(user_input)


# Example Usage
if __name__ == "__main__":
    query = "explain genome integration and viruses"
    print(enhanced_response_generation(query))
