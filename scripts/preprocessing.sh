#! /bin/bash

# Adapted from https://github.com/bricksdont/joeynmt-toy-models/blob/master/scripts/preprocess.sh

scripts=`pwd`
base=$scripts/..

data=$base/data

mkdir -p $base/shared_models

src=bam
trg=fr

# cloned from https://github.com/bricksdont/moses-scripts
cd $base
git clone https://github.com/bricksdont/moses-scripts
MOSES=$base/moses-scripts/scripts

bpe_num_operations=1000
bpe_vocab_threshold=2

#################################################################

# input files are preprocessed already up to truecasing

# remove preprocessing for target language test data, for evaluation

cat $data/test.$trg | $MOSES/recaser/detruecase.perl > $data/test.tokenized.$trg
cat $data/test.tokenized.$trg | $MOSES/tokenizer/detokenizer.perl -l $trg > $data/test.$trg

# learn BPE model on train (concatenate both languages)

subword-nmt learn-joint-bpe-and-vocab -i $data/train.$src $data/train.$trg \
	--write-vocabulary $base/shared_models/vocab.$src $base/shared_models/vocab.$trg \
	-s $bpe_num_operations -o $base/shared_models/$src$trg.bpe

# apply BPE model to train, test and dev

for corpus in train dev test; do
	subword-nmt apply-bpe -c $base/shared_models/$src$trg.bpe --vocabulary $base/shared_models/vocab.$src --vocabulary-threshold $bpe_vocab_threshold < $data/$corpus.$src > $data/$corpus.bpe.$src
	subword-nmt apply-bpe -c $base/shared_models/$src$trg.bpe --vocabulary $base/shared_models/vocab.$trg --vocabulary-threshold $bpe_vocab_threshold < $data/$corpus.$trg > $data/$corpus.bpe.$trg
done

# build joeynmt vocab
python $base/scripts/build_vocab.py $data/train.bpe.$src $data/train.bpe.$trg --output_path $base/shared_models/vocab.txt

# file sizes
for corpus in train dev test; do
	echo "corpus: "$corpus
	wc -l $data/$corpus.bpe.$src $data/$corpus.bpe.$trg
done

wc -l $base/shared_models/*

# sanity checks

echo "At this point, please check that 1) file sizes are as expected, 2) languages are correct and 3) material is still parallel"
