#!/usr/bin/env sh

set -e

STREAMLIT_PORT="${PORT:-8080}"

exec streamlit run app.py \
    --server.port "${STREAMLIT_PORT}" \
    --server.address 0.0.0.0
