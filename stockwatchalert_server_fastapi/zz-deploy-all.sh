echo 'Deploying Server All'

bash zz-deploy-api.sh
bash zz-deploy-api-websocket.sh
bash zz-deploy-engines-driver.sh
bash zz-deploy-engines-worker.sh

echo 'Deployed Server All'
