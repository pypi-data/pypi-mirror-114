import os
import torch
import yaml
from transformers import AutoTokenizer


PYEUROVOC_PATH = os.path.join(os.path.expanduser("~"), ".cache", "pyeurovoc")
REPOSITORY_URL = ""

DICT_MODELS = {
    "bg": "TurkuNLP/wikibert-base-bg-cased",
    "cs": "TurkuNLP/wikibert-base-cs-cased",
    "da": "Maltehb/danish-bert-botxo",
    "de": "bert-base-german-cased",
    "el": "nlpaueb/bert-base-greek-uncased-v1",
    "en": "nlpaueb/legal-bert-base-uncased",
    "es": "dccuchile/bert-base-spanish-wwm-cased",
    "et": "tartuNLP/EstBERT",
    "fi": "TurkuNLP/bert-base-finnish-cased-v1",
    "fr": "camembert-base",
    "hu": "SZTAKI-HLT/hubert-base-cc",
    "it": "dbmdz/bert-base-italian-cased",
    "lt": "TurkuNLP/wikibert-base-lt-cased",
    "lv": "TurkuNLP/wikibert-base-lv-cased",
    "mt": "bert-base-multilingual-cased",
    "nl": "wietsedv/bert-base-dutch-cased",
    "pl": "dkleczek/bert-base-polish-cased-v1",
    "pt": "neuralmind/bert-base-portuguese-cased",
    "ro": "dumitrescustefan/bert-base-romanian-cased-v1",
    "sk": "TurkuNLP/wikibert-base-sk-cased",
    "sl": "TurkuNLP/wikibert-base-sl-cased",
    "sv": "KB/bert-base-swedish-cased"
}


class EuroVocBERT:
    def __init__(self, lang="en"):
        if not os.path.exists(PYEUROVOC_PATH):
            os.makedirs(PYEUROVOC_PATH)

        # model must be downloaded from the repostiory
        if not os.path.exists(os.path.join(PYEUROVOC_PATH, f"model_{lang}.pt")):
            print(f"Model 'model_{lang}.pt' not found in the .cache directory at '{PYEUROVOC_PATH}'")
            print(f"Downloading 'model_{lang}.pt from {REPOSITORY_URL}...")
        # model already exists, loading from .cache directory
        else:
            print(f"Model 'model_{lang}.pt' found in the .cache directory at '{PYEUROVOC_PATH}'")
            print("Loading model...")

        # load the model
        self.model = torch.load(os.path.join(PYEUROVOC_PATH, f"model_{lang}.pt"))

        # load the tokenizer according to the model dictionary
        self.tokenizer = AutoTokenizer.from_pretrained(DICT_MODELS[lang])

    def __call__(self, document_text, num_id_labels=6, num_mt_labels=5, num_do_labels=4):
        encoding_ids = self.tokenizer.encode(
            document_text,
            return_attention_mask=True,
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )
