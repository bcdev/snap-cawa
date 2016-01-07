#!/bin/bash
set -e

# idepix-step.sh 2009-10-01 2009-10-31 /calvalus/projects/eodata/MER_RR__1P/r03/2009/10 /calvalus/projects/cawa/idepix-RR-fullmission/2009/10

minDate=$1
maxDate=$2
input=$3
output=$4

request=requests/idepix-${minDate}-${maxDate}.xml

cat etc/idepix-template.xml \
| sed -e "s,\${minDate},${minDate},g" -e "s,\${maxDate},${maxDate},g" -e "s,\${input},${input},g" -e "s,\${output},${output},g" > $request

echo "java -Xmx256m -jar $CAWA_PRODUCTION_JAR -e --beam $CAWA_BEAM_VERSION --calvalus $CAWA_CALVALUS_VERSION $request"
java -Xmx256m -jar $CAWA_PRODUCTION_JAR -e --beam $CAWA_BEAM_VERSION --calvalus $CAWA_CALVALUS_VERSION $request

