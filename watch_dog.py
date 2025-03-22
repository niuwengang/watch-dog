import time 
from pynvml  import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetMemoryInfo, nvmlShutdown 
import matplotlib.pyplot as plt
from matplotlib.animation  import FuncAnimation 
import psutil 
# 初始化NVML 
nvmlInit() 
handle = nvmlDeviceGetHandleByIndex(0) # 假设只有一个GPU，索引为0 
info = nvmlDeviceGetMemoryInfo(handle) 
max_memory_gpu = info.total / (1024 ** 3) # 总显存大小转换为GB，确保单位统一 
max_memory_ram = psutil.virtual_memory().total / (1024 ** 3) # 总物理内存大小转换为GB 
# 数据存储列表 
times = [] 
memory_used_gpu_data = [] 
memory_used_ram_data = [] 
fig, (ax_gpu, ax_ram) = plt.subplots(2, 1,constrained_layout=True) 
def update(frame): 
    # 绘制GPU内存 
    info = nvmlDeviceGetMemoryInfo(handle) 
    memory_used_gpu = info.used / (1024 ** 3) # 转换为GB，与max_memory单位保持一致 
    # 获取系统内存使用情况 
    memory_info = psutil.virtual_memory() 
    memory_used_ram = memory_info.used / (1024 ** 3) 
    current_time = time.time() 
    times.append(current_time) 
    memory_used_gpu_data.append(memory_used_gpu) 
    memory_used_ram_data.append(memory_used_ram) 
    if len(times) > 60: 
         times.pop(0) 
         memory_used_gpu_data.pop(0) 
         memory_used_ram_data.pop(0)

    ax_gpu.clear() 
    ax_gpu.plot([t - times[0] for t in times], memory_used_gpu_data, label='GPU Memory Used (GB)', color='blue') 
    ax_gpu.set_xlabel('Time (s)') 
    ax_gpu.set_ylabel('Memory Used (GB)') 
    ax_gpu.legend(loc='upper left') 
    ax_gpu.set_title('GPU Memory Usage Over Time') 
    ax_gpu.set_ylim(0, max_memory_gpu) 
    # ax_gpu.set_yticks(range(0, int(max_memory_gpu) + 1,int(max_memory_gpu/10))) 
    # 更新RAM内存图 
    ax_ram.clear() 
    ax_ram.plot([t - times[0] for t in times], memory_used_ram_data, label='RAM Used (GB)', color='green') 
    ax_ram.set_xlabel('Time (s)') 
    ax_ram.set_ylabel('Memory Used (GB)') 
    ax_ram.legend(loc='upper left') 
    ax_ram.set_title('RAM Usage Over Time') 
    ax_ram.set_ylim(0, max_memory_ram) 
    # ax_ram.set_yticks(range(0, int(max_memory_ram) + 1,int(max_memory_ram/10))) # 根据实际内存大小调整步长 
ani = FuncAnimation(fig, update, interval=1000) 
plt.tight_layout() 
plt.subplots_adjust(hspace=0.5) 
plt.subplots_adjust(left=0.15) 
plt.subplots_adjust(bottom=0.10) 
plt.show() 
nvmlShutdown() 