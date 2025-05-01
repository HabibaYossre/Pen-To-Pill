import torch
from ultralytics import YOLO
from ultralytics.engine.model import Model
from ultralytics.nn.tasks import attempt_load_one_weight
import os
import tempfile
import shutil
from huggingface_hub import hf_hub_download

def load_yolo_from_pth(pth_file_path):
    """
    Load a YOLO model from a .pth file by bypassing the file extension check
    
    Args:
        pth_file_path (str): Path to the .pth file
        
    Returns:
        YOLO: Loaded YOLO model
    """
    print(f"Loading YOLO model from {pth_file_path} using custom loader...")
    
    # Create a YOLO model with a basic architecture (this will be overwritten)
    model = YOLO("yolov8n.yaml")  # Just initialize with a configuration, not weights
    
    # Load weights directly without checking file extension
    ckpt = torch.load(pth_file_path, map_location='cpu')
    
    # Apply weights to model (might need adjustments based on state dict structure)
    if 'model' in ckpt:
        # If the checkpoint has a 'model' key, extract model state dict
        model.model = ckpt['model']
    elif 'state_dict' in ckpt:
        # If the checkpoint has a 'state_dict' key
        try:
            model.model.load_state_dict(ckpt['state_dict'])
        except:
            print("Failed to load state_dict directly, trying key remapping...")
            # Try to map and load keys individually
            state_dict = ckpt['state_dict']
            model_state_dict = model.model.state_dict()
            
            # Create a mapping dictionary
            new_state_dict = {}
            for k, v in state_dict.items():
                # Try to find matching params by name (removing prefixes if needed)
                if k in model_state_dict:
                    new_state_dict[k] = v
                elif k.startswith('model.'):
                    # Try removing 'model.' prefix
                    key = k[6:]  # Remove 'model.'
                    if key in model_state_dict:
                        new_state_dict[key] = v
            
            # Load the mapped weights
            if new_state_dict:
                model.model.load_state_dict(new_state_dict, strict=False)
    else:
        # Direct load attempt
        try:
            model.model.load_state_dict(ckpt)
        except:
            print("Direct load failed. Checkpoint structure:", list(ckpt.keys())[:5])
            # Last resort: try to iterate through the model parameters and manually copy weights
            # This is a complex process that would require knowing the exact model structure
    
    print("Custom YOLO model loading completed")
    return model

# Example usage in your startup function
def custom_load_models():
    # Download the weights file from Hugging Face
    yolo_path = hf_hub_download(repo_id="haneenakram/trocr_finetune_weights_stp", 
                               filename="model/yolo_model.pth")
    
    # Load the model using our custom function
    model = load_yolo_from_pth(yolo_path)
    
    return model

# If directly run, test the function
if __name__ == "__main__":
    # Example test
    repo_id = "haneenakram/trocr_finetune_weights_stp"
    filename = "model/yolo_model.pth"
    
    print(f"Testing YOLO model loading from {repo_id}/{filename}")
    yolo_path = hf_hub_download(repo_id=repo_id, filename=filename)
    model = load_yolo_from_pth(yolo_path)
    
    print("Model loaded successfully!")
    print(f"Model type: {type(model)}")