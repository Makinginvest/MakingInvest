echo 'Deploying Mongodb'

rsync -avrmR --exclude='node*modules/' --include='.env' --exclude='.*' --include='\_/' ./ root@128.140.60.95:/root/signalbyt-mongodb-client --delete

ssh -t root@128.140.60.95 << ENDSSH
    cd signalbyt-mongodb-client/ && docker-compose up -d

    exit
ENDSSH
    echo 'Deployed Mongodb'
