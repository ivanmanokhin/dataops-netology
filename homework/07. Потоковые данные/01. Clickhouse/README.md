## Домашнее задание по теме: "Clickhouse"

1. Создайте базу homework

    ```sql
    CREATE DATABASE homework
    ```

    #### Результат:

    ```
    97d1428e22b6 :) \l

    SHOW DATABASES
    
    ┌─name───────────────┐
    │ INFORMATION_SCHEMA │
    │ default            │
    │ homework           │
    │ information_schema │
    │ system             │
    └────────────────────┘
    ```

2. Создаём таблицу metrika

    ```sql
    CREATE TABLE homework.metrika
    (
        `EventDate` Date,
        `CounterID` UInt32,
        `UserID` UInt64,
        `RegionID` UInt32
    )
    ENGINE = MergeTree()
    PARTITION BY toYYYYMM(EventDate)
    ORDER BY (CounterID, EventDate, intHash32(UserID))
    ```

    #### Результат:

    ```
    97d1428e22b6 :) \d
    
    SHOW TABLES
    
    ┌─name────┐
    │ metrika │
    └─────────┘
    ```

3. Заливаем данные в таблицу

    ```bash
    cat metrika_sample.tsv | clickhouse-client --database homework --query "INSERT INTO metrika FORMAT TSV"
    ```

    #### Результат:

    ```
    97d1428e22b6 :) SELECT * FROM metrika LIMIT 3;
    
    ┌──EventDate─┬─CounterID─┬──────────────UserID─┬─RegionID─┐
    │ 2014-03-17 │        57 │ 8585742290196126178 │    14050 │
    │ 2014-03-17 │        57 │  610708775678702928 │       54 │
    │ 2014-03-17 │        57 │  610708775678702928 │       54 │
    └────────────┴───────────┴─────────────────────┴──────────┘
    ```

4. Посчитайте какой пользователь UserID сделал больше всего просмотров страниц?

    #### Результат:
    ```
    97d1428e22b6 :) SELECT UserID, count() as Count
                    FROM metrika
                    GROUP BY UserID
                    ORDER BY Count DESC
                    LIMIT 1;
    
    ┌──────────────UserID─┬─Count─┐
    │ 1313448155240738815 │  4439 │
    └─────────────────────┴───────┘
    ```
