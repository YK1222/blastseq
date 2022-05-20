from distutils.command.install_lib import PYTHON_SOURCE_EXTENSION
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.ticker as ptick


# データファイル指定
inputfile = sys.argv[1]  # msdialデータ
mediumfile = 'mediumlist.txt'  # 培地名リスト (解析時の名前に)
brothfile = 'brothlist.txt'  # broth名リスト (解析時の名前)

# データリスト (=カラム名) を配列に格納
with open(mediumfile, 'r') as f:
    mediumlist = f.read().split("\n")
    mediumlist = mediumlist[:-1]
    print('medium', mediumlist)

with open(brothfile, 'r') as f:
    brothlist = f.read().split("\n")
    brothlist = brothlist[:-1]
    print('broth', brothlist)

# msdialデータをpandas読み込み
table = pd.read_table(inputfile, header=4,
                      usecols=lambda x: x not in ['Fill %', 'Reference RT', 'Reference m/z', 'Formula', 'Ontology', 'INCHIKEY', 'SMILES', 'Annotation tag (VS1.0)', 'RT matched', 'm/z matched', 'MS/MS matched', 'Comment', 'Manually modified for quantification', 'Manually modified for annotation', 'Isotope tracking parent ID', 'Isotope tracking weight number', 'Total score', 'RT similarity', 'Dot product', 'Reverse dot product', 'Fragment presence %', 'S/N avera', '1', '1.1', 'Metabolite name'])

# 各nodeの最大値をデータに追加
table['maxbroval'] = table[brothlist[:]].max(axis=1)
table['maxbro'] = table[brothlist[:]].idxmax(axis=1)
table['maxmedval'] = table[mediumlist[:]].max(axis=1)
table['maxmed'] = table[mediumlist[:]].idxmax(axis=1)


# maxvalmed =< 1000 の broth値とMZ値を抽出
datalist = []
datalist.extend(brothlist[:])
datalist.insert(0, 'Average Mz')
datalist.append('maxmedval')
datalist.append('maxbroval')
plotdata = table[datalist[:]].query('maxmedval <= 1000')

# 最大値を設定する
maxval = plotdata['maxbroval'].max()
maxval = maxval + 1000

# 描画


def plotoption():
    plt.figure(figsize=(8.27, 11.69/2), dpi=100)
    plt.ylim(0, maxval)
    plt.ylabel('Area value')
    plt.xlabel('m/z')


k = 0
for i in brothlist:
    plt.scatter(x=plotdata['Average Mz'], y=plotdata[i], s=5, c='black')
    plt.title(i)
    name = i + '.pdf'
    name

    plt.savefig(name)

"""""
for i in brothlist:
    plt.scatter(x=plotdata['Average Mz'], y=plotdata[i], s=5, label=i)
lg = plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
plt.savefig('allplot.pdf', bbox_extra_artists=(lg,), bbox_inches='tight')


うまくいかなかった
plt.ylim(0, maxval)
k = 1
yoko = 7
tate = 3
fig = plt.figure(figsize=(11.69, 8.27), dpi=100)
for i in brothlist:
    ax = fig.add_subplot(yoko, tate, k)
    ax = plt.scatter(x=plotdata['Average Mz'], y=plotdata[i], s=5)
    k = k+1
plt.ylim(0, maxval)
plt.savefig('a.eps')
plt.figure()
"""
