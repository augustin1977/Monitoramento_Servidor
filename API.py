# main.py
from fastapi import FastAPI,Depends
import psutil
import shutil
import os
from AUTH import validate_token
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina uma lista segura
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def bytes_to_gb(value):
    return round(value / (1024 ** 3), 2)  # GB com 2 casas decimais

@app.get("/cpu", dependencies=[Depends(validate_token)])
def cpu_usage():
    usage_per_core = psutil.cpu_percent(interval=0.5,percpu=True)
    return [{"core": f"Core {i}", "usage_percent": usage} for i, usage in enumerate(usage_per_core)]

@app.get("/memory", dependencies=[Depends(validate_token)])
def memory_info():
    mem = psutil.virtual_memory()
    return {
        "total_gb": bytes_to_gb(mem.total),
        "available_gb": bytes_to_gb(mem.available),
        "used_gb": bytes_to_gb(mem.used),
        "free_gb": bytes_to_gb(mem.free),
        "percent_used": mem.percent}

@app.get("/disk", dependencies=[Depends(validate_token)])
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

@app.get("/temperature", dependencies=[Depends(validate_token)])
def temperature():
    try:
        import subprocess
        output = subprocess.check_output("sensors", text=True)
        return {"sensors_output": output}
    except Exception as e:
        return {"error": str(e)}
    
    