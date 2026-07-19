import uvicorn

from app import app, config

if config.environment.is_production():
    uvicorn.run(
        app, host="0.0.0.0", port=config.port, log_config=None, access_log=False
    )
else:
    uvicorn.run(
        "app:app", port=config.port, reload=True, log_config=None, access_log=False
    )
