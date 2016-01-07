#!/bin/bash
set -e

# tcwv-step.sh 2009-10-01 2009-10-31 /calvalus/projects/cawa/idepix-RR-fullmission/2009/10 /calvalus/projects/cawa/tcwv-meris-fullmission/2009/10

minDate=$1
maxDate=$2
input=$3
output=$4

request=requests/tcwv-${minDate}-${maxDate}.xml

cat etc/tcwv-template.xml \
| sed -e "s,\${minDate},${minDate},g" -e "s,\${maxDate},${maxDate},g" -e "s,\${input},${input},g" -e "s,\${output},${output},g" > $request

echo "java -Xmx256m -jar $CAWA_PRODUCTION_JAR -e --beam $CAWA_BEAM_VERSION --calvalus $CAWA_CALVALUS_VERSION $request"
java -Xmx256m -jar $CAWA_PRODUCTION_JAR -e --beam $CAWA_BEAM_VERSION --calvalus $CAWA_CALVALUS_VERSION $request

