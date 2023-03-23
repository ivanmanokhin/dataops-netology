## Домашнее задание по теме: "Spark SQL"

Цель: изучить датасет по заболеваемости ковид-19 и получить навык работы с DataFrame API

1. Выберите 15 стран с наибольшим процентом переболевших на 31 марта (в выходящем датасете необходимы колонки: iso_code, страна, процент переболевших)

    #### Результат:

    ```python
    from pyspark.sql.functions import *

    df = (spark.read.option('header', True)
                    .option('sep', ',')
                    .option('inferSchema', True)
                    .csv('owid-covid-data.csv'))

    (df.where((col('date') == '2020-03-31')
              & (~col('iso_code').like('%OWID_%')))
       .select('iso_code',
               col('location').alias('страна'),
               (round((col('total_cases') - col('total_deaths')) / col('population') * 100, 3)).alias('процент переболевших'))
       .orderBy(col('процент переболевших').desc())
       .limit(15)
       .show())
    ```
    ```
    +--------+-----------+--------------------+
    |iso_code|     страна|процент переболевших|
    +--------+-----------+--------------------+
    |     SMR| San Marino|               0.619|
    |     AND|    Andorra|               0.471|
    |     LUX| Luxembourg|               0.344|
    |     ISL|    Iceland|               0.332|
    |     ESP|      Spain|               0.187|
    |     CHE|Switzerland|               0.187|
    |     ITA|      Italy|               0.154|
    |     MCO|     Monaco|                0.13|
    |     AUT|    Austria|               0.112|
    |     BEL|    Belgium|               0.104|
    |     DEU|    Germany|               0.085|
    |     NOR|     Norway|               0.085|
    |     FRA|     France|               0.072|
    |     PRT|   Portugal|               0.071|
    |     NLD|Netherlands|               0.068|
    +--------+-----------+--------------------+
    ```

    Данные за 2021 год:

    ```python
    max_date_2021 = df.groupBy(year('date')).agg(max('date')).where(col('year(date)') == '2021').select(col('max(date)').alias('max_date'))

    (df.where((col('date') == max_date_2021.collect()[0][0])
              & (~col('iso_code').like('%OWID_%')))
       .select('iso_code',
               col('location').alias('страна'),
               (round((col('total_cases') - col('total_deaths')) / col('population') * 100, 3)).alias('процент переболевших'))
       .orderBy(col('процент переболевших').desc())
       .limit(15)
       .show())
    ```
    ```
    +--------+-------------+--------------------+
    |iso_code|       страна|процент переболевших|
    +--------+-------------+--------------------+
    |     AND|      Andorra|               16.37|
    |     MNE|   Montenegro|              14.959|
    |     CZE|      Czechia|              14.679|
    |     SMR|   San Marino|              14.553|
    |     SVN|     Slovenia|               10.94|
    |     LUX|   Luxembourg|              10.218|
    |     SRB|       Serbia|               9.616|
    |     ISR|       Israel|               9.596|
    |     BHR|      Bahrain|               9.551|
    |     USA|United States|               9.384|
    |     SWE|       Sweden|               8.776|
    |     EST|      Estonia|               8.739|
    |     LTU|    Lithuania|               8.415|
    |     PAN|       Panama|               8.214|
    |     NLD|  Netherlands|               8.187|
    +--------+-------------+--------------------+
    ```

2. Top 10 стран с максимальным зафиксированным кол-вом новых случаев за последнюю неделю марта 2021 в отсортированном порядке по убыванию (в выходящем датасете необходимы колонки: число, страна, кол-во новых случаев)

    #### Результат:

    ```python
    (df.where((col('date').between('2021-03-29', '2021-03-31'))
          & (~col('iso_code').like('%OWID_%')))
   .orderBy(col('location'), col('new_cases').desc())
   .groupBy(col('location')).agg(first('new_cases').alias('new_cases'), first('date').alias('date'))
   .orderBy(col('new_cases').desc())
   .select(date_format('date', 'yyyy-MM-dd').alias('число'),
           col('location').alias('страна'),
           col('new_cases').alias('кол-во новых случаев'))
   .limit(10)
   .show())
    ```
    ```
    +----------+-------------+--------------------+
    |     число|       страна|кол-во новых случаев|
    +----------+-------------+--------------------+
    |2021-03-31|       Brazil|             90638.0|
    |2021-03-31|        India|             72330.0|
    |2021-03-29|United States|             69429.0|
    |2021-03-31|       France|             59054.0|
    |2021-03-31|       Turkey|             39302.0|
    |2021-03-31|       Poland|             32891.0|
    |2021-03-31|      Germany|             25014.0|
    |2021-03-31|        Italy|             23887.0|
    |2021-03-30|       Sweden|             16427.0|
    |2021-03-31|    Argentina|             16056.0|
    +----------+-------------+--------------------+
    ```

3. Посчитайте изменение случаев относительно предыдущего дня в России за последнюю неделю марта 2021. (например: в россии вчера было 9150 , сегодня 8763, итог: -387) (в выходящем датасете необходимы колонки: число, кол-во новых случаев вчера, кол-во новых случаев сегодня, дельта)

    #### Результат:

    ```python
    from pyspark.sql.window import Window

    (df.where((col('date').between('2021-03-28', '2021-03-31'))
              & (col('iso_code') == 'RUS'))
       .withColumn("кол-во новых случаев вчера",lag('new_cases').over(Window.orderBy("date")))
       .select(date_format('date', 'yyyy-MM-dd').alias('число'),
               col('new_cases').alias('кол-во новых случаев сегодня'),
               'кол-во новых случаев вчера',
               (col('new_cases') - col('кол-во новых случаев вчера')).alias('дельта'))
       .where(col('date') != '2021-03-28')
       .show())
    ```
    ```
    +----------+----------------------------+--------------------------+------+
    |     число|кол-во новых случаев сегодня|кол-во новых случаев вчера|дельта|
    +----------+----------------------------+--------------------------+------+
    |2021-03-29|                      8589.0|                    8979.0|-390.0|
    |2021-03-30|                      8162.0|                    8589.0|-427.0|
    |2021-03-31|                      8156.0|                    8162.0|  -6.0|
    +----------+----------------------------+--------------------------+------+
    ```
