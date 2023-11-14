echo 'Deploying Server Main'

rsync -avrmR \
    --delete-excluded \
    --exclude='__venv/*' \
    --exclude='__pycache__/*' \
    --include='.env' \
    --exclude='.\*' \
    --include='_/' \
    ./ root@5.78.84.141:/root/makinginvest-python-engines-main

ssh root@5.78.84.141 << EOF
    cd makinginvest-python-engines-main/ && docker-compose up -d --build makinginvest-python-engines-main
EOF

echo 'Deployed Server Main'

# this drives the running engines in all
