terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
      version = "0.84.0"
    }
  }
}

provider "yandex" {
  zone      = "ru-central1-a"
}

resource "yandex_serverless_container" "nodejs" {
   name               = "nodejs"
   memory             = 256
   service_account_id = "aje869sfthp1h04unodj"
   image {
       url = "cr.yandex/crpmqifoj5k2rdnn95nl/nodejs:0.1"
   }
}