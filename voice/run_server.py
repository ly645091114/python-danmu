# run_server.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.server:app",
        host="0.0.0.0",
        port=9522,
        reload=True,  # 开发时热重载
    )