
#cd /home/arivera/ciberaldia_sh/backend/
nohup /home/arivera/.local/bin/uvicorn ciberaldia_sh.backend.main:app --host 0.0.0.0 --port 8000 --reload 2>&1 &
/usr/bin/bash /home/arivera/ciberaldia_sh/start_dashboard.sh
echo "Subi el backend de ciberaldia Fecha abajo $(date) " 

