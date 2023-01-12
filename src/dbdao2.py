import requests
import json
import pandas as pd

X = pd.read_parquet('features.parquet')
print(X.shape)
print(type(X.iloc[0, 0]))

input = X.iloc[0, :]
print(input)

columns = X.columns

form_data = {}
for i in range(len(columns)):
    form_data[f'feature_{columns[i]}'] = input[i]

# y = pd.read_parquet('target.parquet')
# print(y)
print(form_data)

query = '''mutation Mutation($owner: String!, $databaseId: String!, $formData: JSON) {
  createRow(
    owner: $owner, 
    databaseId: $databaseId, 
    formData: $formData
  ) {
    rowId
    rowIdNft
    cid
    owner
    hash
    createdAt
    updatedAt
    formData
  }
}'''

variables = {
  "owner": "0xFFce501C47FE475954bE6a318740e0793089004F",
  "formData": form_data,
  "databaseId": "71dc452f-9727-4ea0-8f96-1613e19df463"
}

url = "https://dbdao.xyz/api/graphql"
r = requests.post(url, json={'query': query, "variables": variables})
json_data = json.loads(r.text)

print(json_data)
# df_data = json_data["data"]["databases"]
# df = pd.DataFrame(df_data)
# print(df)