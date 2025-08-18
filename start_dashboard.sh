#!/bin/bash
cd /home/arivera/ciberaldia_sh/interfaz_web/video-dashboard
/usr/bin/node node_modules/.bin/react-scripts start > /home/arivera/ciberaldia_sh/logs/dashboard.log 2>&1 &
echo $! > /home/arivera/ciberaldia_sh/logs/dashboard.pid

