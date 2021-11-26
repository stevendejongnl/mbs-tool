#!/bin/bash

function_list_trydent=("trydent_functions")

trydent_functions() {
  function_list_intern=("delete_sphinx" "update_database" "clear_redis")
  INSTANCE=""
  while [[ $INSTANCE = "" ]]; do
    echo "Choice action"
    select INSTANCE in "${function_list_intern[@]}"; do
      if [[ $INSTANCE ]]; then
        $INSTANCE
      else
        quit
      fi
      break
      done
    done
  exit 0
}

delete_sphinx() {
  sphinx_data="${CUSTOMER}-sphinx-data"
  docker-compose down
  sleep 15
  docker volume rm "$sphinx_data"
  sleep 5
  docker-compose up -d trytond webshop shopproxy
  docker-compose logs -f webshop
}

update_database() {
  docker-compose exec trytond /srv/trytond/bin/trytond -d fixture --all -v
}

clear_redis() {
  docker-compose exec redis redis-cli flushall
}
