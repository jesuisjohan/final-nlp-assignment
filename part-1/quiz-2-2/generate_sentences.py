import csv
import itertools
from typing import Dict, List
import random
from underthesea import sentiment

MAX_COUNT = 10000

def read_grammar_rules(file_name: str) -> Dict[str, List[str]]:
    grammar = {}
    with open(file_name, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rule = row["Rule"]
            expansion = row["Expansion"]
            grammar[rule] = expansion.split("|")
    return grammar


def generate_sentences(symbol: str, grammar: Dict[str, List[str]], depth: int = 0) -> List[str]:
    if depth > 10:
        return [""]

    if symbol not in grammar:
        return [symbol]

    sentences = []
    for expansion in grammar[symbol]:
        components = expansion.split()
        if len(components) == 1:
            sentences.extend(generate_sentences(components[0], grammar, depth + 1))
        else:
            component_sentences = [generate_sentences(component, grammar, depth + 1) for component in components]
            for sentence_combination in itertools.product(*component_sentences):
                if random.random() < 0.5:
                    sentences.append(" ".join(sentence_combination))

    return sentences


grammar_rules = read_grammar_rules("../output/grammar.txt")

sentences = generate_sentences("S", grammar_rules)

with open("../output/samples.txt", "w", encoding="utf-8") as f:
    # In ra các câu sinh ra
    
    count = 0
    
    for sentence in sentences:
        if (count >= MAX_COUNT):
            break
        
        if sentiment(sentence) == "negative":
            continue
        f.write(sentence + "\n")
        
        count += 1
