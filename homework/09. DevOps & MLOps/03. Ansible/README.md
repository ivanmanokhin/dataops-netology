## Домашнее задание по теме: "Ansible"

## Цель: 

Написать рабочий playbook Ansible, чтобы научится работать с ansible, его синтаксисом, и понимать, как через него настраивается раскатка ПО.

## Задание:
Необходимо написать playbook Ansible, который будет в себе содержать:
1. Имя плейбука homework.yaml
2. inventory, из минимум 1 хоста, если есть возможность, то 2 лучше
3. Авторизация должна быть настроена через техническую уз ansible
4. Наименование netology-ml
5. Проверка через метод ping доступность хостов
6. Через var установка пакетов net_tools, git, tree, htop, mc, vim
7. Использование update
8. Копирование текстового файла test.txt
9. Создание в цикле групп пользователей devops_1, test_1 с созданием пользователей и директорий home devops_1, test_1

## Результат: 
- Файлы:
    * [inventory](./ansible/inventory/hosts.yaml)
    * [group_vars](./ansible/group_vars/all.yaml)
    * [playbook](./ansible/homework.yaml)

- Логи:
    * <details>
        <summary>Лог выполнения плейбука</summary>

        ```bash
        [/ansible(main)]> ansible-playbook -i inventory/hosts.yaml homework.yaml
        
        PLAY [all] ***********************************************************************************************************************************************
        
        TASK [Gathering Facts] ***********************************************************************************************************************************
        ok: [netology-ml-01]
        ok: [netology-ml-02]
        
        TASK [ping servers] **************************************************************************************************************************************
        ok: [netology-ml-02]
        ok: [netology-ml-01]
        
        TASK [install packages] **********************************************************************************************************************************
        changed: [netology-ml-01] => (item=net-tools)
        ok: [netology-ml-01] => (item=git)
        changed: [netology-ml-02] => (item=net-tools)
        changed: [netology-ml-01] => (item=tree)
        ok: [netology-ml-02] => (item=git)
        ok: [netology-ml-01] => (item=htop)
        changed: [netology-ml-02] => (item=tree)
        ok: [netology-ml-02] => (item=htop)
        changed: [netology-ml-01] => (item=mc)
        ok: [netology-ml-01] => (item=vim)
        changed: [netology-ml-02] => (item=mc)
        ok: [netology-ml-02] => (item=vim)
        
        TASK [update all packages] *******************************************************************************************************************************
        ok: [netology-ml-01]
        ok: [netology-ml-02]
        
        TASK [copy test.txt] *************************************************************************************************************************************
        changed: [netology-ml-01]
        changed: [netology-ml-02]
        
        TASK [create users] **************************************************************************************************************************************
        changed: [netology-ml-01] => (item=devops_1)
        changed: [netology-ml-02] => (item=devops_1)
        changed: [netology-ml-01] => (item=test_1)
        changed: [netology-ml-02] => (item=test_1)
        
        PLAY RECAP ***********************************************************************************************************************************************
        netology-ml-01             : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
        netology-ml-02             : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
        ```
      </details>