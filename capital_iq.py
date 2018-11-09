import pandas as pd

pd.set_option('display.expand_frame_repr', False)

file = open('I:\Python\capitaliq\capital_iq_download.csv', 'r')
df1 = pd.read_csv(file)

file = open('I:\Python\capitaliq\capital_iq_download_2.csv', 'r')
df2 = pd.read_csv(file)

file = open('I:\Python\capitaliq\capital_iq_download_3.csv', 'r')
df3 = pd.read_csv(file)

frames = [df1, df2, df3]
df = pd.concat(frames, sort=True)

#print(df['Industry_Classifications'].unique())
#df.rename(columns=lambda x: x.strip())

df = df.replace(['-', ' - ', ' -   '], 0)
df['Total_Revenue_LTM_USDmm'] = df['Total_Revenue_LTM_USDmm'].str.replace(',', '')
df['Number_of_Employees_Global'] = df['Number_of_Employees_Global'].str.replace(',', '')
df['Total_Revenue_LTM_USDmm'] = df['Total_Revenue_LTM_USDmm'].astype(float)
df['Number_of_Employees_Global'] = pd.to_numeric(df['Number_of_Employees_Global'], errors='coerce')

sector = df.loc[
    (df['Industry_Classifications'] == 'Telecommunication Services (Primary)') &
    (df['Geographic_Region'] == 'Asia / Pacific') &
    (df['Number_of_Employees_Global'] >= 100) &
    (df['Number_of_Employees_Global'] <= 500) &
    (df['Total_Revenue_LTM_USDmm'] > 0)]

print(sector.head(10))




"""
Premier     >2000 employees; >$3 b revenue
Large       500-2000; $40 m - $3 b
Medium      100-500; $10 m - $40 m
Small       20-100; $2 m - $10 m
"""