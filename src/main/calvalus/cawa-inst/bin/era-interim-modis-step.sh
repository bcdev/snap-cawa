#!/bin/bash
set -e

# era-interim-step.sh MODIS 2008-01-16 2008-01-16 /mnt/hdfs/calvalus/projects/cawa/MODIS_MYD021KM/2008/016 /calvalus/projects/cawa/era-interim_modis/2008/016

sensor=$1
minDate=$2
maxDate=$3
input=$4
output=$5

request=requests/era-interim-$sensor-${minDate}-${maxDate}.xml

cat etc/era-interim-${sensor}-template.xml \
| sed -e "s,\${sensor},${sensor},g" -e "s,\${minDate},${minDate},g" -e "s,\${maxDate},${maxDate},g" -e "s,\${input},${input},g" -e "s,\${output},${output},g" > $request

#echo "java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --beam $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request"
echo "java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --snap $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request"
#java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --beam $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request
java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --snap $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request

