import pandas as pd
import numpy as np
import random
toxic_comment = [
    "You ar dumb","this is trash","horable sound","loser"
]

supportive_comment = [
    "help me a lot","you are amazing","best knowladge","helpfull"
]

data = []

for i in range(50):
    data.append({"comment":random.choice(toxic_comment), "label" : "toxic"})
    data.append({"comment":random.choice(supportive_comment), "label" : "support"})
    
    
    
df = pd.DataFrame(data)
df.to_csv("youtube_comments.csv",index=False)
print("✅ Data save Successfully")
