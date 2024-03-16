echo 'Deploying Server data'

rsync -avrmR --delete-excluded --exclude='__venv/*' --exclude='__pycache__/*' --include='.env' --exclude='.\*' --include='_/' ./ root@49.13.84.137:/root/stockwatchalert-python-data

ssh root@49.13.84.137 << EOF
    cd stockwatchalert-python-data/ && docker-compose up -d --build stockwatchalert-python-data
EOF

echo 'Deployed Server data'
