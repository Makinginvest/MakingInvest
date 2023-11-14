echo 'Deploying Server Engines'

rsync -avrmR \
    --delete-excluded \
    --exclude='__venv/*' \
    --exclude='__pycache__/*' \
    --include='.env' \
    --exclude='.\*' \
    --include='_/' \
    ./ root@5.78.84.141:/root/makinginvest-python-engines-all

ssh root@5.78.84.141 << EOF
    cd makinginvest-python-engines-all/ && docker-compose up -d --build makinginvest-python-engines-all
EOF

echo 'Deployed Server Engines'
