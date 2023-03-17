## Домашнее задание по теме: "Работа с Apache Spark"

В файле `movies.csv` лежит база фильмов. Название фильма записано во втором столбце `title`.
Разбейте названия фильмов на отдельные слова и посчитайте какое слово встречается чаще всего.


1. Запущенный `Spark`:

	```bash
	$ podman-compose ps 
	['podman', '--version', '']
	using podman version: 4.2.0
	podman ps -a --filter label=io.podman.compose.project=spark
	CONTAINER ID  IMAGE                        COMMAND               CREATED        STATUS            PORTS                    NAMES
	ad95e2b8f60f  docker.io/bitnami/spark:3.3  /opt/bitnami/scri...  4 minutes ago  Up 4 minutes ago  0.0.0.0:58080->8080/tcp  spark_spark_1
	45096be58031  docker.io/bitnami/spark:3.3  /opt/bitnami/scri...  4 minutes ago  Up 4 minutes ago                           spark_spark-worker-0_1
	6fa8668eff19  docker.io/bitnami/spark:3.3  /opt/bitnami/scri...  4 minutes ago  Up 4 minutes ago                           spark_spark-worker-1_1
	exit code: 0
	```

2. Копирование файла `movies.csv`:

	```bash
	podman cp $HOME/spark/movies.csv spark_spark_1:/opt/bitnami/spark/
	```

3. Переход в контейнер:

	```bash
	$ podman exec -it spark_spark_1 bash
	1001@ad95e2b8f60f:/opt/bitnami/spark$ pyspark
	Python 3.8.16 (default, Mar 12 2023, 21:24:23) 
	[GCC 10.2.1 20210110] on linux
	Type "help", "copyright", "credits" or "license" for more information.
	Setting default log level to "WARN".
	To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
	23/03/17 21:14:32 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
	Welcome to
	      ____              __
	     / __/__  ___ _____/ /__
	    _\ \/ _ \/ _ `/ __/  '_/
	   /__ / .__/\_,_/_/ /_/\_\   version 3.3.2
	      /_/
	
	Using Python version 3.8.16 (default, Mar 12 2023 21:24:23)
	Spark context Web UI available at http://ad95e2b8f60f:4040
	Spark context available as 'sc' (master = local[*], app id = local-1679087673253).
	SparkSession available as 'spark'.
	>>> 
	```

4. Поиск слова:

	```
	>>> movies = sc.textFile('movies.csv')
	>>> words = movies.map(lambda x: x.split(',')[1]).flatMap(lambda x: x.split()).countByValue()
	>>> sorted(words.items(), key=lambda x: x[1], reverse=True)[0]
	('of', 946)
	```

### Результат: встречается чаще всего слово 'of' (946 раз)
