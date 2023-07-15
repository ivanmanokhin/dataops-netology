## Домашнее задание по теме: "Работа с виртуальными машинами в Yandex.Cloud"

1. Создать виртуальную машину с 20% vCPU

    #### Результат:

    Создание виртуальной машины:
    ```
    yc compute instance create \
      --folder-id b1g7sqtdcf0ldg35mokk \
      --zone ru-central1-a \
      --name ubuntu-cld-21 \
      --create-boot-disk image-folder-id=standard-images,image-family=ubuntu-2204-lts,size=16,type=network-hdd \
      --cores 4 \
      --core-fraction 20 \
      --memory 8 \
      --preemptible \
      --public-ip \
      --ssh-key ~/.ssh/id_rsa.pub
    done (1m4s)
    id: fhmtbvt8heofhmjues00
    folder_id: b1g7sqtdcf0ldg35mokk
    created_at: "2023-07-15T13:20:53Z"
    name: ubuntu-cld-21
    zone_id: ru-central1-a
    platform_id: standard-v2
    resources:
      memory: "8589934592"
      cores: "4"
      core_fraction: "20"
    status: RUNNING
    metadata_options:
      gce_http_endpoint: ENABLED
      aws_v1_http_endpoint: ENABLED
      gce_http_token: ENABLED
      aws_v1_http_token: DISABLED
    boot_disk:
      mode: READ_WRITE
      device_name: fhm305tusvpn6485s3mv
      auto_delete: true
      disk_id: fhm305tusvpn6485s3mv
    network_interfaces:
      - index: "0"
        mac_address: d0:0d:1d:5f:fa:88
        subnet_id: e9bbm5p5oje7fc8pescn
        primary_v4_address:
          address: 10.128.0.3
          one_to_one_nat:
            address: 158.160.109.151
            ip_version: IPV4
    gpu_settings: {}
    fqdn: fhmtbvt8heofhmjues00.auto.internal
    scheduling_policy:
      preemptible: true
    network_settings:
      type: STANDARD
    placement_policy: {}
    ```

    Удаление виртуальной машины:
    ```
    yc compute instance delete fhmtbvt8heofhmjues00
    done (25s)
    ```

2. Поработать со снимками

    #### Результат:

    Заморозка файловой системы:
    ```bash
    yc-user@fhmp6hhn78n5hu3dt72d:~$ sync
    yc-user@fhmp6hhn78n5hu3dt72d:~$ sudo fsfreeze --freeze /
    ```

    Создание снимка:
    ```
    yc compute snapshot create \
    --name ubuntu-cld-21-snapshot-$(date '+%Y%m%d') \
    --disk-id fhmpvknricrnvub0be5v
    done (38s)
    id: fd8bgqu0didehmdnfaq0
    folder_id: b1g7sqtdcf0ldg35mokk
    created_at: "2023-07-15T13:37:17Z"
    name: ubuntu-cld-21-snapshot-20230715
    storage_size: "8275361792"
    disk_size: "17179869184"
    product_ids:
      - f2e07dja1lhosh9lb56j
    status: READY
    source_disk_id: fhmpvknricrnvub0be5v
    ```

    Список снимков:
    ```
    yc compute snapshot list
    +----------------------+---------------------------------+----------------------+--------+
    |          ID          |              NAME               |     PRODUCT IDS      | STATUS |
    +----------------------+---------------------------------+----------------------+--------+
    | fd8bgqu0didehmdnfaq0 | ubuntu-cld-21-snapshot-20230715 | f2e07dja1lhosh9lb56j | READY  |
    +----------------------+---------------------------------+----------------------+--------+
    ```

    Разморозка файловой системы:
    ```bash
    yc-user@fhmp6hhn78n5hu3dt72d:~$ sudo fsfreeze --unfreeze /
    ```

    Создание диска из снимка:
    ```
    yc compute disk create fhmpvknricrnvub0be5v \
      --source-snapshot-name ubuntu-cld-21-snapshot-20230715
    done (41s)
    id: fhmao0h21r67i5blq3ef
    folder_id: b1g7sqtdcf0ldg35mokk
    created_at: "2023-07-15T13:43:34Z"
    name: fhmpvknricrnvub0be5v
    type_id: network-hdd
    zone_id: ru-central1-a
    size: "17179869184"
    block_size: "4096"
    product_ids:
      - f2e07dja1lhosh9lb56j
    status: READY
    source_snapshot_id: fd8bgqu0didehmdnfaq0
    disk_placement_policy: {}
    ```

    Удаление снимка:
    ```
    yc compute snapshot delete \
      --name ubuntu-cld-21-snapshot-20230715
    done (10s)
    ```


3. Создать группу виртуальных машин

    #### Результат:

    Спецификация группы: (specification.yaml):
    ```yaml
    name: vm-group-cld-21
    service_account_id: aje69aurhc8k22uae1m1
    instance_template:
      platform_id: standard-v3
      resources_spec:
        memory: 4g
        cores: 4
      boot_disk_spec:
        mode: READ_WRITE
        disk_spec:
          image_id: fd82sqrj4uk9j7vlki3q
          type_id: network-hdd
          size: 16g
    deploy_policy:
      max_unavailable: 1
      max_expansion: 0
    scale_policy:
      fixed_scale:
        size: 3
    allocation_policy:
      zones:
        - zone_id: ru-central1-a
    ```

    Создание группы:
    ```
    yc compute instance-group create \
      --file specification.yaml
    done (51s)
    id: cl1bf215edjhbcf9ljgl
    folder_id: b1g7sqtdcf0ldg35mokk
    created_at: "2023-07-15T13:57:24.513Z"
    name: vm-group-cld-21
    instance_template:
      platform_id: standard-v3
      resources_spec:
        memory: "4294967296"
        cores: "4"
      boot_disk_spec:
        mode: READ_WRITE
        disk_spec:
          type_id: network-hdd
          size: "17179869184"
          image_id: fd82sqrj4uk9j7vlki3q
      scheduling_policy: {}
    scale_policy:
      fixed_scale:
        size: "3"
    deploy_policy:
      max_unavailable: "1"
      strategy: PROACTIVE
    allocation_policy:
      zones:
        - zone_id: ru-central1-a
    load_balancer_state: {}
    managed_instances_state:
      target_size: "3"
    service_account_id: aje69aurhc8k22uae1m1
    status: ACTIVE
    application_load_balancer_state: {}
    ```

    Удаление группы:
    ```
    yc compute instance-group delete cl1bf215edjhbcf9ljgl
    done (1m9s)
    id: cl1bf215edjhbcf9ljgl
    folder_id: b1g7sqtdcf0ldg35mokk
    created_at: "2023-07-15T13:57:24.513Z"
    name: vm-group-cld-21
    instance_template:
      platform_id: standard-v3
      resources_spec:
        memory: "4294967296"
        cores: "4"
      boot_disk_spec:
        mode: READ_WRITE
        disk_spec:
          type_id: network-hdd
          size: "17179869184"
          image_id: fd82sqrj4uk9j7vlki3q
      scheduling_policy: {}
    scale_policy:
      fixed_scale:
        size: "3"
    deploy_policy:
      max_unavailable: "1"
      strategy: PROACTIVE
    allocation_policy:
      zones:
        - zone_id: ru-central1-a
    load_balancer_state: {}
    managed_instances_state: {}
    service_account_id: aje69aurhc8k22uae1m1
    status: DELETING
    application_load_balancer_state: {}
    ```