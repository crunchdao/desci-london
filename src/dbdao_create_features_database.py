import requests
import json
import pandas as pd

X = pd.read_parquet('features.parquet')

query = '''mutation Mutation($owner: String!, $schema: JSON, $uiSchema: JSON) {
  createDatabase(owner: $owner, schema: $schema, uiSchema: $uiSchema) {
    databaseId
    databaseIdNft
    hash
    owner
    cid
  }
}'''

columns = X.columns

schema_cols = {}
for col in columns:
    schema_cols[f'feature_{col}'] = {
        "type": "number"
      }

schema = {
  "title": "Feature Dataframe",
  "description":"DeSci London Hackaton experimentation.",
  "type": "object",
  "properties": schema_cols
}


variables = {
  "owner": "0xFFce501C47FE475954bE6a318740e0793089004F",
  "schema": schema,
  "uiSchema": {}
}

url = "https://dbdao.xyz/api/graphql"
r = requests.post(url, json={'query': query, "variables": variables})
json_data = json.loads(r.text)

print(json_data)