#!/bin/bash

function_list_trydent=("'Trydent', trydent_functions")

trydent_functions() {
  function_list_intern=(
    "'Delete Sphinx', delete_sphinx"
    "'Update Database', update_database"
    "'Flush Redis', flush_redis"
  )
  INSTANCE=""
  while [[ $INSTANCE = "" ]]; do
    echo "Trydent"

    select INSTANCE in "${function_list_intern[@]}"; do
      if [[ $INSTANCE ]]; then
        run_function_array=("${INSTANCE[@]//,/}")
        run_function=${run_function_array[${#run_function_array[@]}-1]}
        ${run_function}
      else
        quit
      fi
      break
      done
    done
  exit 0
}

docker_yml_check() {
  docker_compose_yml="${run_dir}/docker-compose.yml"
  docker_compose_override_yml="${run_dir}/docker-compose.override.yml"
  docker_compose_run="-f ${docker_compose_yml}"

  if ! test -f "${docker_compose_yml}"; then
    echo "$docker_compose_yml doesn't exists."
  fi
  if test -f "${docker_compose_override_yml}"; then
    docker_compose_run="${docker_compose_run} -f ${docker_compose_override_yml}"
  fi
}

delete_sphinx() {
  echo "Trydent Delete Sphinx"
  sphinx_data="${CUSTOMER}-sphinx-data"
  ${docker_yml_check}

  docker-compose $docker_compose_run down
  sleep 15
  docker volume rm "$sphinx_data"
  sleep 5
  docker-compose $docker_compose_run up -d trytond webshop shopproxy
  docker-compose $docker_compose_run logs -f webshop
}

update_database() {
  echo "Trydent Update Database"
  ${docker_yml_check}

  docker-compose $docker_compose_run exec trytond /srv/trytond/bin/trytond -d fixture --all -v
}

flush_redis() {
  echo "Trydent Flush Redis"
  ${docker_yml_check}

  docker-compose $docker_compose_run exec redis redis-cli flushall
}
