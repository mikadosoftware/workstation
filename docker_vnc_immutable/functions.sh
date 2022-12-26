#!/bin/bash
declare -F psup >/dev/null 2>&1 || function psup(){ if [ $# -eq 0 ]; then echo "Usage: psup pid" >&2;else while [ $# -gt 0 ]; do if [ ${1} -ne 0 ]; then pid=${1};ps -edf | awk -vpid=${pid} '{ if( $2==pid ) { printf("%s\n", $0); } }';psup `ps -edf | awk -vpid=${pid} '{ if( $2==pid ) printf("%s\n", $3); }'`;else echo;fi;shift;done;fi;}
declare -F psdown >/dev/null 2>&1 || function psdown(){ if [ $# -eq 0 ]; then echo "Usage: psdown pid" >&2;return 1;else psdown_level=`echo $1|awk '{ if(substr($0,1,1)=="p") printf("%s",substr($0,2));else printf("0"); }'`;if [ ${psdown_level} -ne 0 ]; then shift;fi;while [ $# -gt 0 ]; do pid=${1};if [ `ps -edf|awk '{print $2}'|grep ${pid}|wc -l` -gt 0 ]; then ps -edf|awk -vpid=${pid} -vlevel=${psdown_level} '{ if( $2==pid ) { if(level>0) for(i=1;i<=level;i++) printf("  "); printf("%s\n", $0); } }';if [ `ps -edf|awk '{print $3}'|grep ${pid}|wc -l` -gt 0 ]; then psdown_level=$(( ${psdown_level} + 1 ));psdown p${psdown_level} `ps -edf | awk -vpid=${pid} '{ if( $3==pid ) printf("%s ", $2); }'`;psdown_level=$(( ${psdown_level} - 1 ));fi;fi;shift;done;fi;}
declare -F killdown >/dev/null 2>&1 || function killdown(){ if [ $# -eq 0 ]; then echo "Usage: killdown pid" >&2;return 1;else while [ $# -gt 0 ]; do if [ ${1} -ne 1 ]; then if [ `ps -edf|awk '{print $2}'|grep ${1}|wc -l` -gt 0 ]; then if [ `ps -edf|awk '{print $3}'|grep ${1}|wc -l` -gt 0 ]; then killdown `ps -edf | awk -vpid=${1} '{ if( $3==pid ) printf("%s ", $2); }'`;fi;fi;kill -9 ${1} 2> /dev/null;shift;fi;done;fi;}
declare -F addcerts >/dev/null 2>&1 || function addcerts() {
for f in $(ls -1 /usr/local/share/ca-certificates/* 2>/dev/null) ; do 
  certificateFile="$f"
  certificateName="MyCA Name - $f" 
  for certDB in $(find  ~/.mozilla* ~/.thunderbird -name "cert9.db" 2>/dev/null)
  do
    certDir=$(dirname ${certDB});
    echo "install certificate ${certificateFile} in Mozilla profile ${certDir}"
    certutil -A -n "${certificateName}" -t "TCu,Cuw,Tuw" -i ${certificateFile} -d sql:${certDir}
  done
done
}