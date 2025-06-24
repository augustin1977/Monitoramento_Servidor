# main.py
from fastapi import FastAPI
import psutil
import shutil
import os

app = FastAPI()

def bytes_to_gb(value):
    return round(value / (1024 ** 3), 2)  # GB com 2 casas decimais

@app.get("/cpu")
def cpu_usage():
    return {"cpu_percent": psutil.cpu_percent(interval=1)}

@app.get("/memory")
def memory_info():
    mem = psutil.virtual_memory()
    return {"total": mem.total, "available": mem.available, "percent": mem.percent}

@app.get("/disk")
def disk_info():
    partitions = psutil.disk_partitions(all=False)
    disk_data = []
    for part in partitions:
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disk_data.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "total_gb": bytes_to_gb(usage.total),
                "used_gb": bytes_to_gb(usage.used),
                "free_gb": bytes_to_gb(usage.free),
                "percent_used": usage.percent
            })
        except PermissionError as e:
            disk_data.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "status": e
            })
            continue

    return disk_data

@app.get("/temperature")
def temperature():
    try:
        import subprocess
        output = subprocess.check_output("sensors", text=True)
        return {"sensors_output": output}
    except Exception as e:
        return {"error": str(e)}
    
    