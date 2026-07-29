导入 sqlite3, os
从 datetime 导入 datetime、timedelta
从 pathlib 导入 Path
从 fastapi 导入 FastAPI、Request、HTTPException
从 fastapi.middleware.cors 导入 CORSMiddleware
从 pydantic 导入 BaseModel
导入 uvicorn

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "records.db"
AUTH_TOKEN = os.environ.get("AUTH_TOKEN", "lyy010234xmjim")

定义 初始化数据库():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app_name TEXT NOT NULL,
        事件 TEXT NOT NULL,
        timestamp TEXT NOT NULL
        )""")
    conn.commit()
    conn.close()

init_db()

app = FastAPI(title="查岗系统")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

类 报告正文(BaseModel):
    app_name: str
    event: str

@app.post("/report")
async def report(body: ReportBody, req: Request):
    auth = req.headers.get("Authorization", "")
    如果认证不等于 “Bearer 
        raise HTTPException(401, "未授权")
    
    now = datetime.utcnow().isoformat()
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("INSERT INTO records (app_name, event, timestamp) VALUES (?, ?, ?)",
                 (body.app_name, body.event, now))
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.get("/ping")
async def ping():
    return "pong"

@app.get("/activity/summary")
async def summary():
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()
    cur.execute("SELECT app_name, event, timestamp FROM records ORDER BY id DESC LIMIT 5")
    recent = cur.fetchall()
    cur.execute("SELECT app_name, event, timestamp FROM records ORDER BY id ASC")
    rows = cur.fetchall()
    conn.close()
    
    sessions, opens = {}, {}
    for r in rows:
        app_name, ev, ts = r
        if ev == "open":
            打开[app_name] = datetime.fromisoformat(ts)
        elif ev == "close" and app_name in opens:
            gap = int((datetime.fromisoformat(ts) - opens[app_name]).total_seconds())
            sessions[app_name] = sessions.get(app_name, 0) + gap
            del opens[app_name]
    
    返回 { "最近的应用": [r[0] 对于 r 在最近], "会话": 会话}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
