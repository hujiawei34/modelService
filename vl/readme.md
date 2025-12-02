

[toc]

# 需求

想要在本地PC部署一个图片识别模型，可以识别验证码图片中的文字

本机配置

nvidia 5060 blackwell架构，win10+wsl2,驱动已装，cuda 版本13.0，smi信息如下：

```bash
(pt_cu130) root@DESKTOP-H75TK46:~/code# nvidia-smi
Tue Dec  2 10:47:18 2025       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.82.02              Driver Version: 581.15         CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5060        On  |   00000000:01:00.0  On |                  N/A |
|  0%   33C    P8             12W /  145W |     817MiB /   8151MiB |      1%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A              26      G   /Xwayland                             N/A      |
|    0   N/A  N/A              35      G   /Xwayland                             N/A      |
|    0   N/A  N/A              46      G   /Xwayland                             N/A      |
+-----------------------------------------------------------------------------------------+
```

# 操作步骤

## wsl中安装cuda

根据官网中的操作安装 

[CUDA Toolkit 13.0 Update 2 Downloads | NVIDIA Developer](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_local)



```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/13.0.2/local_installers/cuda-repo-wsl-ubuntu-13-0-local_13.0.2-1_amd64.deb
sudo dpkg -i cuda-repo-wsl-ubuntu-13-0-local_13.0.2-1_amd64.deb
sudo cp /var/cuda-repo-wsl-ubuntu-13-0-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda-toolkit-13-0
```

检测安装成功

```bash
(pt_cu130) root@DESKTOP-H75TK46:~# nvcc -V
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2025 NVIDIA Corporation
Built on Wed_Aug_20_01:58:59_PM_PDT_2025
Cuda compilation tools, release 13.0, V13.0.88
Build cuda_13.0.r13.0/compiler.36424714_0
```



## 安装pytorch



创建VENV

```bash
python -m venv /root/venvs/pt_cu130
. /root/venvs/pt_cu130/bin/activate

```

使用nighty 的pytorch 适配SM130，也可以使用12.8的正式版

```bash
pip install --pre torch torchvision torchaudio  --index-url https://download.pytorch.org/whl/nightly/cu130
```

检测安装成功

```bash
(pt_cu130) root@DESKTOP-H75TK46:~# python - <<'PY'
import torch, torch.backends.cudnn as cudnn
print("PyTorch:", torch.__version__)
print("CUDA runtime:", torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())
print("cuDNN:", cudnn.version())
print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None")
PY

```

以下是输出 

```bash
#我这个是后来安装2.9的pytorch，也可以使用
PyTorch: 2.9.0+cu128
CUDA runtime: 12.8
CUDA available: True
cuDNN: 91002
GPU: NVIDIA GeForce RTX 5060
```

