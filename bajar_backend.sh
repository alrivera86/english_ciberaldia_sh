
kill -9 $(netstat -tanpl | grep 8000  | awk '{print $7}'| awk -F '/' '{print $1}') 
kill -9 $(netstat -tanpl | grep 3000  | awk '{print $7}'| awk -F '/' '{print $1}') 
kill -9 $( ps -ef  | grep node| grep -v grep  | awk '{print $2}') 
kill -9 $( ps -ef  | grep uvicorn| grep -v grep  | awk '{print $2}') 
sleep 2
kill -9 $(netstat -tanpl | grep 8000  | awk '{print $7}'| awk -F '/' '{print $1}')
kill -9 $( ps -ef  | grep uvicorn| grep -v grep  | awk '{print $2}') 
kill -9 $(netstat -tanpl | grep 3000  | awk '{print $7}'| awk -F '/' '{print $1}') 
kill -9 $( ps -ef  | grep node| grep -v grep  | awk '{print $2}') 
echo "Baje el backend de ciberaldia e interfaz para descargar " | less /home/arivera/ciberaldia_sh/logs/uvicorn.log 2>&1 &
date
