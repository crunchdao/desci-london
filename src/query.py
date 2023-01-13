# https://www.dbdao.xyz/lightpaper
import requests
import json
import pandas as pd
import numpy as np

query = '''query Databases($databaseId: String!) {
  database(databaseId: $databaseId) {
    rows {
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
print(json_data)
df_data = json_data["data"]["database"]["rows"]
# print(df_data)
df = pd.DataFrame(df_data)
# print(df)
df = df.iloc[-1, :]['formData']
# print(df)
df = pd.DataFrame.from_dict(df, orient='index').T
# print(df)
output = np.linalg.norm(df)
# print(output)
assert(output < 5)