echo 'Deploying Server Main'

rsync -avrmR \
    --delete-excluded \
    --exclude='_project/data/*' \
    --exclude='__venv/*' \
    --exclude='__pycache__/*' \
    --include='.env' \
    --exclude='.\*' \
    --include='_/' \
    ./ root@188.34.177.82:/root/makinginvest-python-engines-driver

ssh root@188.34.177.82 << EOF
    cd makinginvest-python-engines-driver/ && docker-compose up -d --build makinginvest-python-engines-driver
EOF

echo 'Deployed Server Main'

# this drives the running engines in all
