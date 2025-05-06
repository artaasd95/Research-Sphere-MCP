import subprocess
import sys
import os
import time
from pathlib import Path

def run_backend():
    """Run the FastAPI backend server"""
    backend_dir = Path("backend")
    os.chdir(backend_dir)
    
    # Create and activate virtual environment
    if not os.path.exists("venv"):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    # Activate virtual environment
    if sys.platform == "win32":
        python = "venv\\Scripts\\python"
        pip = "venv\\Scripts\\pip"
    else:
        python = "venv/bin/python"
        pip = "venv/bin/pip"
    
    # Install dependencies
    print("Installing backend dependencies...")
    subprocess.run([pip, "install", "-r", "requirements.txt"], check=True)
    
    # Run backend server
    print("Starting backend server...")
    backend_process = subprocess.Popen(
        [python, "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000"]
    )
    
    return backend_process

def run_frontend():
    """Run the React frontend development server"""
    frontend_dir = Path("frontend")
    os.chdir(frontend_dir)
    
    # Install dependencies
    print("Installing frontend dependencies...")
    subprocess.run(["npm", "install"], check=True)
    
    # Run frontend server
    print("Starting frontend server...")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"]
    )
    
    return frontend_process

def main():
    """Main function to run both servers"""
    try:
        # Start backend
        os.chdir(Path(__file__).parent)
        backend_process = run_backend()
        
        # Wait a bit for backend to start
        time.sleep(2)
        
        # Start frontend
        os.chdir(Path(__file__).parent)
        frontend_process = run_frontend()
        
        print("\nMCP RAG System is running!")
        print("Backend: http://localhost:8000")
        print("Frontend: http://localhost:3000")
        print("\nPress Ctrl+C to stop both servers...")
        
        # Wait for processes to complete
        backend_process.wait()
        frontend_process.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 