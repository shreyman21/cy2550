#!/bin/bash

GREEN='\033[0;32m'

# Build the application and run it 
python3 manage.py makemigrations
python3 manage.py migrate 
echo -e "${GREEN}The application is running locally on 127.0.0.1:8000${NC}"
python3 manage.py runserver