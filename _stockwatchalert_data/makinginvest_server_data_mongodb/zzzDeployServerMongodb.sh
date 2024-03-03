echo 'Deploying Mongodb'

rsync -avrmR --exclude='node*modules/' --include='.env' --exclude='.*' --include='\_/' ./ root@5.75.187.94:/root/makinginvest-mongodb --delete

ssh -t root@5.75.187.94 << ENDSSH
    cd makinginvest-mongodb/ && docker-compose up -d

    exit
ENDSSH
    echo 'Deployed Mongodb'