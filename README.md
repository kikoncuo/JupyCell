# JupyCell 

**JupyCell**  is a secure API that connects applications to Jupyter Notebook kernels within sandboxed environments. Essential for Large Language Models (LLMs) executing code, it ensures safe and isolated code execution. Designed for extensibility and flexibility, JupyCell enables developers to collaborate seamlessly with LLMs, managing and running code cells efficiently and securely.

The name "JupyCell" is a playful blend of "Jupyter" and "Cell," capturing its core functionality. Additionally, it echoes the Spanish exclamation "¡Yupi!"—a joyful expression of happiness, reflecting the ease and delight JupyCell brings to your development experience.

## Table of Contents 
 
- [Features](#features)
 
- [Getting Started](#getting-started)  
  - [Using Docker](#using-docker)
 
  - [Developer Setup](#developer-setup)  
    - [Prerequisites](#prerequisites)
 
    - [Installation](#installation)
 
- [Usage](#usage)  
  - [Starting the Server](#starting-the-server)

  - [Starting the Server](#starting-the-server)
 
  - [API Endpoints](#api-endpoints)  
    - [Start a Kernel](#start-a-kernel)
 
    - [Manage Cells](#manage-cells)  
      - [Add a Cell](#add-a-cell)
 
      - [Edit a Cell](#edit-a-cell)
 
      - [Run a Cell](#run-a-cell)
 
      - [Run All Cells](#run-all-cells)
 
      - [Delete a Cell](#delete-a-cell)
 
    - [Retrieve Cell Outputs](#retrieve-cell-outputs)
 
- [Testing](#testing)  
  - [Running Tests](#running-tests)
 
- [Examples](#examples)  
  - [Adding and Running Cells](#adding-and-running-cells)
 
  - [Editing Cells and Running All Cells](#editing-cells-and-running-all-cells)
 
- [Contributing](#contributing)
 
- [License]()
 
- [Acknowledgements](#acknowledgements)

## Features 
 
- **Kernel Management** : Start and manage multiple Jupyter Notebook kernels via a simple RESTful API.
 
- **Cell Operations** : Add, edit, delete, and run individual cells, mimicking the interactive experience of Jupyter Notebooks.
 
- **Dependency Handling** : Maintain cell dependencies, ensuring that code execution respects the order and dependencies between cells.
 
- **Rich Output Support** : Capture and retrieve outputs from executed cells, including text, images, and more.
 
- **Asynchronous Operations** : Leverage asynchronous endpoints for efficient and scalable code execution.
 
- **Comprehensive Testing** : Ensure reliability with a robust test suite using `pytest` and FastAPI’s `TestClient`.

## Getting Started 

JupyCell offers flexible setup options to cater to both end-users and developers. Choose the method that best fits your needs.

### Using Docker 

Docker provides an easy and consistent way to deploy JupyCell without worrying about environment configurations.

#### Prerequisites 
 
- **Docker** : Ensure Docker is installed on your machine. Download it from [docker.com]() .

#### Installation 
 
1. **Clone the Repository** 

```bash
git clone https://github.com/yourusername/jupycell.git
cd jupycell
```
 
2. **Build the Docker Image** In the project directory, build the Docker image using the provided `Dockerfile`:

```bash
docker build -t jupycell .
```
 
  - **`-t jupycell`** : Tags the image with the name `jupycell`.
 
3. **Run the Docker Container** 
After successfully building the image, run the container:


```bash
docker run -d -p 8000:8000 --name jupycell_container jupycell
```
 
  - **`-d`** : Runs the container in detached mode.
 
  - **`-p 8000:8000`** : Maps port 8000 of the container to port 8000 on your host machine.
 
  - **`--name jupycell_container`** : Names the container `jupycell_container`.
 
  - **`jupycell`** : Specifies the image to run.
 
4. **Verify the Server is Running** Open your browser and navigate to `http://localhost:8000/docs` to access the interactive API documentation provided by FastAPI’s Swagger UI.

#### Stopping the Container 

To stop and remove the running container:


```bash
docker stop jupycell_container
docker rm jupycell_container
```

### Developer Setup 

For developers looking to contribute or customize JupyCell, follow the steps below to set up the development environment.

#### Prerequisites 
 
- **Python 3.9+** : Ensure you have Python installed. Download it from [python.org](https://www.python.org/downloads/) .
 
- **Git** : For cloning the repository. Download from [git-scm.com](https://git-scm.com/downloads)  if not already installed.

#### Installation 
 
1. **Clone the Repository** 

```bash
git clone https://github.com/yourusername/jupycell.git
cd jupycell
```
 
2. **Create a Virtual Environment** 
It's recommended to use a virtual environment to manage dependencies.


```bash
python3 -m venv venv
```
 
3. **Activate the Virtual Environment**  
  - **On macOS/Linux:** 

```bash
source venv/bin/activate
```
 
  - **On Windows (Command Prompt):** 

```bash
venv\Scripts\activate
```
 
  - **On Windows (PowerShell):** 

```bash
.\venv\Scripts\Activate.ps1
```
 
4. **Install Dependencies** 

```bash
pip install --upgrade pip
pip install -r requirements.txt
```
****Install Dependencies** 

```bash
pip install --upgrade pip
pip install -r requirements.txt
```
`requirements.txt`:** 

```plaintext
fastapi==0.95.2
uvicorn[standard]==0.22.0
jupyter_client==8.3.0
pydantic==1.10.9
pytest==7.2.0
ipykernel==6.20.0
```

## Usage 

### Starting the Server 

#### Adding dependencies for your kernel
If you want to add dependencies to your kernel, you can do so by adding a `requirements_app.txt` file in the root directory of the project. The `requirements_app.txt` file should contain the dependencies you want to install before compiling the docker container. When you start a new kernel, the dependencies will be installed automatically.

#### Using Docker 
If you followed the Docker setup, your server should already be running. If not, refer to the [Using Docker](#using-docker)  section.
#### Using Virtual Environment 

If you set up the developer environment:
 
1. **Ensure the Virtual Environment is Activated** 

```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```
 
2. **Run the FastAPI Application** 

```bash
uvicorn main:app --reload
```
 
  - **`main`** : Refers to the `main.py` file.
 
  - **`app`** : The FastAPI instance inside `main.py`.
 
  - **`--reload`** : Enables auto-reloading on code changes (useful during development).
 
3. **Access the API Documentation** Open your browser and navigate to `http://127.0.0.1:8000/docs` to explore the API endpoints using Swagger UI.

### API Endpoints 

#### Start a Kernel 
**Endpoint** : `POST /start`**Description** : Starts a new Jupyter Notebook kernel session.**Response** :

```json
{
  "kernel_id": 123456789
}
```

#### Manage Cells 

##### Add a Cell 
**Endpoint** : `POST /cell`**Description** : Adds a new cell to the kernel session.**Request Body** :

```json
{
  "kernel_id": 123456789,
  "cell_number": 1,
  "code": "x = 10",
  "action": "add"
}
```
**Response** :

```json
{
  "status": "Cell 1 added."
}
```

##### Edit a Cell 
**Endpoint** : `POST /cell`**Description** : Edits an existing cell's code.**Request Body** :

```json
{
  "kernel_id": 123456789,
  "cell_number": 1,
  "code": "x = 20",
  "action": "edit"
}
```
**Response** :

```json
{
  "status": "Cell 1 updated."
}
```

##### Run a Cell 
**Endpoint** : `POST /cell`**Description** : Executes a specific cell.**Request Body** :

```json
{
  "kernel_id": 123456789,
  "cell_number": 1,
  "action": "run"
}
```
**Response** :

```json
{
  "outputs": [
    {
      "name": "stdout",
      "text": "Hello, World!\n"
    }
  ]
}
```

##### Run All Cells 
**Endpoint** : `POST /cell`**Description** : Executes all cells in the kernel session in order.**Request Body** :

```json
{
  "kernel_id": 123456789,
  "action": "run_all"
}
```
**Response** :

```json
{
  "outputs": [
    {
      "cell_number": 1,
      "outputs": []
    },
    {
      "cell_number": 2,
      "outputs": []
    },
    {
      "cell_number": 3,
      "outputs": [
        {
          "name": "stdout",
          "text": "20\n"
        }
      ]
    }
  ]
}
```

##### Delete a Cell 
**Endpoint** : `POST /cell`**Description** : Deletes a specific cell from the kernel session.**Request Body** :

```json
{
  "kernel_id": 123456789,
  "cell_number": 1,
  "action": "delete"
}
```
**Response** :

```json
{
  "status": "Cell 1 deleted."
}
```

#### Retrieve Cell Outputs 
**Endpoint** : `GET /cell_outputs`**Description** : Retrieves the outputs of a specific cell.**Query Parameters** : 
- `kernel_id` (int): The ID of the kernel session.
 
- `cell_number` (int): The number of the cell.
**Example Request** :

```bash
curl -X GET "http://127.0.0.1:8000/cell_outputs?kernel_id=123456789&cell_number=3"
```
**Response** :

```json
{
  "outputs": [
    {
      "name": "stdout",
      "text": "20\n"
    }
  ]
}
```

## Testing 

JupyCell includes a comprehensive test suite to ensure reliability and correctness of its functionalities.

### Running Tests 
 
1. **Ensure Dependencies Are Installed** Make sure you have `pytest` installed:

```bash
pip install pytest
```
 
2. **Activate Your Virtual Environment** 

```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```
 
3. **Run the Tests** Execute the tests using `pytest`:

```bash
pytest test_main.py
```
**For Verbose Output:** 

```bash
pytest -v test_main.py
```

### Test Suite Overview 

For some reason tests fail inconsistently if ran at the same time, need to investigate further.

The test suite covers the following functionalities:
 
- **Kernel Management** :
  - Starting a new kernel.
 
- **Cell Operations** :
  - Adding a cell.

  - Editing a cell.

  - Running a cell.

  - Running all cells.

  - Deleting a cell.
 
- **Output Retrieval** :
  - Retrieving outputs from specific cells.
 
- **Error Handling** :
  - Attempting to run non-existent cells.
 
- **Complex Scenarios** :
  - Managing dependent cells and ensuring edits propagate correctly.


## Examples 

### Adding and Running Cells 
 
1. **Start a Kernel** 

```bash
KERNEL_ID=$(curl -s -X POST http://127.0.0.1:8000/start | jq -r '.kernel_id')
echo "Kernel ID: $KERNEL_ID"
```
 
2. **Add Cell 1** 

```bash
curl -s -X POST http://127.0.0.1:8000/cell \
     -H "Content-Type: application/json" \
     -d '{"kernel_id": '"$KERNEL_ID"', "cell_number": 1, "code": "x = 10", "action": "add"}' | jq
```
 
3. **Add Cell 2** 

```bash
curl -s -X POST http://127.0.0.1:8000/cell \
     -H "Content-Type: application/json" \
     -d '{"kernel_id": '"$KERNEL_ID"', "cell_number": 2, "code": "y = x * 2", "action": "add"}' | jq
```
 
4. **Add Cell 3** 

```bash
curl -s -X POST http://127.0.0.1:8000/cell \
     -H "Content-Type: application/json" \
     -d '{"kernel_id": '"$KERNEL_ID"', "cell_number": 3, "code": "print(y)", "action": "add"}' | jq
```
 
5. **Run All Cells** 

```bash
curl -s -X POST http://127.0.0.1:8000/cell \
     -H "Content-Type: application/json" \
     -d '{"kernel_id": '"$KERNEL_ID"', "action": "run_all"}' | jq
```
 
6. **Retrieve Output of Cell 3** 

```bash
curl -s -X GET "http://127.0.0.1:8000/cell_outputs?kernel_id=$KERNEL_ID&cell_number=3" | jq
```
**Expected Output** :

```json
{
  "outputs": [
    {
      "name": "stdout",
      "text": "20\n"
    }
  ]
}
```

### Editing Cells and Running All Cells 
 
1. **Edit Cell 2** 

```bash
curl -s -X POST http://127.0.0.1:8000/cell \
     -H "Content-Type: application/json" \
     -d '{"kernel_id": '"$KERNEL_ID"', "cell_number": 2, "code": "y = x * 3", "action": "edit"}' | jq
```
 
2. **Run All Cells Again** 

```bash
curl -s -X POST http://127.0.0.1:8000/cell \
     -H "Content-Type: application/json" \
     -d '{"kernel_id": '"$KERNEL_ID"', "action": "run_all"}' | jq
```
 
3. **Retrieve Updated Output of Cell 3** 

```bash
curl -s -X GET "http://127.0.0.1:8000/cell_outputs?kernel_id=$KERNEL_ID&cell_number=3" | jq
```
**Expected Output** :

```json
{
  "outputs": [
    {
      "name": "stdout",
      "text": "15\n"
    }
  ]
}
```

## Contributing 

Contributions are welcome! Whether it's improving documentation, reporting bugs, or adding new features, your help is appreciated.
 
1. **Fork the Repository** 
Click the "Fork" button at the top-right corner of the repository page.
 
2. **Clone Your Fork** 

```bash
git clone https://github.com/yourusername/jupycell.git
cd jupycell
```
 
3. **Create a New Branch** 

```bash
git checkout -b feature/YourFeatureName
```
 
4. **Make Your Changes** 
Implement your feature or fix the bug.
 
5. **Commit Your Changes** 

```bash
git commit -m "Add feature: YourFeatureName"
```
 
6. **Push to Your Fork** 

```bash
git push origin feature/YourFeatureName
```
 
7. **Open a Pull Request** 
Go to the original repository and click "New pull request." Provide a clear description of your changes.

## License 
This project is licensed under the MIT License.
## Acknowledgements 
 
- **[FastAPI]() ** : A modern, fast (high-performance) web framework for building APIs with Python.
 
- **[Uvicorn](https://www.uvicorn.org/) ** : A lightning-fast ASGI server for Python.
 
- **[Jupyter Client](https://jupyter-client.readthedocs.io/en/stable/) ** : A package providing APIs for managing Jupyter kernels.
 
- **[Pytest](https://pytest.org/) ** : A mature full-featured Python testing tool.


---


Feel free to reach out or contribute if you have suggestions or improvements! Let's make coding joyful with JupyCell!