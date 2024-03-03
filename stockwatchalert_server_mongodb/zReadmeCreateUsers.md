ssh root@154.38.166.122

docker exec -it signalbyt-mongodb-client bash

mongosh --username="adminsignalbytclient" --password="QKYeqqwwq44390Z4e234fsd82B6s3G1signalbytclient"

use admin

<!-- ---------------------------- CREATE USERS ----------------------------- -->

db.createUser(
{
user: 'admincodememoryllc-prod',
pwd: 'QKYN90Z4e82B6s3G1RDcodememoryllc-prod',
roles: ["root","userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]
}
)

db.createUser(
{
user: 'doadmincodememoryllc-prod',
pwd: 'doQKYN90Z4e82B6s3G1RDcodememoryllc-prod',
roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]
}
)

<!-- ------------------------------ DROP USER ------------------------------ -->

db.dropUser("doadminsignalbytclient")

<!-- --------------------------- RESTART SERVER ---------------------------- -->

db.shutdownServer()

db.createUser({
user: 'doadminsignalbytclient',
pwd: 'doQKYeqqwwq44390Z4e234fsd82B6s3G1signalbytclient',
roles: ['userAdminAnyDatabase', 'dbAdminAnyDatabase', 'readWriteAnyDatabase']
});
