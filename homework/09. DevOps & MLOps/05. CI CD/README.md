## Домашнее задание по теме: "CI/CD"

## Цель: 

Научиться пользоваться инструментом CI/CD GitlabCI, который позволит погрузиться в процесс автоматизации посредством написания рабочего playbook.

## Задание:
Сделать playbook .gitlab-ci.yaml по следующим критериям:

- Используем в тасках tag - netology
- Шаги - build, test
- В билде должен выполняться скрипт из шагов: 
  * начало Building
  * создание папки build
  * создание файла в этой папке info.txt
- В тесте:
  * выводим Testing
  * проверяем наличие файла info.txt в папке build 

## Результат: 
- Файлы:
    * [.gitlab-ci.yml](./.gitlab-ci.yml)

- Логи jobs:
    * <details>
        <summary>Лог build</summary>

        ```bash
        Running with gitlab-runner 16.4.1 (d89a789a)
          on netology R3z1jrba7, system ID: s_1f017d8835a8
        Preparing the "shell" executor
        00:00
        Using Shell (bash) executor...
        Preparing environment
        00:00
        Running on ubuntu...
        Getting source from Git repository
        00:00
        Fetching changes with git depth set to 20...
        Reinitialized existing Git repository in /root/builds/R3z1jrba7/0/manokhin/netology-ml/.git/
        Checking out c6d2a74b as detached HEAD (ref is main)...
        Skipping Git submodules setup
        Executing "step_script" stage of the job script
        00:00
        $ echo "Building"
        Building
        $ mkdir build
        $ touch build/info.txt
        Uploading artifacts for successful job
        00:01
        Uploading artifacts...
        Runtime platform                                    arch=amd64 os=linux pid=2769 revision=d89a789a version=16.4.1
        build: found 2 matching artifact files and directories 
        Uploading artifacts as "archive" to coordinator... 201 Created  id=15 responseStatus=201 Created token=64_CUEHm
        Cleaning up project directory and file based variables
        00:00
        Job succeeded
        ```
      </details>
    * <details>
        <summary>Лог test</summary>

        ```bash
        Running with gitlab-runner 16.4.1 (d89a789a)
          on netology R3z1jrba7, system ID: s_1f017d8835a8
        Preparing the "shell" executor
        00:00
        Using Shell (bash) executor...
        Preparing environment
        00:00
        Running on ubuntu...
        Getting source from Git repository
        00:00
        Fetching changes with git depth set to 20...
        Reinitialized existing Git repository in /root/builds/R3z1jrba7/0/manokhin/netology-ml/.git/
        Checking out c6d2a74b as detached HEAD (ref is main)...
        Removing build/
        Skipping Git submodules setup
        Downloading artifacts
        00:00
        Downloading artifacts for build (15)...
        Runtime platform                                    arch=amd64 os=linux pid=2848 revision=d89a789a version=16.4.1
        Downloading artifacts from coordinator... ok        host=manokhin.gitlab.yandexcloud.net id=15 responseStatus=200 OK token=64_eyST3
        Executing "step_script" stage of the job script
        00:00
        $ echo "Testing"
        Testing
        $ if [ -f build/info.txt ]; then echo "File exist"; else echo "File doesn't exist"; exit 1; fi
        File exist
        Cleaning up project directory and file based variables
        00:00
        Job succeeded
        ```
      </details>

- Скриншот:
    ![](./assets/images/pipeline.png)