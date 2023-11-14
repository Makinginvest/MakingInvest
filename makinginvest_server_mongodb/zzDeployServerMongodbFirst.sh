echo 'Deploying Mongodb'

rsync -avrmR --exclude='node*modules/' --include='.env' --exclude='.*' --include='\_/' ./ root@128.140.60.95:/root/signalbyt-mongodb-client --delete

ssh -t root@128.140.60.95<< ENDSSH
    cd signalbyt-mongodb-client/ && docker-compose up -d

    script /dev/null

    docker exec -it signalbyt-mongodb-client bash

    mongosh --port 27026

    use admin

    db.createUser({
    user: 'adminsignalbytclient',
    pwd: 'QKYeqqwwq44390Z4e234fsd82B6s3G1signalbytclient',
    roles: ['root', 'userAdminAnyDatabase', 'dbAdminAnyDatabase', 'readWriteAnyDatabase']
    });

    exit
ENDSSH
    echo 'Deployed Mongodb'
