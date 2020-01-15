import pandas as pd
import json

#pd.read_excel('Action_context.xlsx').to_json('action_context_list.json',orient='records')

with open('action_context.json','w') as f:
    f.write(json.dumps(json.loads(pd.read_excel('Action_context.xlsx').to_json(orient='records')), indent=2))