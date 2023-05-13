from underthesea import pos_tag, sent_tokenize
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import csv


def create_grammar_rules(tagged_sentences: List[List[Tuple[str, str]]]) -> Dict[str, Set[str]]:
    rules: defaultdict[str, Set[str]] = defaultdict(set)

    for sentence in tagged_sentences:
        for i, (word, tag) in enumerate(sentence):
            if i == 0:
                rules["S"].add(tag)
            rules[tag].add(word)

    return rules


def write_grammar_rules_to_csv(grammar_rules: Dict[str, Set[str]], csv_file: str) -> None:
    with open(csv_file, "w", encoding="utf-8", newline="") as csv_output:
        csv_writer = csv.writer(csv_output)
        csv_writer.writerow(["Rule", "Expansion"])

        sorted_rules = sorted(grammar_rules.items(), key=lambda x: x[0])

        for rule, expansions in sorted_rules:
            sorted_expansions = sorted(expansions)
            csv_writer.writerow([rule, "|".join(sorted_expansions)])


with open("input/sentences.txt", "r", encoding="utf-8") as input_file:
    paragraphs: List[str] = input_file.readlines()

sentences: List[str] = []

for p in paragraphs:
    processed_paragraph: str = p.strip()
    sentences.extend(sent_tokenize(processed_paragraph))

tagged_sentences: List[List[Tuple[str, str]]] = [pos_tag(sentence) for sentence in sentences]
grammar_rules: Dict[str, Set[str]] = create_grammar_rules(tagged_sentences)
write_grammar_rules_to_csv(grammar_rules, "grammar_rules.csv")
