import uvicorn
import sys


APP_IMPORT_STRING="app.main:app"
HOST="0.0.0.0"
PORT=5000

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "dev":
            import os
            cwd = os.path.join(os.getcwd(), "app")
            uvicorn.run(
                APP_IMPORT_STRING,
                host=HOST,
                port=PORT,
                log_level="debug",
                reload=True,
                reload_dirs=[cwd]
            )
        elif sys.argv[1] == "prod":
            uvicorn.run(
                APP_IMPORT_STRING,
                host=HOST,
                port=PORT,
                log_level="info"
            )
    else:
        print("Needs args to run")

if __name__=="__main__":
    main()
