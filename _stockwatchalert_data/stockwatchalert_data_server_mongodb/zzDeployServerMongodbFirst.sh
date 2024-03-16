echo 'Deploying Mongodb'

rsync -avrmR --exclude='node*modules/' --include='.env' --exclude='.*' --include='\_/' ./ root@5.75.187.94:/root/makinginvest-mongodb --delete

ssh -t root@5.75.187.94 << 'ENDSSH'
    cd makinginvest-mongodb/ && docker-compose up -d
    sleep 5

    docker exec -it makinginvest-mongodb bash -c '
    echo "
    mongosh --port 27027 --eval \"

    sleep 5
    use admin

    sleep 5
    db.createUser({
    user: 'adminmakinginvest',
    pwd: 'QKYeqqwwq44390Z4e234fsd82B6s3G1makinginvest',
    roles: ['root', 'userAdminAnyDatabase', 'dbAdminAnyDatabase', 'readWriteAnyDatabase']
    });\"
    "
    '
ENDSSH
echo 'Deployed Mongodb'
