import torch
from huggingface_hub import HfApi
# import kagglehub

# kagglehub.login()
# # Download latest version
# path1 = kagglehub.model_download("mohammed237/trocr_finetune_weights_stp/pyTorch/default")
# path2 = kagglehub.model_download("mohammed237/yolo-weights-word-detection/pyTorch/default")

# print("Path to model files:", path1)
# print("Path to model files:", path2)


# Upload the file
api = HfApi()
api.upload_file(
    path_or_fileobj="model_weights.pth",
    path_in_repo="TROCR_model/model.pth",
    repo_id="haneenakram/trocr_finetune_weights_stp",
    repo_type="model"
)
api = HfApi()
api.upload_file(
    path_or_fileobj="worddetection.pt",
    path_in_repo="model/yolo_model.pth",
    repo_id="haneenakram/trocr_finetune_weights_stp",
    repo_type="model"
)