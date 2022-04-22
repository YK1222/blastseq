#!/bin/zsh
#本体、データベース、分類データのpathを定義
BLAST="/Users/pcmf35/Desktop/16S"
db="/Users/pcmf35/Documents/Research/BLAST"
tax="/Users/pcmf35/Documents/Research/BLAST/TAX.tsv"

#みんなが繰り返し使うことを前提とするため、無限ループ
while true
do
#ダブルクリック起動を前提とするため、本体位置に移動
cd $BLAST

#ファイル名に日付と時刻を含むため、一応宣言
day=$(date +%Y%m%d-%H%M%S)
echo "現時刻は${day}です"
echo "inputフォルダにfastaファイルを入れ、ファイル名を入力し、エンターを押してください。"
read filename
#input以下にあるはずだが、一応検索を挟む。エラーループを挟みたい
file=$(find ./input -name "${filename}")
echo "$file を対象にBLASTを行います。"
echo "エンターをもう一度押すと開始します。"
read a

#logを参照してその日初めての起動だったらデータベースを更新
start=$(date "+%Y%m%d %H:%M:%S")
startday=$(echo $start | awk '{print $1}')
lastday=$(tail -1 log.txt | awk '{print $1}')
if [ $startday -gt $lastday ];
then
cd $db
echo "16S ribosomal RNA のデータベースを更新します (一日一回初回起動時更新)"
ncbi-blast-dbs 16S_ribosomal_RNA
rm "${db/16S_ribosomal_RNA.tar.gz}"
cd $BLAST
fi

#ブラスト開始 一時ファイルに保存
blastn -query $file -db $db/16S_ribosomal_RNA -max_target_seqs 1 -outfmt "6 qseqid stitle pident qlen bitscore qcovs gaps" > result99999.txt

#表データを改変し、tsvとして整理 菌株番号が分類名に入っていたらそこも分ける。subspは種名に入れる。
#整理後、一時ファイルに保存
awk -F '\t' 'BEGIN{OFS="\t"}
	{
	if($2 ~ "^[A-Z].*[A-Z].*" && $2 !~ "subsp.")
		{
		r = gensub(" ", "\t", 2, $2)
		print $1,r,$3,$4,$5,$6,$7
		}
	else if($2 ~ "^[A-Z].*[A-Z].*" && $2 ~ "subsp.")
		{
		r=gensub(" ", "\t", 4, $2)
		print $1,r,$3,$4,$5,$6,$7
		}
	else
		{
		print $0
		}
	}' result99999.txt \
|awk -F '\t' 'BEGIN{OFS="\t"}
	{
		r = gensub(" ", "\t", 1, $2)
		print $1,r,$3,$4,$5,$6,$7,$8
		}'\
|gsed -e 's/ strain //g' \
|gsed -e 's/strain //g' \
|gsed -e 's/16S ribosomal RNA,//g' \
|gsed -e 's/partial sequence//g' \
|gsed -e 's/complete sequence//g' \
|gsed -e 's/ \t /\t/g' \
|gsed -e 's/  / /g' \
|gsed -e 's/\t /\t/g' > "piyo.tsv"

#入力ファイルを一度リストになおし、一時ファイルに保存
seqkit seq -g ${file} | seqkit fx2tab > tab.tsv

#保存した整理後一時ファイルとfastaリストファイルをjoinで結合。
#順番は変わらないため、sortの必要はないが、エラー行が出たらどうしようか
join -t $'\t' piyo.tsv tab.tsv >> hoge.tsv

#出力データのヘッダーを作成
echo "Name\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tspecies\tTopHitStrain\tIdentity\tLength\tbitscore\tcoverage\tgap\tseqence" > "./output/${day}.tsv"

#事前に入手していた分類ファイルとBLASTデータを結合し、詳細な分類ツリーを付属させる。
while read line;
do
genus=$(echo $line | awk -F '\t' '{print $2}')
one=$(echo $line | awk -F '\t' '{print $1}')
other=$(echo $line | cut -f 3-)
awk -v genus=$genus -v one=$one -v other=$other -F '\t' '$6 == genus {print one"\t"$0"\t"other}' "${tax}" >> "./output/${day}.tsv"
done <hoge.tsv

#一時ファイルを削除する。
rm tab.tsv
rm result99999.txt
rm piyo.tsv
rm hoge.tsv

#logを残す。
end=$(date "+%Y%m%d %H:%M:%S")
echo "${start}\t${end}\t${file}\t${day}.tsv" >> log.txt

#アナウンス
echo "出力結果は output/${day}.tsv にあります。"
echo "エンターで最初に戻る。"
read a
done
