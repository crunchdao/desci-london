import requests
import json
import pandas as pd

X = pd.read_parquet('features.parquet')

test = 

1/0

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

columns = X.columns
input = X.head(2)

form_data = {}
for i in range(len(columns)):
  form_data[f'feature_{columns[i]}'] = input[i]

variables = {
"owner": "0xFFce501C47FE475954bE6a318740e0793089004F",
"formData": form_data,
"databaseId": "c2e1e9a4-3d07-4e61-b478-a7013d20ffcd"
}

url = "https://dbdao.xyz/api/graphql"
r = requests.post(url, json={'query': query, "variables": variables})