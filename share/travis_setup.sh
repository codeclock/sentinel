#!/bin/bash
set -evx

mkdir ~/.suppocore

# safety check
if [ ! -f ~/.suppocore/.suppo.conf ]; then
  cp share/suppo.conf.example ~/.suppocore/suppo.conf
fi
