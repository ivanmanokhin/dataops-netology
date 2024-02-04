from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from kaggle.api.kaggle_api_extended import KaggleApi
import pandas as pd
from clickhouse_driver import Client

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

def connect_to_clickhouse(**kwargs):
    '''Функция для подключения к ClickHouse'''
    return Client(host=kwargs['host'],
                  port=kwargs['port'],
                  database=kwargs['database'])

def remove_rows_with_nulls(df):
    '''Функция для очистки датасета от строк, в которых есть значения Null'''
    df_len = df.shape[0]
    df = df.dropna()
    print(f'Проверка значений на Null выполнена (удалено {df_len - df.shape[0]} строк)')
    return df

def validate_data(df, attrv_dict):
    '''Функция для проверки данных в датасете'''
    df_len = df.shape[0]

    # Проверка формата invoice_id
    df = df[df['id'].str.match(r'^\d{3}-\d{2}-\d{4}$')]

    # Проверка допустимых значений для атрибутов
    df = df[df['branch'].isin(attrv_dict['branches'])]
    df = df[df['city'].isin(attrv_dict['cities'])]
    df = df[df['customer_type'].isin(attrv_dict['customer_types'])]
    df = df[df['gender'].isin(attrv_dict['genders'])]
    df = df[df['payment_method'].isin(attrv_dict['payment_methods'])]
    
    print(f'Данные валидированы (удалено {df_len - df.shape[0]} строк)')

    return df

def insert_date_into_clickhouse(clickhouse_client, table_name, column_names, batch_size, df):
    '''Функция для добавления данных в ClickHouse'''
    for i in range(0, len(df), batch_size):
        batch_df = df.iloc[i:i + batch_size]
        print(f'Подготовлен батч размером {batch_df.shape[0]}')
        clickhouse_client.execute(f'INSERT INTO {table_name} ({", ".join(column_names)}) VALUES', batch_df.to_dict(orient='records'))
        print(f'  Загружено {batch_df.shape[0]} строк')

def download_dataset_from_kaggle(**kwargs):
    '''Функция для получения загрузки датасета из Kaggle'''
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files(kwargs['dataset_id'], kwargs['dataset_path'], unzip=True)
    print('Датасет успешно загружен')

def load_into_clickhouse(**kwargs):
    attrv_dict = {
        'branches' : ['A', 'B', 'C'],
        'cities' : ['Yangon', 'Naypyitaw', 'Mandalay'],
        'customer_types' : ['Member', 'Normal'],
        'genders' : ['Male', 'Female'],
        'payment_methods' : ['Cash', 'Ewallet', 'Credit card'],
    }

    column_names = ['id', 'branch', 'city', 'customer_type', 'gender',
                    'product_line', 'unit_price', 'quantity', 'tax',
                    'total', 'date', 'time', 'payment_method', 'cogs',
                    'gross_margin_percentage', 'gross_income', 'rating']

    df = pd.read_csv(f"{kwargs['dataset_path']}/supermarket_sales - Sheet1.csv", header=None, names=column_names, skiprows=1)
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x) # удаление пробелов из значений
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time']) # перевод даты в формат datetime
    df.drop(columns=['date'], inplace=True)  # удаление ненужных столбцов
    df.drop(columns=['time'], inplace=True)
    column_names = df.columns.tolist()

    # удаление строк с Null значениями
    df = remove_rows_with_nulls(df)

    # валидация формата и допустимых значений
    df = validate_data(df, attrv_dict)

    if df.shape[0] > 0:
        # загрузка данных в ClickHouse
        clickhouse_client = connect_to_clickhouse(**kwargs['clickhouse_params'])
        insert_date_into_clickhouse(clickhouse_client, kwargs['table_name'], column_names, kwargs['batch_size'], df)
        clickhouse_client.disconnect()
        print(f'Данные успешно загружены в ClickHouse ({df.shape[0]})')
    else:
        print(f'Данные отсутствуют')

dag = DAG(
    'data_load_dag',
    default_args=default_args,
    description='DAG для извлечения, первичной обработки и перемещения данных',
    #schedule_interval=timedelta(days=1),
    schedule_interval="@daily"
)

start_task = DummyOperator(
    task_id='start_task',
    dag=dag,
)

download_dataset_task = PythonOperator(
    task_id='download_dataset_task',
    python_callable=download_dataset_from_kaggle,
    op_kwargs={'dataset_id': 'aungpyaeap/supermarket-sales','dataset_path': './supermarket-sales'},
    dag=dag,
)

load_unprocessed_data_task = PythonOperator(
    task_id='load_unprocessed_data_task',
    python_callable=load_into_clickhouse,
    op_kwargs={'dataset_path': './supermarket-sales', 'clickhouse_params': clickhouse_params, 'table_name': 'unprocessed_data', 'batch_size': 100},
    dag=dag,
)

end_task = DummyOperator(
    task_id='end_task',
    dag=dag,
)

start_task >> download_dataset_task >> load_unprocessed_data_task >> end_task
