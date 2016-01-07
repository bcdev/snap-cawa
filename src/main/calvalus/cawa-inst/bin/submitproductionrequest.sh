#!/bin/bash

if [ "$1" = "" ]; then
  echo "usage: $0 <request>"
  exit 1
fi

java -Xmx256m -jar $CAWA_PRODUCTION_JAR -e --beam $CAWA_BEAM_VERSION --calvalus $CAWA_CALVALUS_VERSION $*
