import requests
import pandas as pd

url = 'http://127.0.0.1:5000/extract_jd'

file_path = './CS.xlsx'
df = pd.read_excel(file_path)
jd1 = df['岗位要求'][0]
file_path = './data.xlsx'
df2 = pd.read_excel(file_path)
jd2 = df2['岗位要求'][0]

input_data = {'jd': jd1} #input format
response = requests.post(url, json=input_data)
if response.status_code == 200:
    output = response.json()
    print(output)
    print(type(output))
else:
    print(f"Error: {response.status_code}, {response.text}")

input_data = {'jd': jd2}
response = requests.post(url, json=input_data)
if response.status_code == 200:
    output = response.json()
    print(output)
    print(type(output))
else:
    print(f"Error: {response.status_code}, {response.text}")