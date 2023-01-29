## Домашнее задание по теме: "HDFS"

1. Запустите контейнер с любой версией Ubuntu. Скачайте с сайта https://grouplens.org/datasets/movielens датасет любого размера:
    ```bash
    wget https://files.grouplens.org/datasets/movielens/ml-latest.zip
    unzip ml-latest.zip
    UBUNTU=$(docker run -dt ubuntu:latest)
    ```

2. Перенесите файл ratings.csv в контейнер:
    ```bash
    docker cp ml-latest/ratings.csv $UBUNTU:/ratings.csv
    ```

3. Посчитайте топ-5 пользователей, которые выставили наибольшее количество оценок:
    ```bash
    docker exec $UBUNTU /usr/bin/cut -d, -f1 ratings.csv | sort | uniq -c | sort -nr | head -n5
      23715 123100
       9279 117490
       8381 134596
       7884 212343
       7515 242683
    ```

4. В качестве ответа укажите количество оценок, которые выставил первый пользователей получившегося рейтинга:

   Количество оценок первого пользователя в рейтинге (userId == 123100): 23715

