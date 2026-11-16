import json
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()
DATA_FILE = Path("employees.json")


class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    salary: int = Field(..., gt=0)


def read_employees() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_employees(employees: list[dict]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(employees, f, indent=2)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/employees")
def get_all_employees():
    return read_employees()


@app.get("/employees/{name}")
def get_employee_by_name(name: str):
    for emp in read_employees():
        if emp["name"].lower() == name.lower():
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")


@app.post("/employees", status_code=201)
def add_employee(emp: EmployeeCreate):
    if not emp.name.strip():
        raise HTTPException(status_code=422, detail="Name cannot be empty")
    employees = read_employees()
    new_emp = emp.model_dump()
    employees.append(new_emp)
    save_employees(employees)
    return new_emp
