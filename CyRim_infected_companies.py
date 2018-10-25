"""
This was written as a proof-of-concept for work.
It is a small piece of a large project that was originally completed in Excel.
"""

import pandas as pd

pd.set_option('display.expand_frame_repr', False)

df_companies = pd.read_csv('CyRim-NumberOfCompanies.csv')
df_replication_rate = pd.read_csv('CyRim-ReplicationRate.csv')
df_infection_rate = pd.read_csv('CyRim-InfectionRates.csv')

df_merge = pd.merge(df_companies, df_replication_rate, on='VulnerabilityScore')
df_merge['CompaniesDistributedByReplicationRate'] = df_merge['Companies'] * df_merge['ReplicationRate']

df_infected_companies = pd.merge(df_merge, df_infection_rate, on=('VulnerabilityScore', 'Size'))
df_infected_companies['InfectedCompanies'] = df_infected_companies['CompaniesDistributedByReplicationRate'] * df_infected_companies['InfectionRate']

df_infected_companies_subtotals = pd.DataFrame()
df_infected_companies_subtotals['InfectedCompaniesSubtotals'] = df_infected_companies.groupby(['Sector', 'Size', 'ScenarioVariant'])['InfectedCompanies'].sum()

interim_df_infected_companies = df_infected_companies
interim_df_infected_companies = interim_df_infected_companies.drop(columns=['VulnerabilityScore'])
interim_df_infected_companies = interim_df_infected_companies.drop(columns=['ReplicationRate'])
interim_df_infected_companies = interim_df_infected_companies.drop(columns=['CompaniesDistributedByReplicationRate'])
interim_df_infected_companies = interim_df_infected_companies.drop(columns=['InfectionRate'])
interim_df_infected_companies = interim_df_infected_companies.drop(columns=['ReplicationRateBucket'])
interim_df_infected_companies = interim_df_infected_companies.drop(columns=['Companies'])
interim_df_infected_companies = interim_df_infected_companies.drop(columns=['ScaleFactor'])

df_infected_grouped = interim_df_infected_companies.groupby(['Sector', 'Size', 'ScenarioVariant']).sum().reset_index()
df_companies_grouped = df_companies.groupby(['Sector', 'Size']).sum().reset_index()
df_companies_grouped = df_companies_grouped.drop(columns=['VulnerabilityScore'])

merged_for_distribution = pd.merge(df_infected_grouped, df_companies_grouped, on=['Sector', 'Size'])
merged_for_distribution['distribution'] = (merged_for_distribution['InfectedCompanies'] / merged_for_distribution['Companies']) * 100

infected_sorted = merged_for_distribution.sort_values(by=['Sector', 'Size'], ascending=True)
infected_sorted['distribution'] = infected_sorted['distribution'].astype(int) # values rounded right at the end
infected_S1 = infected_sorted.loc[infected_sorted['ScenarioVariant'] == 'S1', ['Sector', 'Size', 'distribution']]
infected_S1_pivot = infected_S1.pivot(index='Sector', columns='Size', values='distribution')


def get_global_infection(scenariovar):
    infected_scenariovar = infected_sorted.loc[infected_sorted['ScenarioVariant'] == scenariovar, ['Sector', 'Size', 'distribution']]
    infected_scenariovar = infected_scenariovar.pivot(index='Sector', columns='Size', values='distribution')
    cols = infected_scenariovar.columns.tolist()
    cols = cols[-1:] + cols[1:2] + cols[0:1] + cols[2:3]
    infected_scenariovar = infected_scenariovar[cols]
    print('Global Infection Rate by Size and Sector -', scenariovar)
    print('-----------------------------------------------')
    return infected_scenariovar


print(get_global_infection('S1'))
print('-----------------------------------------------')
print(get_global_infection('S2'))
print('-----------------------------------------------')
print(get_global_infection('X1'))

pd.concat([
    pd.concat([get_global_infection('S1'), get_global_infection('S2'), get_global_infection('X1')], axis=1)
]).to_csv('test.csv')

