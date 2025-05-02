#import torch
from huggingface_hub import HfApi
# import kagglehub
from huggingface_hub import login

#login("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")

# kagglehub.login()
# # Download latest version
# path1 = kagglehub.model_download("mohammed237/trocr_finetune_weights_stp/pyTorch/default")
# path2 = kagglehub.model_download("mohammed237/yolo-weights-word-detection/pyTorch/default")

# print("Path to model files:", path1)
# print("Path to model files:", path2)


api = HfApi()


# Upload model1
api.upload_folder(
    folder_path="GroundTruthmedicinebart-ocr-correction",
    path_in_repo="medicinembart",
    repo_id="haneenakram/trocr_finetune_weights_stp",
    repo_type="model"
)

# Upload model2
api.upload_folder(
    folder_path="GroundTruthAppointbart-ocr-correction",
    path_in_repo="Appointmbart",
    repo_id="haneenakram/trocr_finetune_weights_stp",
    repo_type="model"
)

# Upload model3
api.upload_folder(
    folder_path="mbart-ocr-correction",
    path_in_repo="mbart",
    repo_id="haneenakram/trocr_finetune_weights_stp",
    repo_type="model"
)
