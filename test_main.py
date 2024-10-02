# test_main.py

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def kernel_id():
    # Start a new kernel and return its ID
    response = client.post("/start")
    assert response.status_code == 200
    data = response.json()
    return data["kernel_id"]

def test_start_kernel():
    response = client.post("/start")
    assert response.status_code == 200
    data = response.json()
    assert "kernel_id" in data

def test_add_cell(kernel_id):
    # Add a new cell
    response = client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 1,
        "code": "x = 10",
        "action": "add"
    })
    print(response)
    data = response.json()
    assert data["status"] == "Cell 1 added."

def test_edit_cell(kernel_id):
    # Add a cell first
    client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 1,
        "code": "x = 10",
        "action": "add"
    })

    # Edit the cell
    response = client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 1,
        "code": "x = 20",
        "action": "edit"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Cell 1 updated."

def test_run_cell(kernel_id):
    # Add a cell
    client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 1,
        "code": "x = 10",
        "action": "add"
    })

    # Run the cell
    response = client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 1,
        "action": "run"
    })
    assert response.status_code == 200
    data = response.json()
    assert "outputs" in data
    # Check outputs (should be empty since x = 10 doesn't produce output)
    assert len(data["outputs"]) == 0

def test_run_all_cells(kernel_id):
    # Add multiple cells
    client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 1,
        "code": "x = 10",
        "action": "add"
    })
    client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 2,
        "code": "y = x * 2",
        "action": "add"
    })
    client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 3,
        "code": "print(y)",
        "action": "add"
    })

    # Run all cells
    response = client.post("/cell", json={
        "kernel_id": kernel_id,
        "action": "run_all"
    })
    assert response.status_code == 200
    data = response.json()
    assert "outputs" in data
    assert len(data["outputs"]) == 3

    # Check the output of the last cell
    last_cell_output = data["outputs"][2]["outputs"]
    assert len(last_cell_output) > 0
    output = last_cell_output[0]
    assert output["name"] == "stdout"
    assert output["text"].strip() == "20"

def test_get_cell_outputs(kernel_id):
    # Add and run a cell
    client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 1,
        "code": "print('Hello, World!')",
        "action": "add"
    })
    client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 1,
        "action": "run"
    })

    # Get outputs
    response = client.get("/cell_outputs", params={
        "kernel_id": kernel_id,
        "cell_number": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert "outputs" in data
    assert len(data["outputs"]) > 0
    output = data["outputs"][0]
    assert output["name"] == "stdout"
    assert output["text"].strip() == "Hello, World!"

def test_delete_cell(kernel_id):
    # Add a cell
    client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 1,
        "code": "x = 10",
        "action": "add"
    })

    # Delete the cell
    response = client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 1,
        "action": "delete"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Cell 1 deleted."

    # Try to get outputs of deleted cell
    response = client.get("/cell_outputs", params={
        "kernel_id": kernel_id,
        "cell_number": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == "Cell number does not exist."

def test_multiline_code_execution(kernel_id):
    code = '''def greet(name):
    return f"Hello, {name}!"

print(greet("Tester"))'''

    # Add a cell with multiline code
    response = client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 1,
        "code": code,
        "action": "add"
    })
    assert response.status_code == 200

    # Run the cell
    response = client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 1,
        "action": "run"
    })
    assert response.status_code == 200
    data = response.json()
    outputs = data.get("outputs", [])
    assert len(outputs) > 0
    output = outputs[0]
    assert output["name"] == "stdout"
    assert output["text"].strip() == "Hello, Tester!"

def test_run_nonexistent_cell(kernel_id):
    response = client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 99,
        "action": "run"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["error"] == "Cell number does not exist."

def test_edit_functionality(kernel_id):
    # Add three cells
    client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 1,
        "code": "a = 5",
        "action": "add"
    })
    client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 2,
        "code": "b = a * 2",
        "action": "add"
    })
    client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 3,
        "code": "print(b)",
        "action": "add"
    })

    # Run all cells
    response = client.post("/cell", json={
        "kernel_id": kernel_id,
        "action": "run_all"
    })
    assert response.status_code == 200
    data = response.json()

    # Check output before edit
    outputs = data["outputs"]
    last_cell_output = outputs[2]["outputs"]
    assert len(last_cell_output) > 0
    output = last_cell_output[0]
    assert output["name"] == "stdout"
    assert output["text"].strip() == "10"

    # Edit the second cell
    client.post("/cell", json={
        "kernel_id": kernel_id,
        "cell_number": 2,
        "code": "b = a * 3",
        "action": "edit"
    })

    # Run all cells again
    response = client.post("/cell", json={
        "kernel_id": kernel_id,
        "action": "run_all"
    })
    assert response.status_code == 200
    data = response.json()

    # Check output after edit
    outputs = data["outputs"]
    last_cell_output = outputs[2]["outputs"]
    assert len(last_cell_output) > 0
    output = last_cell_output[0]
    assert output["name"] == "stdout"
    assert output["text"].strip() == "15"
