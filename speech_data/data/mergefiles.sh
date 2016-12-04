#!/bin/bash
DIRS=/Users/sivagurukannan/Desktop/Fall2016/StatNLP/Project/President-Speeches-Embeddings/president_scraper/data/*

for d in $DIRS
do
	FILES=$d/*
	
	for f in $FILES
	do
		
  		echo "Processing $f file..."
  		# take action on each file. $f store current file name
  		cat $f >> $d/combined.txt 
	done
done
