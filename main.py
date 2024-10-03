from fastapi import FastAPI
from pydantic import BaseModel
from jupyter_client import KernelManager
import asyncio
from typing import Optional

app = FastAPI()
kernels = {}

class CodeExecutionRequest(BaseModel):
    kernel_id: int
    cell_number: Optional[int] = None
    code: Optional[str] = None
    action: str  # 'add', 'edit', 'run', 'delete', 'run_all'

@app.post("/start")
async def start_kernel():
    km = KernelManager()
    await asyncio.to_thread(km.start_kernel)
    kc = km.client()
    await asyncio.to_thread(kc.start_channels)
    kernel_id = id(kc)
    kernels[kernel_id] = {'client': kc, 'cells': {}}
    return {"kernel_id": kernel_id}

@app.post("/cell")
async def cell_operations(request: CodeExecutionRequest):
    kernel_data = kernels.get(request.kernel_id)
    if not kernel_data:
        return {"error": "Kernel not found"}

    cells = kernel_data['cells']
    kc = kernel_data['client']
    action = request.action.lower()

    if action in ('add', 'edit'):
        if request.cell_number is None or request.code is None:
            return {"error": "cell_number and code are required for add/edit actions."}

        if action == 'add':
            if request.cell_number in cells:
                return {"error": "Cell number already exists. Use 'edit' to modify it."}
            cells[request.cell_number] = {'code': request.code, 'outputs': []}
            return {"status": f"Cell {request.cell_number} added."}

        elif action == 'edit':
            if request.cell_number not in cells:
                return {"error": "Cell number does not exist. Use 'add' to create it."}
            cells[request.cell_number]['code'] = request.code
            cells[request.cell_number]['outputs'] = []  # Reset outputs
            return {"status": f"Cell {request.cell_number} updated."}

    elif action == 'run':
        if request.cell_number is None:
            return {"error": "cell_number is required for run action."}
        if request.cell_number not in cells:
            return {"error": "Cell number does not exist."}
        return await run_cell(kc, cells, request.cell_number)

    elif action == 'run_all':
        return await run_all_cells(kc, cells)

    elif action == 'delete':
        if request.cell_number is None:
            return {"error": "cell_number is required for delete action."}
        if request.cell_number not in cells:
            return {"error": "Cell number does not exist."}
        del cells[request.cell_number]
        return {"status": f"Cell {request.cell_number} deleted."}

    else:
        return {"error": "Invalid action. Use 'add', 'edit', 'run', 'delete', or 'run_all'."}

async def run_cell(kc, cells, cell_number):
    code = cells[cell_number]['code']

    # Ensure the kernel is ready by waiting for its "idle" state
    while True:
        try:
            msg = await asyncio.to_thread(kc.get_iopub_msg, timeout=1)
            if msg['header']['msg_type'] == 'status' and msg['content']['execution_state'] == 'idle':
                break  # The kernel is ready
        except Exception:
            break
    
    # Execute the cell code 
    msg_id = await asyncio.to_thread(kc.execute, code)
    outputs = []

    while True:
        try:
            msg = await asyncio.to_thread(kc.get_iopub_msg, timeout=30)
            msg_type = msg['header']['msg_type']

            if msg_type == 'status':
                if msg['content']['execution_state'] == 'idle':
                    break  # Execution is complete
            elif msg_type in ('execute_result', 'display_data', 'stream', 'error'):
                outputs.append(msg['content'])
        except Exception:
            break

    cells[cell_number]['outputs'] = outputs
    return {"outputs": outputs}

async def run_all_cells(kc, cells):
    sorted_cells = sorted(cells.items())
    all_outputs = []
    for cell_number, cell_data in sorted_cells:
        result = await run_cell(kc, cells, cell_number)
        all_outputs.append({'cell_number': cell_number, 'outputs': result['outputs']})
    return {"outputs": all_outputs}

@app.get("/cell_outputs")
async def get_cell_outputs(kernel_id: int, cell_number: int):
    kernel_data = kernels.get(kernel_id)
    if not kernel_data:
        return {"error": "Kernel not found"}
    cells = kernel_data['cells']
    if cell_number not in cells:
        return {"error": "Cell number does not exist."}
    return {"outputs": cells[cell_number]['outputs']}
