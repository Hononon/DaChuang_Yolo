# DaChuang_Yolo
# 1.显卡配置 
## 1.Nidia显卡驱动及Cuda安装
1. Nidia驱动版本：470.82.00（可使用GeforceExperience安装最新版本） 
2. Cuda版本：11.4 下载链接：https://developer.nvidia.cn/cuda-11-4-0-download-archive? 
3. Cudnn版本：8.2.4 下载链接：https://developer.nvidia.cn/rdp/cudnn-archive 
## 2.Anaconda配置 
1. 安装anaconda Anaconda版本：Anaconda3-2021.05 安装时添加到环境变量 下载链接：https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/ 
2. Anaconda配置 ####1.创建虚拟环境 conda create -n pytorch python=3.8 
2. 激活虚拟环境 conda activate pytorch 
3. 添加镜像源 conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/ conda config --set show_channel_urls yes

## 3. pytorch安装
conda install pytorch torchvision torchaudio cudatoolkit=11.4
