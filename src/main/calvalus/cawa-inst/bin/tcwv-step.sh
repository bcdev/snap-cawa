#!/bin/bash
set -e

# tcwv-step.sh MERIS 2009-10-01 2009-10-31 /calvalus/projects/cawa/idepix/meris/2009/10 /calvalus/projects/cawa/tcwv/meris/2009/10
# tcwv-step.sh MODIS 2008-01-16 2008-01-16 /calvalus/projects/cawa/idepix/modis/2008/016 /calvalus/projects/cawa/tcwv/modis/2008/016

sensor=$1
minDate=$2
maxDate=$3
input=$4
output=$5

request=requests/tcwv-${sensor}-${minDate}-${maxDate}.xml

cat etc/tcwv-${sensor}-template.xml \
| sed -e "s,\${minDate},${minDate},g" -e "s,\${maxDate},${maxDate},g" -e "s,\${input},${input},g" -e "s,\${output},${output},g" > $request

echo "java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --snap $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request"
java -Xmx256m -jar $CALVALUS_PRODUCTION_JAR -e --snap $CALVALUS_BEAM_VERSION --calvalus $CALVALUS_CALVALUS_VERSION $request

