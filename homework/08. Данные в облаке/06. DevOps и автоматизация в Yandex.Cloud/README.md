## Домашнее задание по теме: "DevOps и автоматизация в Yandex.Cloud"

### Задание: Создать serverless контейнер с помощью terraform

1. Создайте контейнер используя код из [примера документаци](https://cloud.yandex.ru/docs/serverless-containers/quickstart#primery-prilozhenij-i-dockerfile) и и положите его в container registry

    #### Результат:

    Сборка образа:
    ```bash
    docker build . \
    >   -t cr.yandex/crpmqifoj5k2rdnn95nl/nodejs:0.1
    [+] Building 4.6s (9/9) FINISHED                                                                                                                                                         
     => [internal] load .dockerignore                                                                                                                                                   0.4s
     => => transferring context: 2B                                                                                                                                                     0.0s
     => [internal] load build definition from Dockerfile                                                                                                                                0.5s
     => => transferring dockerfile: 144B                                                                                                                                                0.0s
     => [internal] load metadata for docker.io/library/node:16-slim                                                                                                                     3.7s
     => [internal] load build context                                                                                                                                                   0.2s
     => => transferring context: 30B                                                                                                                                                    0.0s
     => [1/4] FROM docker.io/library/node:16-slim@sha256:f9b352a2b524dd1c56c65e0cb365f7517093a7d3298f41a8e85dd034a6f33474                                                               0.0s
     => CACHED [2/4] WORKDIR /app                                                                                                                                                       0.0s
     => CACHED [3/4] RUN npm install express                                                                                                                                            0.0s
     => CACHED [4/4] COPY ./index.js .                                                                                                                                                  0.0s
     => exporting to image                                                                                                                                                              0.1s
     => => exporting layers                                                                                                                                                             0.0s
     => => writing image sha256:3e659bf07849432420c921207345fb3677b984bb7c0af39296e56ec6b8f93a00                                                                                        0.1s
     => => naming to cr.yandex/crpmqifoj5k2rdnn95nl/nodejs:0.1                                                                                                                          0.1s
    ```

    Пуш образа в registry:
    ```bash
    docker push cr.yandex/crpmqifoj5k2rdnn95nl/nodejs:0.1
    The push refers to repository [cr.yandex/crpmqifoj5k2rdnn95nl/nodejs]
    599cab3bbf2d: Pushed 
    80465176c2a0: Pushed 
    9fa6bba5824e: Pushed 
    ffc136f837e3: Pushed 
    33792ec58d86: Pushed 
    e9749f2c1438: Pushed 
    3dd37d21f53f: Pushed 
    a51779df6d64: Pushed 
    0.1: digest: sha256:5804f429f6ae4737553c5a35479861b38a1cdae08d9be196219105a62e8bb828 size: 199
    ```

    Проверка наличия образа в registry:
    ```bash
    yc container image list
    +----------------------+---------------------+-----------------------------+------+-----------------+
    |          ID          |       CREATED       |            NAME             | TAGS | COMPRESSED SIZE |
    +----------------------+---------------------+-----------------------------+------+-----------------+
    | crp4lsnd2oktse363isp | 2023-07-17 07:02:48 | crpmqifoj5k2rdnn95nl/nodejs |  0.1 | 64.1 MB         |
    +----------------------+---------------------+-----------------------------+------+-----------------+
    ```

2. Опишите деплой serverless контейнера с помощью terraform

    #### Результат:

    Деплой контейнера описан в файле [main.tf](./main.tf)

    Токен/каталог/фолдер заданы через переменные окружения

    Планирование:
    ```bash
    terraform plan
    
    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create
    
    Terraform will perform the following actions:
    
      # yandex_serverless_container.nodejs will be created
      + resource "yandex_serverless_container" "nodejs" {
          + core_fraction      = (known after apply)
          + cores              = 1
          + created_at         = (known after apply)
          + execution_timeout  = (known after apply)
          + folder_id          = (known after apply)
          + id                 = (known after apply)
          + memory             = 256
          + name               = "nodejs"
          + revision_id        = (known after apply)
          + service_account_id = "aje869sfthp1h04unodj"
          + url                = (known after apply)
    
          + image {
              + digest = (known after apply)
              + url    = "cr.yandex/crpmqifoj5k2rdnn95nl/nodejs:0.1"
            }
        }
    
    Plan: 1 to add, 0 to change, 0 to destroy.
    ```

    Применение конфигурации:
    ```bash
    terraform apply --auto-approve
    
    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create
    
    Terraform will perform the following actions:
    
      # yandex_serverless_container.nodejs will be created
      + resource "yandex_serverless_container" "nodejs" {
          + core_fraction      = (known after apply)
          + cores              = 1
          + created_at         = (known after apply)
          + execution_timeout  = (known after apply)
          + folder_id          = (known after apply)
          + id                 = (known after apply)
          + memory             = 256
          + name               = "nodejs"
          + revision_id        = (known after apply)
          + service_account_id = "aje869sfthp1h04unodj"
          + url                = (known after apply)
    
          + image {
              + digest = (known after apply)
              + url    = "cr.yandex/crpmqifoj5k2rdnn95nl/nodejs:0.1"
            }
        }
    
    Plan: 1 to add, 0 to change, 0 to destroy.
    yandex_serverless_container.nodejs: Creating...
    yandex_serverless_container.nodejs: Still creating... [10s elapsed]
    yandex_serverless_container.nodejs: Creation complete after 17s [id=bba4ftokchlc6svh0e97]
    
    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

    Проверка контейнера в Serverless Containers:
    ```bash
    yc serverless container list
    +----------------------+--------+----------------------+--------+
    |          ID          |  NAME  |      FOLDER ID       | STATUS |
    +----------------------+--------+----------------------+--------+
    | bba4ftokchlc6svh0e97 | nodejs | b1g7sqtdcf0ldg35mokk | ACTIVE |
    +----------------------+--------+----------------------+--------+
    ```

    Удаление созданного контейнера:
    ```bash
    terraform destroy --auto-approve
    yandex_serverless_container.nodejs: Refreshing state... [id=bba4ftokchlc6svh0e97]
    
    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      - destroy
    
    Terraform will perform the following actions:
    
      # yandex_serverless_container.nodejs will be destroyed
      - resource "yandex_serverless_container" "nodejs" {
          - concurrency        = 0 -> null
          - core_fraction      = 100 -> null
          - cores              = 1 -> null
          - created_at         = "2023-07-17T07:45:35Z" -> null
          - execution_timeout  = "10s" -> null
          - folder_id          = "b1g7sqtdcf0ldg35mokk" -> null
          - id                 = "bba4ftokchlc6svh0e97" -> null
          - labels             = {} -> null
          - memory             = 256 -> null
          - name               = "nodejs" -> null
          - revision_id        = "bba8prhb548qoggqb74j" -> null
          - service_account_id = "aje869sfthp1h04unodj" -> null
          - url                = "https://bba4ftokchlc6svh0e97.containers.yandexcloud.net/" -> null
    
          - image {
              - args        = [] -> null
              - command     = [] -> null
              - digest      = "sha256:5804f429f6ae4737553c5a35479861b38a1cdae08d9be196219105a62e8bb828" -> null
              - environment = {} -> null
              - url         = "cr.yandex/crpmqifoj5k2rdnn95nl/nodejs:0.1" -> null
            }
        }
    
    Plan: 0 to add, 0 to change, 1 to destroy.
    yandex_serverless_container.nodejs: Destroying... [id=bba4ftokchlc6svh0e97]
    yandex_serverless_container.nodejs: Destruction complete after 5s
    
    Destroy complete! Resources: 1 destroyed.
    ```