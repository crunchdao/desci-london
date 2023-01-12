# https://www.dbdao.xyz/lightpaper
import requests
import json
import pandas as pd
import numpy as np

query = '''query Databases($databaseId: String!) {
  database(databaseId: $databaseId) {
    databaseId
    databaseIdNft
    hash
    owner
    cid
    createdAt
    updatedAt
    schema
    uiSchema
    rows {
      rowId
      rowIdNft
      cid
      owner
      hash
      createdAt
      updatedAt
      formData
    }
  }
}'''

variables = {
  "databaseId": "71dc452f-9727-4ea0-8f96-1613e19df463"
}

url = "https://dbdao.xyz/api/graphql"
r = requests.post(url, json={'query': query, "variables": variables})
json_data = json.loads(r.text)

df_data = json_data["data"]["database"]["rows"]
df = pd.DataFrame(df_data)
df = df.iloc[-1, :]['formData']
# print(df)
df = pd.DataFrame.from_dict(df, orient='index').T
# print(df)

output = np.linalg.norm(df)

assert(output < 5)