## Домашнее задание по теме: "Docker и микросервисная архитектура"

## **Цель**: 

Закрепить полученные знания по технологии контейнеризации Docker путём написания dockerfile с последующей сборкой и подъёмом на его базе докер-контейнера.

## **Задание**:
Необходимо сделать dockerfile для получения рабочего контейнера.
1.  В качестве основы, берём образ continuumio/miniconda3:latest
2.  Добавляем и делаем рабочей папкой /app 
3.  Создаём простой sh файл с названием 1.sh, который должен выдавать надпись “Hello Netology”.
4.  Надо скопировать этот файл внутрь контейнера и выдать ему права на исполнение.
5.  Запустить установку пакетов python mlflow boto3 pymysql.
6.  В конце запустить на вывод файл 1.sh.
7.  После чего собрать через docker build контейнер с тегом netology-ml:netology-ml

## **Результат**: 
- полученный dockerfile:
    * [Dockerfile](./Dockerfile)
- лог выполнения сборки:
    * <details>
        <summary>Лог сборки образа</summary>
  
        ```bash
        :~# docker build -t netology-ml:netology-ml .
        [+] Building 356.7s (10/10) FINISHED                                                                                                       docker:default
         => [internal] load .dockerignore                                                                                                                    0.1s
         => => transferring context: 2B                                                                                                                      0.0s
         => [internal] load build definition from Dockerfile                                                                                                 0.1s
         => => transferring dockerfile: 186B                                                                                                                 0.0s
         => [internal] load metadata for docker.io/continuumio/miniconda3:latest                                                                             1.7s
         => [1/5] FROM docker.io/continuumio/miniconda3:latest@sha256:42cd2ca0ece04579b6127e1a1a0f83c25a079145d408eb65e39206ac05069a77                      12.2s
         => => resolve docker.io/continuumio/miniconda3:latest@sha256:42cd2ca0ece04579b6127e1a1a0f83c25a079145d408eb65e39206ac05069a77                       0.1s
         => => sha256:a4686437ef419b54dce6e0bfa5a47a4e21b0c1615827e4697b7cc6bf016dce60 109.18MB / 109.18MB                                                   4.2s
         => => sha256:42cd2ca0ece04579b6127e1a1a0f83c25a079145d408eb65e39206ac05069a77 3.11kB / 3.11kB                                                       0.0s
         => => sha256:77f9119def83d94b7afb654b39a1c21aaa7f255518aba57de08321760c27c86a 869B / 869B                                                           0.0s
         => => sha256:a101d1f8cd1cbfc6b0e91e4f1ce03e48a6bdca7987168647044a497e57411c56 4.90kB / 4.90kB                                                       0.0s
         => => sha256:9d21b12d5fab9ab82969054d72411ce627c209257df64b6057016c981e163c30 31.42MB / 31.42MB                                                     0.9s
         => => sha256:eb0f38cf74ca793b7d7898c36d5c5b1e2fc078e4c8781e2d9de4b2e919fbf05f 50.07MB / 50.07MB                                                     1.7s
         => => extracting sha256:9d21b12d5fab9ab82969054d72411ce627c209257df64b6057016c981e163c30                                                            3.0s
         => => extracting sha256:eb0f38cf74ca793b7d7898c36d5c5b1e2fc078e4c8781e2d9de4b2e919fbf05f                                                            2.0s
         => => extracting sha256:a4686437ef419b54dce6e0bfa5a47a4e21b0c1615827e4697b7cc6bf016dce60                                                            4.4s
         => [internal] load build context                                                                                                                    0.1s
         => => transferring context: 73B                                                                                                                     0.0s
         => [2/5] WORKDIR /app                                                                                                                               8.3s
         => [3/5] COPY 1.sh /app/                                                                                                                            0.4s
         => [4/5] RUN chmod +x /app/1.sh                                                                                                                     0.7s
         => [5/5] RUN conda install -y mlflow boto3 pymysql                                                                                                 81.0s
         => exporting to image                                                                                                                             252.1s
         => => exporting layers                                                                                                                            252.0s 
         => => writing image sha256:a6a9ff3d2a2f1dfefe2bee19cf53dd1f727baa9839e1a5d5d624d6b45728fc01                                                         0.0s 
         => => naming to docker.io/library/netology-ml:netology-ml                                                                                           0.0s
        ```
      </details>
    * <details>
        <summary>Запуск контейнера</summary>
  
        ```bash
        :~# docker run netology-ml:netology-ml
        Hello Netology
        ```
      </details>
    * [Образ на Docker Hub](https://hub.docker.com/r/manokhin/netology-ml/tags)
