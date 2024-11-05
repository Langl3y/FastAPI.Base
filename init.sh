#!/bin/bash

pip install -r requirements.txt
cp .env.sample .env
python -c "from api.common.utils import create_database; create_database()"