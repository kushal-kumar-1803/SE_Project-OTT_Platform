import psutil
import datetime

class InstanceService:
    start_time = datetime.datetime.now()

    @staticmethod
    def get_instance_status():
        uptime = datetime.datetime.now() - InstanceService.start_time
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()

        return {
            "status": "running",
            "uptime": str(uptime),
            "cpu_usage": f"{cpu_usage}%",
            "memory_usage": f"{memory.percent}%"
        }
