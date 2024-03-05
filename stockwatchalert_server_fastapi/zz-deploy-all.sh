echo 'deploying server all'

bash zz-deploy-api.sh
bash zz-deploy-data-ws.sh
bash zz-deploy-data.sh
bash zz-deploy-engines-all.sh
bash zz-deploy-engines-main.sh

echo 'deployed server all'