pip list见[附录](#pip list)







# 附录

## pip list

```bash
Package                           Version
--------------------------------- -----------------
aiohappyeyeballs                  2.6.1
aiohttp                           3.13.2
aiosignal                         1.4.0
annotated-doc                     0.0.4
annotated-types                   0.7.0
anthropic                         0.71.0
anyio                             4.12.0
apache-tvm-ffi                    0.1.4
astor                             0.8.1
async-timeout                     5.0.1
attrs                             25.4.0
av                                16.0.1
blake3                            1.0.8
cachetools                        6.2.2
cbor2                             5.7.1
certifi                           2025.11.12
charset-normalizer                3.4.4
click                             8.2.1
cloudpickle                       3.1.2
coloredlogs                       15.0.1
compressed-tensors                0.12.2
ctranslate2                       4.6.1
cuda-bindings                     13.0.3
cuda-pathfinder                   1.2.2
cuda-python                       13.0.3
cupy-cuda12x                      13.6.0
depyf                             0.20.0
dill                              0.4.0
diskcache                         5.6.3
distro                            1.9.0
dnspython                         2.8.0
docstring_parser                  0.17.0
einops                            0.8.1
email-validator                   2.3.0
exceptiongroup                    1.3.1
fastapi                           0.123.0
fastapi-cli                       0.0.16
fastapi-cloud-cli                 0.5.2
fastar                            0.8.0
faster-whisper                    1.2.1
fastrlock                         0.8.3
filelock                          3.20.0
flashinfer-python                 0.5.2
flatbuffers                       25.9.23
frozenlist                        1.8.0
fsspec                            2025.10.0
gguf                              0.17.1
h11                               0.16.0
hf-xet                            1.2.0
httpcore                          1.0.9
httptools                         0.7.1
httpx                             0.28.1
huggingface-hub                   0.36.0
humanfriendly                     10.0
idna                              3.11
interegular                       0.3.3
Jinja2                            3.1.6
jiter                             0.12.0
jmespath                          1.0.1
jsonschema                        4.25.1
jsonschema-specifications         2025.9.1
lark                              1.2.2
llguidance                        1.3.0
llvmlite                          0.44.0
lm-format-enforcer                0.11.3
loguru                            0.7.3
markdown-it-py                    4.0.0
MarkupSafe                        3.0.2
mdurl                             0.1.2
mistral_common                    1.8.6
model-hosting-container-standards 0.1.9
mpmath                            1.3.0
msgpack                           1.1.2
msgspec                           0.20.0
multidict                         6.7.0
networkx                          3.4.2
ninja                             1.13.0
numba                             0.61.2
numpy                             2.1.2
nvidia-cublas                     13.1.0.3
nvidia-cublas-cu12                12.8.4.1
nvidia-cuda-cupti                 13.0.85
nvidia-cuda-cupti-cu12            12.8.90
nvidia-cuda-nvrtc                 13.0.88
nvidia-cuda-nvrtc-cu12            12.8.93
nvidia-cuda-runtime               13.0.96
nvidia-cuda-runtime-cu12          12.8.90
nvidia-cudnn-cu12                 9.10.2.21
nvidia-cudnn-cu13                 9.13.0.50
nvidia-cudnn-frontend             1.16.0
nvidia-cufft                      12.0.0.61
nvidia-cufft-cu12                 11.3.3.83
nvidia-cufile                     1.15.1.6
nvidia-cufile-cu12                1.13.1.3
nvidia-curand                     10.4.0.35
nvidia-curand-cu12                10.3.9.90
nvidia-cusolver                   12.0.4.66
nvidia-cusolver-cu12              11.7.3.90
nvidia-cusparse                   12.6.3.3
nvidia-cusparse-cu12              12.5.8.93
nvidia-cusparselt-cu12            0.7.1
nvidia-cusparselt-cu13            0.8.0
nvidia-cutlass-dsl                4.3.1
nvidia-ml-py                      13.580.82
nvidia-nccl-cu12                  2.27.5
nvidia-nccl-cu13                  2.27.7
nvidia-nvjitlink                  13.0.88
nvidia-nvjitlink-cu12             12.8.93
nvidia-nvshmem-cu12               3.3.20
nvidia-nvshmem-cu13               3.4.5
nvidia-nvtx                       13.0.85
nvidia-nvtx-cu12                  12.8.90
onnxruntime                       1.23.2
openai                            2.8.1
openai-harmony                    0.0.8
opencv-python-headless            4.12.0.88
outlines_core                     0.2.11
packaging                         25.0
partial-json-parser               0.2.1.1.post7
pillow                            12.0.0
pip                               25.3
prometheus_client                 0.23.1
prometheus-fastapi-instrumentator 7.1.0
propcache                         0.4.1
protobuf                          6.33.1
psutil                            7.1.3
py-cpuinfo                        9.0.0
pybase64                          1.4.2
pycountry                         24.6.1
pydantic                          2.12.5
pydantic_core                     2.41.5
pydantic-extra-types              2.10.6
Pygments                          2.19.2
python-dotenv                     1.2.1
python-json-logger                4.0.0
python-multipart                  0.0.20
pytorch-triton                    3.5.1+gitbfeb0668
PyYAML                            6.0.3
pyzmq                             27.1.0
ray                               2.52.1
referencing                       0.37.0
regex                             2025.11.3
requests                          2.32.5
rich                              14.2.0
rich-toolkit                      0.17.0
rignore                           0.7.6
rpds-py                           0.30.0
safetensors                       0.7.0
scipy                             1.15.3
sentencepiece                     0.2.1
sentry-sdk                        2.46.0
setproctitle                      1.3.7
setuptools                        59.6.0
shellingham                       1.5.4
sniffio                           1.3.1
starlette                         0.50.0
supervisor                        4.3.0
sympy                             1.14.0
tabulate                          0.9.0
tiktoken                          0.12.0
tokenizers                        0.22.1
tomli                             2.3.0
torch                             2.9.0
torchaudio                        2.9.0
torchvision                       0.24.0
tqdm                              4.67.1
transformers                      4.57.3
triton                            3.5.0
typer                             0.20.0
typer-slim                        0.20.0
typing_extensions                 4.15.0
typing-inspection                 0.4.2
urllib3                           2.5.0
uvicorn                           0.38.0
uvloop                            0.22.1
vllm                              0.11.2
watchfiles                        1.1.1
websockets                        15.0.1
xformers                          0.0.33.post1
xgrammar                          0.1.25
yarl                              1.22.0
yt-dlp                            2025.11.12
```



