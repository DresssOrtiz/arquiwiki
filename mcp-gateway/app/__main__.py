import logging

import uvicorn

from app.server import build_from_env

logging.basicConfig(level=logging.INFO)
uvicorn.run(build_from_env(), host="0.0.0.0", port=8002, log_level="info")
