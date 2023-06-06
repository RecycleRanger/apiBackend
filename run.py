import uvicorn
import sys


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "dev":
            import os
            cwd = os.path.join(os.getcwd(), "app")
            uvicorn.run("app.main:app", host="127.0.0.1", port=5000, log_level="debug", reload=True, reload_dirs=[cwd])
        elif sys.argv[1] == "prod":
            uvicorn.run("app.main:app", host="127.0.0.1", port=5000, log_level="info")
    else:
        print("Needs args to run")

if __name__=="__main__":
    main()
