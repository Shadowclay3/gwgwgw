from flask import Flask, request, jsonify
import psutil, json

app = Flask(__name__)

api_key = "hf7fhf87qhw3d93dj92Klsq09iqdmpq893DM"

import psutil

def get_system_info():
    # Информация о памяти
    memory = psutil.virtual_memory()
    total_memory = round(memory.total / (1024 ** 3))  # Общий объем оперативной памяти в гигабайтах
    used_memory = round(memory.used / (1024 ** 3))    # Использовано оперативной памяти в гигабайтах
    percent_memory = round(memory.percent)           # Загрузка оперативной памяти в процентах

    memory_info = {
        "total Gb": total_memory,
        "used Gb": used_memory,
        "percent %": percent_memory,
    }

    # Информация о дисках
    disk_partitions = psutil.disk_partitions()
    disk_info = []
    for partition in disk_partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        total_disk = round(usage.total / (1024 ** 3))  # Общий объем диска в гигабайтах
        used_disk = round(usage.used / (1024 ** 3))    # Использовано дискового пространства в гигабайтах
        percent_disk = round(usage.percent)           # Загрузка диска в процентах

        disk_info.append({
            "device": partition.device,
            "total Gb": total_disk,
            "used Gb": used_disk,
            "percent %": percent_disk,
        })

    # Информация о процессоре
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    total_cpu_percent = round(sum(cpu_percent) / len(cpu_percent))  # Общая загрузка процессора в процентах

    cpu_info = {
        "total %": total_cpu_percent,
        "cores %": [round(core) for core in cpu_percent],
    }

    return {
        "memory": memory_info,
        "disks": disk_info,
        "cpu": cpu_info,
    }

@app.route('/', methods=['POST'])
def server():
    try:
        # Получаем JSON-данные из тела запроса
        data = request.get_json()
        # Проверяем, что данные были успешно получены
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400
        if data['api_key'] == api_key:
            return jsonify({"status": "succes", "data": get_system_info()}), 200
        else:
            return jsonify({"error": "Invalid api-key"}), 400
    except Exception as e: 
        if data['api_key'] == api_key: return jsonify({"status": "error", "error": f"Unknown error: {e}"}), 400
        else: return jsonify({})

if __name__ == '__main__':
    app.run(host='192.168.0.107', port=8082)
