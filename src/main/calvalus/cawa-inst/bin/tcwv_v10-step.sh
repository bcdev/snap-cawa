#!/bin/bash
set -e

# tcwv_v10-step.sh MERIS 2009-10-01 2009-10-31 /calvalus/projects/cawa/idepix/meris/2009/10 /calvalus/projects/cawa/tcwv/meris/2009/10

sensor=$1
minDate=$2
maxDate=$3
input=$4
output=$5

request=requests/tcwv-${sensor}_v10-${minDate}-${maxDate}.xml

cat etc/tcwv-${sensor}_v10-template.xml \
| sed -e "s,\${minDate},${minDate},g" -e "s,\${maxDate},${maxDate},g" -e "s,\${input},${input},g" -e "s,\${output},${output},g" > $request

echo "java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --snap $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request"
java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --snap $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request

