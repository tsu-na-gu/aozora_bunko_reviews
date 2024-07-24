import rdflib
import pandas as pd

# TTLファイルの読み込み
ttl_file = 'reviews/management/commands/ndc9.ttl'
g = rdflib.Graph()
g.parse(ttl_file, format='ttl')

# データを抽出
data = []

for s, p, o in g:
    if p == rdflib.URIRef("http://www.w3.org/2004/02/skos/core#notation"):
        ndc_code = str(o)
        data.append({'subject': str(s), 'ndc_code': ndc_code})
    elif p == rdflib.URIRef("http://www.w3.org/2004/02/skos/core#broader"):
        broader_code = str(o).split(':')[-1]
        data.append({'subject': str(s), 'broader_code': broader_code})

# pandas DataFrameに変換
df = pd.DataFrame(data)

# ndc_codeとbroader_codeの長さを確認
df['ndc_code_length'] = df['ndc_code'].apply(len)
df['broader_code_length'] = df['broader_code'].apply(len)

# 長さが10を超えるデータを確認
long_ndc_codes = df[df['ndc_code_length'] > 10]
long_broader_codes = df[df['broader_code_length'] > 10]

print("NDCコードが10桁を超えるデータ:\n", long_ndc_codes)
print("broader_codeが10桁を超えるデータ:\n", long_broader_codes)