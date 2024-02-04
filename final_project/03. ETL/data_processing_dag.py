from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
import pandas as pd
from clickhouse_driver import Client
import psycopg2

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 2, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# параметры подключения к ClickHouse
clickhouse_params = {
    'host':'clickhouse',
    'port': 9000,
    'database': 'default'
}

# параметры подключения к PostgreSQL
postgres_params = {
    'host': 'postgres',
    'port': 5432,
    'user': 'airflow',
    'password': 'airflow',
    'database': 'postgres'
}

# атрибуты для маппинга
column_map = {
    'cities': 'city',
    'branches': 'branch',
    'product_lines': 'product_line',
    'payment_methods': 'payment_method',
    'customer_types': 'customer_type'
}

def connect_to_clickhouse(**kwargs):
    '''Функция для подключения к ClickHouse'''
    return Client(host=kwargs['host'],
                  port=kwargs['port'],
                  database=kwargs['database'])

def connect_to_postgres(**kwargs):
    '''Функция для подключения к PostgreSQL'''
    return psycopg2.connect(host=kwargs['host'],
                            port=kwargs['port'],
                            user=kwargs['user'],
                            password=kwargs['password'],
                            database=kwargs['database'])

def dataframe_values_mapping(postgres_params, schema, column_map, df):
    '''Функция для маппинга значений в id'''
    query = 'SELECT id, name FROM "{}"."{}"'
    values_dict = {}

    postgres_client = connect_to_postgres(**postgres_params)
    cursor = postgres_client.cursor()

    for k, v in column_map.items():
        cursor.execute(query.format(schema, k))
        values_dict = dict(cursor.fetchall())
        df[v] = df[v].map({_v: _k for _k, _v in values_dict.items()})

    cursor.close()
    postgres_client.close()

    print('Маппинг данных успешно выполнен')
    
    return df

def insert_dates(cursor, row, schema):
    '''Функция для заполнения таблицы sakes_dates'''
    query = f"""
             INSERT INTO {schema}.sales_dates (date, year, month, month_name, day, day_of_the_week)
             VALUES ('{row['datetime']}',
                      {row['datetime'].year},
                      {row['datetime'].month},
                     '{row['datetime'].strftime('%B')}',
                      {row['datetime'].day},
                     '{row['datetime'].strftime('%A')}')
             RETURNING id
             """

    cursor.execute(query)
    return cursor.fetchone()[0] # возврат id строки

def insert_time(cursor, row, schema):
    '''Функция для заполнения таблицы sales_time'''
    query = f"""
             INSERT INTO {schema}.sales_time (datetime, hour, minute, second)
             VALUES ('{row['datetime']}',
                      {row['datetime'].hour},
                      {row['datetime'].minute},
                      {row['datetime'].second})
             RETURNING id
             """

    cursor.execute(query)
    return cursor.fetchone()[0] # возврат id строки

def insert_rating(cursor, row, schema):
    '''Функция для заполнения таблицы sales_rating'''
    query = f"""
             INSERT INTO {schema}.sales_rating (rating)
             VALUES ({row['rating']})
             RETURNING id
             """

    cursor.execute(query)
    return cursor.fetchone()[0] # возврат id строки

def extract_unprocessed_data(**kwargs):
    '''Функция для извлечения данных из ClickHouse'''
    clickhouse_client = connect_to_clickhouse(**kwargs['clickhouse_params'])

    # получаем данные из ClickHouse
    data = clickhouse_client.execute(f"SELECT * FROM {kwargs['table_name']} ORDER BY datetime")

    # создаем датафрейм с полученными данными
    df = pd.DataFrame(data, columns=[col[0] for col in clickhouse_client.execute(f"DESCRIBE {kwargs['table_name']}")])

    # используем механизм кросс-коммуникации для передачи данных в другие задачи
    kwargs['ti'].xcom_push(key='unprocessed_data', value=df)

    clickhouse_client.disconnect()

def load_to_nds(**kwargs):
    '''Функция для загрузки данных в PostgreSQL (NDS)'''
    query =  """
             INSERT INTO {}.sales (id, datetime, city_id, branch_id, customer_type_id, gender,
                                       payment_method_id, product_line_id, unit_price, quantity, rating)
             VALUES('{}', '{}', {}, {}, {}, '{}', {}, {}, {}, {}, {})
             """

    # получаем данные
    df = kwargs['ti'].xcom_pull(task_ids='extract_unprocessed_data', key='unprocessed_data')

    # создаем копию датафрейма для маппинга значений
    _df = df.copy()
    _df = dataframe_values_mapping(kwargs['postgres_params'], 
                                   kwargs['schema'],
                                   kwargs['column_map'],
                                   _df)

    postgres_client = connect_to_postgres(**kwargs['postgres_params'])
    cursor = postgres_client.cursor()

    # добавляем данные в таблицу NDS
    for i, row in df.iterrows():
        _row = _df.iloc[i]
        cursor.execute(query.format(kwargs['schema'],
                                    _row['id'],
                                    _row['datetime'],
                                    _row['city'],
                                    _row['branch'],
                                    _row['customer_type'],
                                    _row['gender'],
                                    _row['payment_method'],
                                    _row['product_line'],
                                    _row['unit_price'],
                                    _row['quantity'],
                                    _row['rating']))

    postgres_client.commit()
    cursor.close()
    postgres_client.close()

    print('Загрузка данных в Postgres успешно выполнена')

