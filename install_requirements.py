import os
import subprocess
import sys
import re

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.stdout.decode('utf-8'), e.stderr.decode('utf-8')

def install_conda_packages():
    print("正在安装 SimpleITK...")
    stdout, stderr = run_command("conda install -c simpleitk simpleitk -y")
    if stderr:
        print("安装 SimpleITK 时出错：", stderr)
    else:
        print("SimpleITK 安装完成。")

def install_pip_packages():
    packages = ["hydra-core", "nibabel", "omegaconf", "einops", "matplotlib", "lightning", "tensorboard", "wandb"]
    for package in packages:
        print(f"正在安装 {package}...")
        stdout, stderr = run_command(f"pip install {package}")
        if stderr:
            print(f"安装 {package} 时出错：", stderr)
        else:
            print(f"{package} 安装完成。")

def get_cuda_version():
    stdout, stderr = run_command("nvcc --version")
    if stderr:
        print("无法获取 CUDA 版本：", stderr)
        return None
    cuda_version_match = re.search(r"V(\d+\.\d+)", stdout)
    if cuda_version_match:
        return cuda_version_match.group(1)
    else:
        print("无法解析 CUDA 版本。")
        return None

def get_torch_version(cuda_version):
    torch_cuda_map = {
        "11.1": "torch==1.9.0+cu111",
        "11.3": "torch==1.10.0+cu113",
        "11.6": "torch==1.12.0+cu116",
        # 根据需要补充其他版本映射
    }
    return torch_cuda_map.get(cuda_version)

def install_torch(cuda_version):
    torch_version = get_torch_version(cuda_version)
    if torch_version:
        print(f"正在安装适合 CUDA {cuda_version} 的 PyTorch: {torch_version}...")
        stdout, stderr = run_command(f"pip install {torch_version} torchvision torchaudio -f https://download.pytorch.org/whl/torch_stable.html")
        if stderr:
            print("安装 PyTorch 时出错：", stderr)
        else:
            print("PyTorch 安装完成。")
    else:
        print(f"未找到适合 CUDA {cuda_version} 的 PyTorch 版本。")

def check_anaconda():
    stdout, stderr = run_command("conda --version")
    if stderr:
        print("未检测到 Anaconda。")
        user_input = input("是否安装 Anaconda?(y/n): ").strip().lower()
        if user_input == 'y':
            print("请访问 https://www.anaconda.com/products/individual 下载并安装 Anaconda。")
        else:
            print("未安装 Anaconda, 脚本将退出。")
        sys.exit()
    else:
        print("已检测到 Anaconda。")

def main():
    print("开始安装依赖...")
    check_anaconda()
    install_conda_packages()
    install_pip_packages()
    cuda_version = get_cuda_version()
    if cuda_version:
        install_torch(cuda_version)
    else:
        print("未检测到 CUDA, 跳过 PyTorch 安装。")
    print("所有操作完成。")

if __name__ == "__main__":
    main()