import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import re

def load_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    data = np.loadtxt(file_path)
    valid_mask = data[:, 0] != 0
    timestamps = data[valid_mask, 0]
    values = data[valid_mask, 1]
    if len(timestamps) == 0:
        raise ValueError("文件中无有效数据（时间戳全为0）")
    return timestamps, values

def main():
    # 修改数据目录为/file
    data_dir = './file'
    
    input_pattern = re.compile(r'inputData_(\d+)_(\d+)\.txt')
    response_pattern = re.compile(r'responseData_(\d+)_(\d+)\.txt')
    
    input_files = {}
    response_files = {}
    
    for file in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file)
        input_match = input_pattern.search(file)
        if input_match:
            index = int(input_match.group(1))
            motor_id = int(input_match.group(2))
            input_files[(index, motor_id)] = file_path
        
        response_match = response_pattern.search(file)
        if response_match:
            index = int(response_match.group(1))
            motor_id = int(response_match.group(2))
            response_files[(index, motor_id)] = file_path
    
    # 指定电机组合
    motor_groups = [
        {12, 19}, {13, 20}, {14, 21}, {15, 22},
        {16, 23}, {17, 24}, {18, 25}, {0, 6},
        {1, 7}, {2, 8}, {3, 9}, {4, 10}, {5, 11}
    ]
    
    # 按组合绘制图片
    for group_idx, group in enumerate(motor_groups):
        # 创建一个大图，包含组合中的所有电机图
        fig, axes = plt.subplots(len(group), 1, figsize=(12, 6 * len(group)))
        if len(group) == 1:
            axes = [axes]  # 确保axes始终是列表
        
        # 记录该组中成功绘制的电机数量
        plotted_count = 0
        
        for motor_id in sorted(group):
            # 查找该电机的所有索引
            motor_indices = set()
            for (idx, mid) in input_files.keys():
                if mid == motor_id:
                    motor_indices.add(idx)
            for (idx, mid) in response_files.keys():
                if mid == motor_id:
                    motor_indices.add(idx)
            
            if not motor_indices:
                print(f"警告: Motor {motor_id} 无数据，跳过")
                continue
            
            # 选择第一个找到的索引
            index = min(motor_indices)
            key = (index, motor_id)
            
            input_file = input_files.get(key)
            response_file = response_files.get(key)
            
            if not input_file or not response_file:
                print(f"警告: Motor {motor_id} 文件不完整，跳过")
                continue
            
            try:
                input_ts, input_val = load_data(input_file)
                resp_ts, resp_val = load_data(response_file)
                
                # 在大图中对应位置绘制子图
                ax = axes[plotted_count]
                ax.plot(input_ts, input_val, 'b-', label='Input')
                ax.plot(resp_ts, resp_val, 'r--', label='Response')
                ax.set_title(f'Motor {motor_id}')
                ax.set_xlabel('Time (ms)' if input_ts.dtype == np.int64 else 'Time (s)')
                ax.set_ylabel('Signal Value')
                ax.grid(True)
                ax.legend()
                
                print(f"成功绘制: 第 {index} 组 Motor {motor_id}，数据点数量: {len(input_ts)}")
                plotted_count += 1
                
            except Exception as e:
                print(f"处理 Motor {motor_id} 时出错: {e}")
        
        # 如果该组有成功绘制的电机，保存大图
        if plotted_count > 0:
            # 调整子图布局
            plt.tight_layout()
            os.makedirs('./grouped_images', exist_ok=True)
            plt.savefig(f'./grouped_images/group_{group_idx}.png')
            plt.close()
            print(f"已保存第 {group_idx} 组图片，包含 {plotted_count} 个电机")

if __name__ == "__main__":
    main()
