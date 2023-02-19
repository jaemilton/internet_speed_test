#!/bin/bash
SECONDS=0
MYSQLHOST=$1
DATABASE=$2
#echo "PATH >>> $PATH"
export PYTHONHOME="/usr"

full_path=$(realpath $0)
dir_path=$(dirname $full_path)
#echo "dir_path=$dir_path"

if [ -f  $dir_path/.env ]
then
  #echo ">>>>>> reading variables from $dir_path/.env"
  export $(cat $dir_path/.env | sed 's/#.*//g' | xargs)
else
  echo ">>>>>> variables file $dir_path/.env not found"
fi

USR_VAR=USR_${DATABASE^^}
USERNAME=${!USR_VAR}

PWD_VAR=PWD_${DATABASE^^}
PASSWORD=${!PWD_VAR}

python3.9 /root/git/internet_speed_test/internet_speed_test.py --database --host $MYSQLHOST --user $USERNAME --password $PASSWORD --database_name $DATABASE

eval "echo Elapsed time: $(date -ud "@$SECONDS" +'$((%s/3600/24)) days %H hr %M min %S sec')"
