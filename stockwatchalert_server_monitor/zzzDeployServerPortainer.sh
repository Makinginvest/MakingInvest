echo 'Deploying Portainer'

rsync -avrmR --exclude='node*modules/' --include='.env' --exclude='.*' --include='\_/' ./ root@5.78.84.141:/root/makinginvest-portainer --delete

ssh -t root@5.78.84.141 << ENDSSH

    cd makinginvest-portainer/ && sudo docker-compose up -d --build makinginvest-portainer

    exit
ENDSSH
    echo 'Deployed Portainer'
