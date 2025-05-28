from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import get_db_connection

app = FastAPI()

# Khởi tạo Jinja2 để render template HTML
templates = Jinja2Templates(directory="templates")

# Route để render trang chính
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route để xử lý tìm kiếm
@app.get("/search")
async def search_students(query: str = ""):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if query.strip() == "":
        # Nếu không có từ khóa, trả về toàn bộ bảng
        query_sql = "SELECT * FROM Students"
        cursor.execute(query_sql)
    else:
        # Tìm kiếm theo ma_sv, ten, hoặc dia_chi
        query_sql = """
            SELECT * FROM Students 
            WHERE ma_sv LIKE %s OR ten LIKE %s OR dia_chi LIKE %s
        """
        cursor.execute(query_sql, (f"%{query}%", f"%{query}%", f"%{query}%"))
    
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return students