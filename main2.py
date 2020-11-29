import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
main_df = pd.DataFrame()
sizes = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000]

for i in sizes:
    df = pd.read_csv('Result_CPU/CPU_' + str(i) + '.txt')
    df["Size"] = i
    df["Type"] = "CPU"
    df["seconds"] = df['microseconds'] / 1000000
    main_df = pd.concat([main_df, df])