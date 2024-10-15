import time
import requests
import json

class JupyCellClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.kernel_id = None

    def start_kernel(self):
        response = requests.post(f"{self.base_url}/start")
        if response.status_code == 200:
            self.kernel_id = response.json().get('kernel_id')
            print(f"Kernel started with ID: {self.kernel_id}")
        else:
            print(f"Failed to start kernel. Status code: {response.status_code}")

    def add_cell(self, cell_number, code):
        payload = {
            "kernel_id": self.kernel_id,
            "cell_number": cell_number,
            "code": code,
            "action": "add"
        }
        response = requests.post(f"{self.base_url}/cell", json=payload)
        if response.status_code == 200:
            print(f"Cell {cell_number} added successfully.")
        else:
            print(f"Failed to add cell. Status code: {response.status_code}")

    def run_all_cells(self):
        payload = {
            "kernel_id": self.kernel_id,
            "action": "run_all"
        }
        response = requests.post(f"{self.base_url}/cell", json=payload)
        if response.status_code == 200:
            print("All cells ran successfully.")
            return response.json()
        else:
            print(f"Failed to run all cells. Status code: {response.status_code}")
            return None

    def run_cell(self, cell_number):
        payload = {
            "kernel_id": self.kernel_id,
            "cell_number": cell_number,
            "action": "run"
        }
        response = requests.post(f"{self.base_url}/cell", json=payload)
        if response.status_code == 200:
            print(f"Cell {cell_number} ran successfully.")
            return response.json()
        else:
            print(f"Failed to run cell. Status code: {response.status_code}")
            return None

    def get_cell_output(self, cell_number):
        params = {
            "kernel_id": self.kernel_id,
            "cell_number": cell_number
        }
        response = requests.get(f"{self.base_url}/cell_outputs", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve cell output. Status code: {response.status_code}")
            return None

# Main code to test
if __name__ == "__main__":
    # Initialize JupyCell client
    client = JupyCellClient(base_url="http://localhost:8000")

    # Start a new kernel
    kernel = client.start_kernel()
    print(kernel)

    # Add the code to create a graph using pandas and matplotlib
    graph_code = '''
x=5
    '''
    add = client.add_cell(1, graph_code)
    print(add)

    # Run the cell to generate and display the graph
    run = client.run_cell(1)
    print(run)


    #time.sleep(10)  # Wait a bit before retrying to handle delays
    #getCellOutput = client.get_cell_output(1)
    #print(getCellOutput)
