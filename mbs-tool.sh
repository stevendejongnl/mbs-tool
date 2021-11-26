#!/bin/bash

shopt -s nocasematch

run_dir="$PWD"

active_trydent=false

if [[ "$run_dir" == *Cloudsuite/trydent* ]]; then
  active_trydent=true
fi

SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )/scripts"

if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
. "$DIR/main.sh"
if [ "$active_trydent" = true ]; then
  . "$DIR/trydent.sh"
fi

function_list=("${function_list_main[@]}" "${function_list_trydent[@]}")


INSTANCE=""
while [[ $INSTANCE = "" ]]; do
  echo "Choice action"
  select INSTANCE in "${function_list[@]}"; do
    if [[ $INSTANCE ]]; then
      $INSTANCE
    else
      quit
    fi
    break
    done
  done
exit 0