def load_to_dds(**kwargs):
    '''Функция для загрузки данных в PostgreSQL (DDS)'''
    query =  """
             INSERT INTO {}.sales
             VALUES('{}', {}, {}, {}, {}, {}, '{}', {}, {}, {}, {}, {}, {}, {}, {}, {})
             """

    # получаем данные
    df = kwargs['ti'].xcom_pull(task_ids='extract_unprocessed_data', key='unprocessed_data')

    # создаем копию датафрейма для маппинга значений
    _df = df.copy()
    _df = dataframe_values_mapping(kwargs['postgres_params'], 
                                   kwargs['schema'],
                                   kwargs['column_map'],
                                   _df)

    postgres_client = connect_to_postgres(**kwargs['postgres_params'])
    cursor = postgres_client.cursor()

    # добавляем данные в таблицы DDS
    for i, row in df.iterrows():
        _row = _df.iloc[i]
        date_id = insert_dates(cursor, row, kwargs['schema'])
        time_id = insert_time(cursor, row, kwargs['schema'])
        rating_id = insert_rating(cursor, row, kwargs['schema'])
        cursor.execute(query.format(kwargs['schema'],
                                    _row['id'],
                                    date_id,
                                    time_id,
                                    _row['city'],
                                    _row['branch'],
                                    _row['customer_type'],
                                    _row['gender'],
                                    _row['payment_method'],
                                    _row['product_line'],
                                    rating_id,
                                    _row['unit_price'],
                                    _row['quantity'],
                                    _row['tax'],
                                    _row['total'],
                                    _row['cogs'],
                                    _row['gross_income']))

    postgres_client.commit()
    cursor.close()
    postgres_client.close()

    print('Загрузка данных в Postgres успешно выполнена')

def transfer_of_processed_data(**kwargs):
    transfer_query = 'INSERT INTO {} ({}) VALUES'
    truncate_query = 'TRUNCATE TABLE un{}'

    df = kwargs['ti'].xcom_pull(task_ids='extract_unprocessed_data', key='unprocessed_data')
    df.drop(columns=['insert_time'], inplace=True)

    clickhouse_client = connect_to_clickhouse(**kwargs['clickhouse_params'])

    # загрузка данных в таблицу с обработанными данными
    for i in range(0, len(df), kwargs['batch_size']):
        batch_df = df.iloc[i:i + kwargs['batch_size']]
        print(f'Подготовлен батч размером {batch_df.shape[0]}')
        clickhouse_client.execute(transfer_query.format(kwargs['table_name'], ' ,'.join(df.columns)), batch_df.to_dict(orient='records'))
        print(f'  Загружено {batch_df.shape[0]} строк')

    print('Обработаные данные загружены')

    # очистка таблицы с необработанными данными
    clickhouse_client.execute(truncate_query.format(kwargs['table_name']))
    print('Таблица с необработанными данными очищена')

dag = DAG(
    'data_processing_dag',
    default_args=default_args,
    description='DAG для извлечения, обработки и перемещения данных',
    #schedule_interval=timedelta(days=1),
    schedule_interval="@daily"
)

start_task = DummyOperator(
    task_id='start_task',
    dag=dag,
)

extract_task = PythonOperator(
    task_id='extract_unprocessed_data',
    python_callable=extract_unprocessed_data,
    op_kwargs={'clickhouse_params': clickhouse_params, 'table_name': 'unprocessed_data'},
    provide_context=True,
    dag=dag,
)

load_nds_task = PythonOperator(
    task_id='load_to_nds',
    python_callable=load_to_nds,
    op_kwargs={'postgres_params': postgres_params, 'column_map': column_map, 'schema': 'nds'},
    provide_context=True,
    dag=dag,
)

load_dds_task = PythonOperator(
    task_id='load_to_dds',
    python_callable=load_to_dds,
    op_kwargs={'postgres_params': postgres_params, 'column_map': column_map, 'schema': 'dds'},
    provide_context=True,
    dag=dag,
)

transfer_task = PythonOperator(
    task_id='transfer_of_processed_data',
    python_callable=transfer_of_processed_data,
    op_kwargs={'clickhouse_params': clickhouse_params, 'table_name': 'processed_data', 'batch_size': 100},
    provide_context=True,
    dag=dag,
)

end_task = DummyOperator(
    task_id='end_task',
    dag=dag,
)

start_task >> extract_task >> [load_nds_task, load_dds_task] >> transfer_task >> end_task