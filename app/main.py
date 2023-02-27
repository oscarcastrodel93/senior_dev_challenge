__author__  = "Oscar Castro"
__email__   = "omcastro93@gmail.com"
__version__ = "1.0"


from sqlalchemy.orm import Session
import starlette.status as status

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

from .database.db import SessionLocal, engine
from .database import crud, models
from . import schemas
from .helpers import validate_save, check_officer
from .auth.auth_handler import signJWT
from .auth.auth_bearer import JWTBearer

models.Base.metadata.create_all(engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#############
# API section

@app.post("/login")
async def officer_login(officer: schemas.OfficerLogin, db: Session = Depends(get_db)):
    """
    API to login a officer with a specified identification_number

    TODO: add password to officer
    """
    
    if check_officer(db, officer):
        return signJWT(officer.identification_number)
    return {
        "error": "Datos incorrectos!"
    }


@app.post("/cargar_infraccion", status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
async def create_fine(fine: schemas.FineCreate, db: Session = Depends(get_db)):
    """
    API to create a fine with specified payload.

    TODO: add relationship between fine and officer
    """
    
    db_vehicle = crud.get_record_by_field(
        db, model_name="vehicles", field="licence_plate", value=fine.placa_patente
    )
    if not db_vehicle:
        raise HTTPException(status_code=404, detail="Esta placa/patente no existe.")
    
    fine_data = {
        "comments": fine.comentarios,
        "date_created": fine.timestamp,
        "vehicle_id": db_vehicle.id
    }
    crud.create_record(db=db, model_name="fines", data=fine_data)
    return {"status": "ok"}


@app.get("/generar_informe", response_model=list[schemas.FineList])
async def list_fines(db: Session = Depends(get_db), email: str = None):
    """
    API to list available fines by email
    """
    if not email:
        raise HTTPException(status_code=400, detail="Parametro requerido: email")
    
    fines = crud.list_fines(db, email)
    if not fines:
        raise HTTPException(status_code=404, detail="No se encontraron registros")
    
    return fines

###############
# admin section

@app.get("/admin", response_class=HTMLResponse, include_in_schema=False)
async def admin(request: Request):
    """
    Renders index admin page
    """
    return templates.TemplateResponse("admin.html", {"request": request})


@app.get("/admin/{module}", response_class=HTMLResponse, include_in_schema=False)
async def list_records(request: Request, module: str, db: Session = Depends(get_db)):
    """
    Renders page to list all records by given module name (plural)
    """
    records = crud.list_records(db, model_name=module)
    try:
        return templates.TemplateResponse(f"list_{module}.html", {
            "request": request, "records": records
        })
    except:
        raise HTTPException(status_code=404, detail="Pagina no encontrada.")


@app.get("/admin/{module}/create", response_class=HTMLResponse, include_in_schema=False)
@app.get("/admin/{module}/{record_id}/edit/", response_class=HTMLResponse, include_in_schema=False)
async def form_save_record(request: Request, module: str, record_id: int | None = None, db: Session = Depends(get_db)):
    """
    Renders form to create or update a record, given a module name (plural)
    When module it's vehicles, injects people data to populate owner select field.
    """
    params = {}
    record = {}
    if module == "vehicles":
        params["people"] = crud.list_records(db, model_name="people")

    if record_id:
        record = crud.get_record(db, model_name=module, record_id=record_id)

    return templates.TemplateResponse(f"create_{module}.html", {
        "request": request, "params": params, "record": record
    })


@app.post("/admin/{module}/create", response_class=HTMLResponse, include_in_schema=False)
@app.post("/admin/{module}/{record_id}/edit/", response_class=HTMLResponse, include_in_schema=False)
async def save_record(request: Request, module: str, record_id: int | None = None, db: Session = Depends(get_db)):
    """
    Receives post form to create or update a record, given a module name (plural) and record_id (if updating)
    """
    form_data = await request.form()
    form_data = jsonable_encoder(form_data)

    validate_save(db, module, form_data, record_id)
    
    if record_id:
        crud.update_record(db, model_name=module, data=form_data, record_id=record_id)
    else:
        crud.create_record(db, model_name=module, data=form_data)

    return RedirectResponse(f"/admin/{module}", status_code=status.HTTP_302_FOUND)


@app.get("/admin/{module}/{record_id}/delete", response_class=HTMLResponse, include_in_schema=False)
async def delete_record(request: Request, module: str, record_id:int, db: Session = Depends(get_db)):
    """
    Deletes a record given a module name (plural) and record_id
    """
    crud.delete_record(db, model_name=module, record_id=record_id)
    return RedirectResponse(f"/admin/{module}", status_code=status.HTTP_302_FOUND)
