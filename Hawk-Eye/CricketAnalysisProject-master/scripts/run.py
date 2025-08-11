import os
import sys
import subprocess
import time
import signal
import psutil
from dotenv import load_dotenv

def check_ports():
    """Check if required ports are available"""
    ports = [5000, 3000]  # Backend and frontend ports
    for port in ports:
        for conn in psutil.net_connections():
            if conn.laddr.port == port:
                print(f"❌ Port {port} is already in use")
                return False
    return True

def start_backend():
    """Start the Flask backend server"""
    print("Starting backend server...")
    os.chdir("backend")
    python_path = r"C:\Users\Hammad\AppData\Local\Programs\Python\Python313\python.exe"
    backend = subprocess.Popen(
        [python_path, "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True
    )
    os.chdir("..")
    return backend

def start_frontend():
    """Start the React frontend development server"""
    print("Starting frontend server...")
    os.chdir("frontend")
    frontend = subprocess.Popen(
        "npm start",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True
    )
    os.chdir("..")
    return frontend

def monitor_processes(backend, frontend):
    """Monitor the backend and frontend processes"""
    try:
        while True:
            # Check if processes are still running
            if backend.poll() is not None:
                print("Backend server stopped unexpectedly")
                break
            if frontend.poll() is not None:
                print("Frontend server stopped unexpectedly")
                break
            
            # Print any output from the processes
            backend_output = backend.stdout.readline()
            if backend_output:
                print(f"Backend: {backend_output.strip()}")
            
            frontend_output = frontend.stdout.readline()
            if frontend_output:
                print(f"Frontend: {frontend_output.strip()}")
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()
        print("Servers stopped")

def main():
    # Load environment variables
    load_dotenv()
    
    # Check if ports are available
    if not check_ports():
        print("Please free up the required ports and try again")
        sys.exit(1)
    
    # Check if required directories exist
    if not os.path.exists("backend") or not os.path.exists("frontend"):
        print("❌ Required directories not found")
        print("Please run this script from the project root directory")
        sys.exit(1)
    
    # Check if node_modules exists
    if not os.path.exists("frontend/node_modules"):
        print("Installing frontend dependencies...")
        os.chdir("frontend")
        subprocess.run("npm install", shell=True, check=True)
        os.chdir("..")
    
    # Start the servers
    backend = start_backend()
    frontend = start_frontend()
    
    # Monitor the processes
    monitor_processes(backend, frontend)

if __name__ == "__main__":
    main() 