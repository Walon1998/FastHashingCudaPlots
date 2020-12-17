import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

main_df = pd.DataFrame()
sizes = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000]

for i in sizes:
    df = pd.read_csv('Result_CPU/CPU_' + str(i) + '.txt')
    df["Size"] = i
    df["Type"] = "CPU SHA-256"
    main_df = pd.concat([main_df, df])

for i in range(len(sizes)):
    temp_df = pd.DataFrame()
    df = pd.read_csv('Result_PARSHA/GPU_' + str(i) + '.csv', skiprows=3)
    df = df[1:]
    df = pd.to_numeric(df['Duration'])
    iters = len(df.index) / 100

    # print(df)
    for k in range(100):
        val = 0
        for j in range(int(iters)):
            val += df.values[k + j * 100]
        temp_df = temp_df.append({'microseconds': val}, ignore_index=True)

    temp_df["Size"] = sizes[i]
    temp_df["Type"] = 'GPU PARSHA-256'
    main_df = pd.concat([main_df, temp_df])
    # print(temp_df)

df = pd.read_csv('Result_GPU/GPU_1_1.csv', skiprows=3)
df = df[1:]
for i in sizes:
    temp_df = pd.DataFrame()
    temp_df["microseconds"] = pd.to_numeric(df.head(100)['Duration']) * 1000000
    temp_df["Size"] = i
    temp_df["Type"] = 'GPU SHA-256'
    df = df[100:]
    main_df = pd.concat([main_df, temp_df])

print(main_df)

sns.set(style="whitegrid", rc={'figure.figsize': (16, 9)}, font_scale=2)
ax = sns.lineplot(x="Size", y="microseconds", style="Type", hue='Type', err_style='bars', data=main_df, markers=True, dashes=False, linewidth=5, ms=12)
ax.set(xscale="log", yscale="log")
ax.set(ylabel="Time [μs]", xlabel='Input size [Bytes]', title='SHA-256 vs. PARSHA-256')
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles[0:], labels=labels[0:])

new_df = main_df[main_df['Size'] == 100000000]
new_df = new_df.groupby(['Type']).mean()
print(new_df)

for x, y in zip(new_df['Size'], new_df['microseconds']):
    plt.text(x=(x + 25000000), y=(y), s='{:.0f}'.format(y), fontsize=14)

# plt.show()
plt.savefig('plot_parsha.pdf', format="pdf", bbox_inches="tight")
