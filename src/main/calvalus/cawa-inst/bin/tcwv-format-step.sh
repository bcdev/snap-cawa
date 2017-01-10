#!/bin/bash
set -e

# tcwv-format-step.sh 2009-01-01 2009-01-31  /calvalus/projects/cawa/tcwv-fullmission/2009/01 /calvalus/projects/cawa/tcwv-fullmission-nc/2009/01

sensor=$1
minDate=$2
maxDate=$3
input=$4
output=$5

request=requests/tcwv-format-${sensor}-${minDate}-${maxDate}.xml

cat etc/tcwv-format-${sensor}-template.xml \
| sed -e "s,\${minDate},${minDate},g" -e "s,\${maxDate},${maxDate},g" -e "s,\${input},${input},g" -e "s,\${output},${output},g" > $request

echo "java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --snap $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request"
java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --snap $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request

