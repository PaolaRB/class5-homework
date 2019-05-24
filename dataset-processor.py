import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs('plots/bar', exist_ok=True)
os.makedirs('plots/hist', exist_ok=True)
os.makedirs('plots/line', exist_ok=True)
os.makedirs('plots/scatter', exist_ok=True)


parser = argparse.ArgumentParser(description='Script to analyze and visualize data')
parser.add_argument('file_path', type=str, help='File path of the dataset')
parser.add_argument('header_names', type=str, help='File path of header column names')
args = parser.parse_args()

file_path = args.file_path
header_path = args.header_names

if not os.path.isfile(file_path):
    print('Invalid file, I\'ll crash')

if not os.path.isfile(header_path):
    print('Invalid header file, I\'ll crash')

# Header: create the 30 column names adding the suffix: -mean, -se, -worst
list_header = ['id', 'diagnosis']
with open(header_path) as file_handler:
    for line in file_handler:
        line_values = line.split(',')
        column_names = [line_values]
        for l in ('-mean', '-se', '-worst'):
            for item in line_values:
                list_header.append(item.strip() + l)

list_header_mean = [x for x in list_header if '-mean' in x]
list_header_se = [x for x in list_header if '-se' in x]
list_header_worst = [x for x in list_header if '-worst' in x]

# Load the dataframe
df = pd.read_csv(file_path, names=list_header)

print('**************************************** Shape *******************************************************')
print(df.shape)
print('**************************************** Info ********************************************************')
df.info()
print('**************************************** Describe ****************************************************')
print(df.describe())
print('**************************************** Head ********************************************************')
print(df.head(n=1))

print('************************************ Values per type of cancer  **************************************')
print(df['diagnosis'].value_counts())

print('*********************************** Describe per type cancer *****************************************')
df_b = df[df['diagnosis'] == 'B']
df_m = df[df['diagnosis'] == 'M']

print('*************************************** PLOT *******************************************************')
df.pop('id')

# ************* Bars - All ***************
df_diagnosis = df.groupby(['diagnosis'])
df_mean = df_diagnosis.mean()
index = ['B', 'M']
df_mean = df_mean.reindex(index)
for i, column in enumerate(df_mean):
    if i >= 0:
        plt.subplot(3, 10, i+1)
        df_mean[column].plot(kind='bar', figsize=(25, 20))
        plt.title(df_mean.columns[i])
        plt.tight_layout()
plt.savefig(f'plots/bar/AllGroupbyDiagnosis.png', format='png')
plt.clf()
print('*** Plot bars - OK')

df.pop('diagnosis')

# ************** Line Chart ************
for index, column in enumerate(df.columns):
    plt.figure(figsize=(10, 5))
    plt.plot(df[column], color='blue')
    plt.title(f'Plot of {column}')
    plt.xlabel('Patient id')
    plt.ylabel(column)
    plt.savefig(f'plots/line/{column}.png', format='png')
    plt.clf()
print('*** Line chart - Individually')


fig, ax = plt.subplots(3, 10, figsize=(40, 15))
m = 0
for i in range(3):
    for j in range(10):
        ax[i, j].plot(df[df.columns[m]], alpha=0.75)
        ax[i, j].set_xlabel("")
        ax[i, j].set_title(df.columns[m], fontname='Arial', fontsize=10)
        plt.tight_layout()
        m += 1
        for tick in ax[i, j].get_xticklabels():
            tick.set_fontname('Arial')
            tick.set_fontsize('7')
        for tick in ax[i, j].get_yticklabels():
            tick.set_fontname('Arial')
            tick.set_fontsize('7')

plt.savefig(f'plots/line/All.png', format='png')
plt.clf()
print('*** Line chart - Together')


# *************** Plotting Histograms *******************
fig, ax = plt.subplots(3, 10, figsize=(18, 15), sharey=True)
m = 0
for i in range(3):
    for j in range(10):
        ax[i, j].hist(df[df.columns[m]], bins=6, alpha=0.75)
        ax[i, j].set_xlabel("")
        ax[i, j].set_title(df.columns[m], fontname='Arial', fontsize=10)
        plt.tight_layout()
        m += 1
        for tick in ax[i, j].get_xticklabels():
            tick.set_fontname('Arial')
            tick.set_fontsize('7')
        for tick in ax[i, j].get_yticklabels():
            tick.set_fontname('Arial')
            tick.set_fontsize('7')

plt.savefig(f'plots/hist/All.png', format='png')
plt.clf()
print('**** Histograms - Together')

# # ******************* Scatter **********************
#for item in (list_header_mean, list_header_se, list_header_worst):
for index1, column1 in enumerate(df[list_header_mean].columns):
    for index2, column2 in enumerate(df[list_header_mean].columns):
        if index1 < index2:
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.scatter(df[column1], df[column2])
            ax.set_title(f'Scatter between {column1} and {column2}')
            ax.set_xlabel(column1)
            ax.set_ylabel(column2)
            plt.savefig(f'plots/scatter/{column1}-{column2}.png', format='png')
            plt.clf()

for index1, column1 in enumerate(df[list_header_se].columns):
    for index2, column2 in enumerate(df[list_header_se].columns):
        if index1 < index2:
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.scatter(df[column1], df[column2])
            ax.set_title(f'Scatter between {column1} and {column2}')
            ax.set_xlabel(column1)
            ax.set_ylabel(column2)
            plt.savefig(f'plots/scatter/{column1}-{column2}.png', format='png')
            plt.clf()

for index1, column1 in enumerate(df[list_header_worst].columns):
    for index2, column2 in enumerate(df[list_header_worst].columns):
        if index1 < index2:
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.scatter(df[column1], df[column2])
            ax.set_title(f'Scatter between {column1} and {column2}')
            ax.set_xlabel(column1)
            ax.set_ylabel(column2)
            plt.savefig(f'plots/scatter/{column1}-{column2}.png', format='png')
            plt.clf()
