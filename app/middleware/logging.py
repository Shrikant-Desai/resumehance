import time
import logging
from fastapi import Request

# configure the logger
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    # before request hits the route
    start_time = time.time()

    logger.info(f"Incoming Request: {request.method} {request.url}")

    # actually call the route handler
    response = await call_next(request)

    # after response comes back
    duration = time.time() - start_time
    logger.info(
        f"Completed: {request.method} {request.url} "
        f"| Status: {response.status_code} "
        f"| Duration: {duration:.3f}s"
    )

    return response
