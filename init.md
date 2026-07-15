
# install minicanda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# init fish
source ~/.config/fish/config.fish
~/miniconda3/bin/conda init fish
# change channels
conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.bfsu.edu.cn/anaconda/cloud/conda-forge/
conda config --set show_channel_urls yes
# accept
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
# create env
conda create -n econ_rag python=3.10 -y
conda activate econ_rag


# 安装ollama
sudo pacman -S ollama
sudo systemctl enable --now ollama
systemctl status ollama

```bash
sudo mkdir -p /etc/systemd/system/ollama.service.d/
sudo nano /etc/systemd/system/ollama.service.d/override.conf


[Service]
# 修改模型存储路径（默认在 /usr/share/ollama/.ollama/models）
Environment="OLLAMA_MODELS=/mnt/data/ollama_models"

# 允许局域网、本地开发服务（如本地 RAG、Agent 容器）跨域访问
Environment="OLLAMA_HOST=0.0.0.0"
Environment="OLLAMA_ORIGINS=*"
```
sudo mkdir -p /mnt/data/ollama_models
sudo chown -R ollama:ollama /mnt/data/ollama_models
sudo chmod +x /mnt/data

sudo systemctl daemon-reload
sudo systemctl restart ollama

#安装conda



# 下载模型
pip install modelscope
从国内源高速下载 Qwen2.5-7B 的 GGUF 文件：

Bash
# 下载指定的 GGUF 文件到本地
modelscope download --model qwen/Qwen2.5-7B-Instruct-GGUF --include qwen2.5-7b-instruct-q4_k_m.gguf --local_dir .
写一个 Modelfile 文件告诉 Ollama 怎么读它：
在你下载好的目录下新建一个名为 Modelfile 的文件：

Dockerfile
FROM ./qwen2.5-7b-instruct-q4_k_m.gguf
使用 Ollama 导入并创建模型：

Bash
ollama create my-qwen2.5:7b -f ./Modelfile
导入成功后，直接运行即可（秒开，不需要再联网下载）：
















