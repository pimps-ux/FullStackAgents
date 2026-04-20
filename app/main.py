from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.pipeline import run_pipeline
from app.storage import JsonStorage

app = FastAPI(title=settings.app_name, version=settings.version)
templates = Jinja2Templates(directory="templates")
storage = JsonStorage()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/pipeline/run")
def pipeline_run() -> dict:
    result, contacts, companies = run_pipeline()
    wh = storage.load()
    wh["contacts"] = [c.model_dump() for c in contacts]
    wh["companies"] = [c.model_dump() for c in companies]
    wh["runs"].append(result.model_dump(mode="json"))
    storage.save(wh)
    return {
        "message": "Pipeline executado com sucesso.",
        "result": result.model_dump(mode="json"),
    }


@app.get("/api/dashboard")
def dashboard_data() -> dict:
    wh = storage.load()
    latest = wh["runs"][-1] if wh["runs"] else {}
    return {
        "kpis": latest,
        "totals": {
            "contacts": len(wh["contacts"]),
            "companies": len(wh["companies"]),
        },
        "consent_rate": round(
            (sum(1 for c in wh["contacts"] if c.get("consent_any_source")) / len(wh["contacts"]) * 100), 2
        )
        if wh["contacts"]
        else 0,
    }


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request, "app_name": settings.app_name})
