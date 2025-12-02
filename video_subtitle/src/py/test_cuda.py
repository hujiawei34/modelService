
import torch, torch.backends.cudnn as cudnn
print("PyTorch:", torch.__version__)
print("CUDA runtime:", torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())
print("cuDNN:", cudnn.version())
print("GPU:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None")