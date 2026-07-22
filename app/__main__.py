import uvicorn

from app import app, config

if config.environment.is_production():
    uvicorn.run(app, host="0.0.0.0", port=8080, log_config=None, access_log=False)
else:
    uvicorn.run("app:app", port=8080, reload=True, log_config=None, access_log=False)
