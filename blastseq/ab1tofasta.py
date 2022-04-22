#導入
import sys
import abifpy
from abifpy import Trace
import glob
import os

#変数定義
seq = ''
target = ''
files =[]
inputfile = ''
cutoff = 0.0001
trimseq = ''
name =''
#最初のメッセージ
print('with abifpy, pip insltall or activate env')

#対象のフォルダを指定
print('指定ディレクトリにあるAB1ファイルを対象にします')
target = input('ディレクトリを指定: ')

#フォルダ内のAB1ファイルリストを取得
files = glob.glob(target+'/*.ab1')
files.sort()
print (files)
#処理開始
if len(files) == 0:
    print('ディレクトリにAB1ファイルがありません!')
    sys.exit()
else:
    quality = input('クオリティカットオフ値を設定 10から100の整数 (デフォルト:60) :')
    if quality == '':
        quality = 60
    quality = float(quality)
    qu = str(quality)
    cutoff = float(10**(quality/(-10)))
    for inputfile in files:
        print(inputfile)
        seq = Trace(inputfile)
        try:
            trimseq = seq.trim(seq.seq, cutoff)
        except ValueError:
            trimseq = "NNNN"
        with open(target + '_' + qu + '.fasta', 'a') as f:
            filename = os.path.basename(inputfile)
            name = filename.replace('.ab1', '')
            print('>' + name, file=f)
            if trimseq == '':
                print('NNNN', file=f)
            else :
                print(trimseq, file=f)
            trimseq =''
sys.exit()
