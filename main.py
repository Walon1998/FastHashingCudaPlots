import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math

sizes = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000]
blocks = [16, 16, 32, 256, 2512, 25008, 250016, 2500016, 25000016]
factors = [1, 1, 2, 3, 2, 4, 6, 4, 8, 12]
files = ['Result_GPU/GPU_1_1.csv', 'Result_GPU/GPU_64_80.csv', 'Result_GPU/GPU_64_160.csv', 'Result_GPU/GPU_64_240.csv', 'Result_GPU/GPU_128_80.csv', 'Result_GPU/GPU_128_160.csv',
         'Result_GPU/GPU_128_240.csv', 'Result_GPU/GPU_256_80.csv', 'Result_GPU/GPU_256_160.csv' ]

names = ['<1,1>', '<64,80>', '<64,160>', '<64,240>', '<128,80>', '<128,160>', '<128,240>', '<256,80>', '<256,160>', '<256,240>']

main_df = pd.DataFrame()

peak_perf = []
for i in range(len(blocks)):
    val = (1407 * (blocks[i] / 16)) / (1245 * 1000000)
    main_df = main_df.append({'seconds': val, 'Size': sizes[i], 'Launch Configuration': 'Peak Performance'}, ignore_index=True)
    peak_perf.append(val)

print(peak_perf)

for j in range(len(files)):
    df = pd.read_csv(files[j], skiprows=3)
    df = df[1:]
    for i in sizes:
        temp_df = pd.DataFrame()
        temp_df["seconds"] = pd.to_numeric(df.head(100)['Duration']) / factors[j]
        temp_df["Size"] = i
        temp_df["Launch Configuration"] = names[j]
        df = df[100:]
        main_df = pd.concat([main_df, temp_df])

print(main_df)

sns.set(style="whitegrid", rc={'figure.figsize': (16, 9)}, font_scale=2)
ax = sns.lineplot(x="Size", y="seconds", style="Launch Configuration", hue='Launch Configuration', err_style='bars', data=main_df, markers=True, dashes=False)
ax.set(xscale="log", yscale="log")
ax.set(ylabel="Time [s] / Occupancy", xlabel='Input size [Bytes]', title='SHA-256')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[0:], labels=labels[0:])

plt.show()

# plt.savefig('plot1.pdf', format="pdf", bbox_inches="tight")
