import torch
print(torch.cuda.is_available())  # Harusnya hasilnya "True"
print(torch.cuda.get_device_name(0))  # Harusnya keluar nama RTX 4060

