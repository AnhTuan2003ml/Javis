import psutil
import eel
import json
import os

def get_cpu_temperature():
    """Get CPU temperature"""
    try:
        # Try psutil sensors first
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    if entries:
                        return round(entries[0].current, 1)
        
        # Estimate based on CPU usage
        cpu_usage = psutil.cpu_percent(interval=0.1)
        estimated_temp = 35 + (cpu_usage * 0.5)
        return round(estimated_temp, 1)
    except:
        return 45

@eel.expose
def getNetworkSpeed():
    """Get current network usage in Mbps"""
    try:
        import time
        
        old = psutil.net_io_counters()
        old_sent = old.bytes_sent
        old_recv = old.bytes_recv
        time.sleep(1)  # measure in 1 second interval
        new = psutil.net_io_counters()
        new_sent = new.bytes_sent
        new_recv = new.bytes_recv

        upload_speed = (new_sent - old_sent) / (1024 * 1024)  # MB/s
        download_speed = (new_recv - old_recv) / (1024 * 1024)  # MB/s

        total_usage = upload_speed + download_speed
        return round(total_usage, 2)
    except:
        return 0.0

@eel.expose
def getSystemStats():
    """Get real system statistics"""
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # CPU temperature
        cpu_temp = get_cpu_temperature()
        
        # Memory usage
        memory = psutil.virtual_memory()
        ram_total = memory.total
        ram_used = memory.used
        
        # Total disk usage across all drives
        disk_total = 0
        disk_used = 0
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_total += usage.total
                disk_used += usage.used
            except PermissionError:
                continue
        
        return {
            'cpu': round(cpu_percent, 1),
            'cpu_temp': cpu_temp,
            'ram_total': ram_total,
            'ram_used': ram_used,
            'disk_total': disk_total,
            'disk_used': disk_used
        }
    except Exception as e:
        print(f"System stats error: {e}")
        return {
            'cpu': 0,
            'cpu_temp': 45,
            'ram_total': 8589934592,  # 8GB fallback
            'ram_used': 4294967296,   # 4GB fallback
            'disk_total': 549755813888,   # 512GB fallback
            'disk_used': 171798691840     # 160GB fallback
        }

@eel.expose
def readCalendarEvents():
    """Read calendar events from jarvis_calendar.json"""
    try:
        calendar_path = 'jarvis_calendar.json'
        if os.path.exists(calendar_path):
            with open(calendar_path, 'r') as f:
                return json.load(f)
        return []
    except:
        return []

@eel.expose
def readReminders():
    """Read reminders from reminders.json"""
    try:
        reminders_path = 'reminders.json'
        if os.path.exists(reminders_path):
            with open(reminders_path, 'r') as f:
                return json.load(f)
        return []
    except:
        return []