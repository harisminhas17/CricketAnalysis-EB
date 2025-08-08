import os
import torch
import yaml
from pathlib import Path

# Add Optuna import
try:
    import optuna
except ImportError:
    os.system("pip install optuna")
    import optuna
import argparse

def train_yolo11(optuna_trial=None, custom_params=None):
    print("=== YOLO 11 Training Script ===")
    
    # Update model path to local directory
    yolo11_model_path = Path('yolo11n.pt')
    if not yolo11_model_path.exists():
        print(f"Error: YOLO 11 model {yolo11_model_path} not found!")
        return None
    
    print(f"✓ Found YOLO 11 model: {yolo11_model_path}")
    
    # Check data.yaml
    if not Path('data.yaml').exists():
        print("Error: data.yaml not found!")
        return None
    
    print("✓ Found data.yaml")
    
    # Check dataset
    if not Path('dataset/train/images').exists():
        print("Error: Training images not found!")
        return None
    
    print("✓ Found training images")
    
    # Check labels
    labels_dir = Path('dataset/train/labels')
    if not labels_dir.exists():
        print("Error: Labels directory not found! Run convert_csv_to_yolo.py first.")
        return None
    
    label_count = len(list(labels_dir.glob('*.txt')))
    print(f"✓ Found {label_count} label files")
    
    # Install ultralytics if not available
    try:
        from ultralytics import YOLO
        print("✓ Ultralytics YOLO available")
    except ImportError:
        print("Installing ultralytics...")
        os.system("pip install ultralytics")
        from ultralytics import YOLO
        print("✓ Ultralytics YOLO installed")
    
    # Load and train the model
    print("\n=== Starting YOLO 11 Training ===")
    
    try:
        # Load the YOLO 11 model
        model = YOLO(str(yolo11_model_path))
        print(f"✓ Loaded YOLO 11 model: {yolo11_model_path}")
        
        # Default params
        params = {
            'data': 'data.yaml',
            'epochs': 50,
            'imgsz': 640,
            'batch': 16,
            'name': 'yolo11_ball_detect',
            'project': 'runs/train',
            'verbose': True,
            'save': True,
            'save_period': 10
        }
        # If Optuna trial, override with suggested params
        if optuna_trial is not None:
            params['epochs'] = optuna_trial.suggest_int('epochs', 20, 100)
            params['imgsz'] = optuna_trial.suggest_categorical('imgsz', [416, 512, 640, 800])
            params['batch'] = optuna_trial.suggest_categorical('batch', [8, 16, 32])
            params['lr0'] = optuna_trial.suggest_loguniform('lr0', 1e-4, 1e-1)
            params['name'] = f"optuna_trial_{optuna_trial.number}"
        if custom_params is not None:
            params.update(custom_params)
        # Start training
        results = model.train(
            data=params['data'],
            epochs=params['epochs'],
            imgsz=params['imgsz'],
            batch=params['batch'],
            name=params['name'],
            project=params['project'],
            verbose=params['verbose'],
            save=params['save'],
            save_period=params['save_period'],
            lr0=params.get('lr0', None)
        )
        
        print("✓ Training completed successfully!")
        print(f"Results saved in: runs/train/{params['name']}/")
        
        # For Optuna: return best mAP50-95 from results (if available)
        if optuna_trial is not None:
            try:
                # Ultralytics saves metrics in results dict
                best_map = results.metrics.get('metrics/mAP_0.5:0.95', None)
                if best_map is None:
                    # fallback to mAP_0.5
                    best_map = results.metrics.get('metrics/mAP_0.5', 0)
                return best_map
            except Exception as e:
                print(f"Optuna: Could not fetch mAP: {e}")
                return 0
        return results
        
    except Exception as e:
        print(f"Error during training: {e}")
        print("Please check your model file and dataset.")
        return None

def optuna_tune(n_trials=10):
    def objective(trial):
        return train_yolo11(optuna_trial=trial)
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)
    print("\n=== Optuna Tuning Complete ===")
    print("Best trial:")
    print(study.best_trial)
    print("Best hyperparameters:")
    print(study.best_trial.params)
    # Save best params
    with open("best_yolo11_hyperparams.yaml", "w") as f:
        yaml.dump(study.best_trial.params, f)
    return study

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--optuna', action='store_true', help='Run Optuna hyperparameter tuning')
    parser.add_argument('--trials', type=int, default=10, help='Number of Optuna trials')
    args = parser.parse_args()
    if args.optuna:
        optuna_tune(n_trials=args.trials)
    else:
        train_yolo11() 