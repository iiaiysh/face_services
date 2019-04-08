#!/bin/bash
source deactivate
conda activate face_services
CUDA_VISIBLE_DEVICES=0 gunicorn --bind=0.0.0.0:8001 --workers=1 json_server:app
