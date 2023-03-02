from api.main import app
import uvicorn

# from backend.app.sql_app.utils_scripts.create_tables import create_tables

# create_tables()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
