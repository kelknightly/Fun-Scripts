import pandas as pd
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 200)

df = pd.read_csv('OECD-WTO_BATIS_data.csv', low_memory=False)
economies = pd.read_csv('wto_economies.csv', encoding='latin-1')

recent = df.loc[(df['Year'] == 2012) & (df['Item_code'] == 'S205'),
                ['Reporter', 'Partner', 'Year', 'Flow', 'Balanced_value', 'Item_code']]

recent_economies = pd.merge(recent, economies, how='inner', left_on='Partner', right_on='COUNTRY_CODE')
recent_economies = pd.merge(recent_economies, economies, how='inner', left_on='Reporter', right_on='COUNTRY_CODE')
recent_economies = recent_economies.rename(index=str, columns={'Reporter': 'reporter', 'Partner': 'partner',
                                                               'Year': 'year', 'Flow': 'flow',
                                                               'Balanced_value': 'balanced_value', 'Item_code': 'item_code',
                                                               'id_x': 'partner_id', 'COUNTRY_CODE_x': 'partner_code',
                                                               'COUNTRY_DESCRIPTION_x': 'partner_country_name',
                                                               'id_y': 'reporter_id', 'COUNTRY_CODE_y': 'reporter_code',
                                                               'COUNTRY_DESCRIPTION_y': 'reporter_country_name'
                                                               }
                                           )

recent_economies_neat = recent_economies[['reporter_id', 'reporter_country_name', 'partner_id', 'partner_country_name',
                                          'flow', 'balanced_value']]
recent_economies_neat = recent_economies_neat.dropna()
recent_economies_neat.reporter_id = recent_economies_neat.reporter_id.astype(int)
recent_economies_neat.partner_id = recent_economies_neat.partner_id.astype(int)
recent_economies_neat = recent_economies_neat[recent_economies_neat.reporter_country_name != 'World']
recent_economies_neat = recent_economies_neat[recent_economies_neat.reporter_country_name != 'Rest of the World']
recent_economies_neat = recent_economies_neat[recent_economies_neat.partner_country_name != 'World']
recent_economies_neat = recent_economies_neat[recent_economies_neat.partner_country_name != 'Rest of the World']

# edge file: target id, source id, type (Directed), weight (balanced value)
edge_imports = recent_economies_neat.loc[recent_economies_neat['flow'] == 'M']
edge_imports2 = edge_imports.copy()
edge_imports2['type'] = 'Directed'
edge_imports2 = edge_imports2[['reporter_id', 'reporter_country_name', 'partner_id', 'partner_country_name', 'type',
                               'balanced_value']]
edge_imports2 = edge_imports2.rename(index=str, columns={'reporter_id': 'target', 'partner_id': 'source',
                                                         'partner_country_name': 'source_name',
                                                         'reporter_country_name': 'target_name',
                                                         'balanced_value': 'weight'})
edge_imports3 = edge_imports2[['target', 'source', 'weight']]

edge_exports = recent_economies_neat.loc[recent_economies_neat['flow'] == 'X']
edge_exports2 = edge_exports.copy()
edge_exports2['type'] = 'Directed'
edge_exports2 = edge_exports2[['partner_id', 'partner_country_name', 'reporter_id', 'reporter_country_name', 'type',
                               'balanced_value']]
edge_exports2 = edge_exports2.rename(index=str, columns={'reporter_id': 'source', 'partner_id': 'target',
                                                         'partner_country_name': 'target_name',
                                                         'reporter_country_name': 'source_name',
                                                         'balanced_value': 'weight'})
edge_exports3 = edge_exports2[['target', 'source', 'weight']]

# node file: id, partner, country name, eventually GDP (IMF 2017)
node_df = recent_economies_neat[['reporter_id', 'reporter_country_name']]
node_df = node_df.rename(index=str, columns={'reporter_id': 'id', 'reporter_country_name': 'country_name'})
node_df = node_df.drop_duplicates(keep='first')

edge_imports3.to_csv('all_edge_imports.csv', index=False)
edge_exports3.to_csv('all_edge_exports.csv', index=False)
node_df.to_csv('all_nodes.csv', index=False)

asia = ('Australia', 'Bangladesh', 'China', 'Hong Kong, China', 'Indonesia', 'India', 'Japan', 'Korea, Republic of',
        'Malaysia', 'New Zealand', 'Papua New Guinea', 'Philippines', 'Singapore', 'Thailand',
        'United States of America', 'United Kingdom', 'Russian Federation')

edge_imports_asia = edge_imports2.loc[(edge_imports2['target_name'].isin(asia)) &
                                      (edge_imports2['source_name'].isin(asia))]
edge_imports_asia2 = edge_imports_asia[['target', 'source', 'weight']]

edge_exports_asia = edge_exports2.loc[(edge_exports2['target_name'].isin(asia)) &
                                      (edge_exports2['source_name'].isin(asia))]
edge_exports_asia2 = edge_exports_asia[['target', 'source', 'weight']]

node_df_asia = node_df.loc[node_df['country_name'].isin(asia)]

edge_imports_asia2.to_csv('asia_edge_imports.csv', index=False)
edge_exports_asia2.to_csv('asia_edge_exports.csv', index=False)
node_df_asia.to_csv('asia_nodes.csv', index=False)

test = ('United States of America', 'Japan', 'China')  # checking difference between export/import values

edge_imports_test = edge_imports2.loc[(edge_imports2['target_name'].isin(test)) &
                                      (edge_imports2['source_name'].isin(test))]
edge_imports_test2 = edge_imports_test[['target', 'source', 'weight']]

edge_exports_test = edge_exports2.loc[(edge_exports2['target_name'].isin(test)) &
                                      (edge_exports2['source_name'].isin(test))]
edge_exports_test2 = edge_exports_test[['target', 'source', 'weight']]

node_df_test = node_df.loc[node_df['country_name'].isin(test)]

print(edge_imports_test2)
print(edge_exports_test2)
print(node_df_test)
