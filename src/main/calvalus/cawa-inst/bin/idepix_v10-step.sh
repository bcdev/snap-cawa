#!/bin/bash
set -e

# idepix_v10-step.sh MERIS 2009-10-01 2009-10-31 /calvalus/projects/eodata/MER_RR__1P/r03/2009/10 /calvalus/projects/cawa/era-interim-meris/2009/10 /calvalus/projects/cawa/idepix-RR-fullmission/2009/10

sensor=$1
minDate=$2
maxDate=$3
input=$4
erainterim=$5
output=$6

request=requests/idepix-${sensor}_v10-${minDate}-${maxDate}.xml

cat etc/idepix-${sensor}_v10-template.xml \
| sed -e "s,\${minDate},${minDate},g" -e "s,\${maxDate},${maxDate},g" -e "s,\${input},${input},g" -e "s,\${erainterim},${erainterim},g" -e "s,\${output},${output},g" > $request

#echo "java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --beam $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request"
echo "java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --snap $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request"
#java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --beam $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request
java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --snap $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request

