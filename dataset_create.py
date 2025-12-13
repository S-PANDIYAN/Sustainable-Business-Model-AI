import os
import pandas as pd

ESG_KEYWORDS = {
    "environment": ["carbon", "emission", "renewable", "energy", "waste", "climate"],
    "social": ["job", "community", "health", "education", "safety"],
    "governance": ["ethics", "compliance", "transparency", "policy", "audit"]
}

def extract_features(text):
    text = text.lower()
    return {
        "env_score": sum(text.count(w) for w in ESG_KEYWORDS["environment"]),
        "soc_score": sum(text.count(w) for w in ESG_KEYWORDS["social"]),
        "gov_score": sum(text.count(w) for w in ESG_KEYWORDS["governance"]),
    }

rows = []

# Process SDG and Circular Economy reports from pdf_to_text folder
pdf_to_text_path = "D:\\AI-BSM\\pdf_to_text"

# SDG report
sdg_file = os.path.join(pdf_to_text_path, "The-Sustainable-Development-Goals-Report-2025.txt")
if os.path.exists(sdg_file):
    with open(sdg_file, "r", encoding="utf-8") as f:
        text = f.read()
    features = extract_features(text)
    features["source"] = "sdg"
    features["document"] = "The-Sustainable-Development-Goals-Report-2025.txt"
    rows.append(features)

# Circular Economy report
circular_file = os.path.join(pdf_to_text_path, "Towards the circular economy - Vol 2.txt")
if os.path.exists(circular_file):
    with open(circular_file, "r", encoding="utf-8") as f:
        text = f.read()
    features = extract_features(text)
    features["source"] = "circular"
    features["document"] = "Towards the circular economy - Vol 2.txt"
    rows.append(features)

# GRI Standards from extracted_text folder
gri_folder = os.path.join(pdf_to_text_path, "extracted_text")
if os.path.exists(gri_folder):
    for file in os.listdir(gri_folder):
        if file.endswith(".txt"):
            with open(os.path.join(gri_folder, file), "r", encoding="utf-8") as f:
                text = f.read()
            features = extract_features(text)
            features["source"] = "gri"
            features["document"] = file
            rows.append(features)

df = pd.DataFrame(rows)
df.to_csv("data/esg_features.csv", index=False)