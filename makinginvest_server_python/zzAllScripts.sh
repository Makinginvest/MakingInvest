echo 'Deploying Server All'

bash zzDeployServerApi.sh
bash zzDeployServerData.sh
bash zzDeployServerDataWs.sh
bash zzDeployServerEnginesAll.sh
bash zzDeployServerEnginesMain.sh

echo 'Deployed Server All'
