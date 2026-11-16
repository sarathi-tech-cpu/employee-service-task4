import json
from fastapi.testclient import TestClient
from src.main import app
import src.main as main_module

client = TestClient(app)


def setup_function(func):
    temp_file = main_module.Path("test_employees.json")
    sample = [{"name": "Arun", "department": "Sales", "salary": 30000}]
    temp_file.write_text(json.dumps(sample), encoding="utf-8")
    main_module.DATA_FILE = temp_file


def teardown_function(func):
    temp_file = main_module.Path("test_employees.json")
    if temp_file.exists():
        temp_file.unlink()


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_list_employees():
    res = client.get("/employees")
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_get_employee_success():
    res = client.get("/employees/Arun")
    assert res.status_code == 200
    assert res.json()["name"] == "Arun"


def test_get_employee_not_found():
    res = client.get("/employees/Ravi")
    assert res.status_code == 404


def test_create_employee_invalid_salary():
    res = client.post(
        "/employees", json={"name": "Karthik", "department": "IT", "salary": -5}
    )
    assert res.status_code == 422


def test_create_employee_empty_name():
    res = client.post(
        "/employees", json={"name": "", "department": "IT", "salary": 40000}
    )
    assert res.status_code == 422


def test_create_employee_success():
    res = client.post(
        "/employees", json={"name": "Meena", "department": "HR", "salary": 45000}
    )
    assert res.status_code == 201
    assert res.json()["name"] == "Meena"
