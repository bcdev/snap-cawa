#!/bin/bash
set -e

# format-step.sh 2009-01-01 2009-01-31  /calvalus/projects/cawa/idepix-RR-fullmission/2009/01 /calvalus/projects/cawa/idepix-RR-fullmission/2009/01

minDate=$1
maxDate=$2
input=$3
output=$4

request=requests/format-${minDate}-${maxDate}.xml

cat etc/format-template.xml \
| sed -e "s,\${minDate},${minDate},g" -e "s,\${maxDate},${maxDate},g" -e "s,\${input},${input},g" -e "s,\${output},${output},g" > $request

echo "java -Xmx256m -jar $CAWA_PRODUCTION_JAR -e --beam $CAWA_BEAM_VERSION --calvalus $CAWA_CALVALUS_VERSION $request"
java -Xmx256m -jar $CAWA_PRODUCTION_JAR -e --beam $CAWA_BEAM_VERSION --calvalus $CAWA_CALVALUS_VERSION $request

