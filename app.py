mport sqlite3, os from datetime import datetime、timedelta from pathlib import Path from fastapi 
导入 FastAPI、Request、HTTPException 来自 fastapi.middleware.跨域导入 CORSMiddleware 
从 pydantic 导入 BaseModel，导入 uvicorn
BASE_DIR = Path(file).parent DB_PATH = BASE_DIR / "records.db" JST = timedelta(hours=9) 
AUTH_TOKEN = os.environ.get("AUTH_TOKEN",“lyy010234xmjim”)
def init_db(): conn = sqlite3.connect(str(DB_PATH)) conn.execute("""CREATE TABLE IF NOT 
EXISTS records ( id INTEGER PRIMARY KEY AUTOINCREMENT, app_name TEXT NOT 
NULL, event TEXT NOT NULL, timestamp TEXT NOT NULL)""") conn.commit(); conn.close() 
init_db()
app = FastAPI(title="查岗系统") app.add_middleware(CORSMiddleware, allow_origins=[""], 
allow_methods=[""], allow_headers=["*"])
class ReportBody(BaseModel): app_name: str event: str
@app.post("/report") async def report(body: ReportBody, req: Request): auth = 
f"Bearer AUTH_TOKEN}": 抛出 
 当前时间 = datetime.utcnow().isoformat() 连接 = 
sqlite3.connect(str(DB_PATH)) conn.execute("INSERT INTO records VALUES (?, ?, ?)", 
(body.app_name, body.event, now)) conn.commit(); conn.close() return {"status": "ok"}
@app.get("/ping") async def ping(): return "pong"
@app.get("/activity/summary") async def summary(): conn = sqlite3.connect(str(DB_PATH)) cur =
conn.cursor() cur.execute("SELECT app_name, event, timestamp FROM records ORDER BY id 
DESC LIMIT 5") recent = cur.fetchall() cur.execute("SELECT app_name, event, timestamp FROM
records ORDER BY id ASC") rows = cur.fetchall() conn.close() sessions, opens = {}, {} for r in 
rows: app, ev, ts = r if ev == "open": opens[app] = datetime.fromisoformat(ts) elif ev == "close" 
并且在 opens 中的 app：gap = int((datetime.fromisoformat(ts) - opens[app]).total_seconds()) 
sessions[app] = sessions.get(app, 0) + gap del opens[app] return { "recent_apps": [r[0] for r in 
最近], "sessions": sessions }
if name == "main": port = int(os.environ.get("PORT", 8000)) uvicorn.run(app, host="0.0.0.0", 
端口=端口)
