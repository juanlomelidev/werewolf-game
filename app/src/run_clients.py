import subprocess
import os
import time

def main():
    # Define el directorio donde están ubicados los scripts
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Cambia al directorio del script
    os.chdir(script_dir)
    
    # Ejecuta el client.py ocho veces
    client_processes = []
    for i in range(8):
        print(f"Starting client.py instance {i+1}...")
        client_process = subprocess.Popen(['python', 'client.py'])
        client_processes.append(client_process)
        time.sleep(1)  # Espera 1 segundo entre la ejecución de cada cliente

    # Espera a que todos los procesos de cliente terminen
    for client_process in client_processes:
        client_process.wait()

if __name__ == "__main__":
    main()
