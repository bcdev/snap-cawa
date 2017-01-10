#!/bin/bash
set -e

# idepix-format-step.sh MERIS 2009-01-01 2009-01-31  /calvalus/projects/cawa/idepix-RR-fullmission/2009/01 /calvalus/projects/cawa/idepix-RR-fullmission-nc/2009/01

sensor=$1
minDate=$2
maxDate=$3
input=$4
output=$5

request=requests/idepix-format-${sensor}-${minDate}-${maxDate}.xml

cat etc/idepix-format-${sensor}-template.xml \
| sed -e "s,\${minDate},${minDate},g" -e "s,\${maxDate},${maxDate},g" -e "s,\${input},${input},g" -e "s,\${output},${output},g" > $request

#echo "java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --beam $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request"
echo "java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --snap $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request"
#java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --beam $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request
java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --snap $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request

