import pandas as pd

df = pd.read_csv("D:\\AI-BSM\\data\\esg_labeled.csv")

df["total_esg"] = df["env_score"] + df["soc_score"] + df["gov_score"]

def label_esg(score):
    if score < 200:
        return "Low"
    elif score < 600:
        return "Medium"
    else:
        return "High"

df["sustainability_label"] = df["total_esg"].apply(label_esg)

df.to_csv("data/esg_labeled.csv", index=False)

print(df[["document", "total_esg", "sustainability_label"]].head())
