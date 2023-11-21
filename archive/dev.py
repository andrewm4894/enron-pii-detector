#%%

import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def clean_text(text, n_skip_lines=15):
    text_clean = "\n".join(text.split("\n")[n_skip_lines:])
    return text_clean

#%%

# params
openai_model = "gpt-3.5-turbo"
data_path = './data/enron-email-dataset/emails.csv'
nrows = 1000

#%%

# get data
df = pd.read_csv(data_path, nrows=nrows)
print(df.shape)

#%%

df_sample = df.sample(1)
text = df_sample.message.values[0]
print(text)

#%%

text_clean = clean_text(text)
print(text_clean)

#%%

prompt = f"""
perform entirty extraction from the below email message(s).

please return the extracted entities in a long format of key-value pairs like

{{
"<entity-type>": "<entity-value>"
...
}}

```
{text_clean}
```
"""
print(prompt)

#%%

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    model=openai_model,
)
chat_completion_message = chat_completion.choices[0].message

#%%

print(chat_completion_message.content)

#%%

#%%

#%%