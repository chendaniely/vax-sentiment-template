for article in data/*.csv
do
    echo $article
    python src/csv_to_multi_single.py $article
done
