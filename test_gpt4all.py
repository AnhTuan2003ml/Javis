#!/usr/bin/env python3
"""Test GPT4All initialization"""

import os
import sys

def test_gpt4all_init():
    """Test the GPT4All initialization function"""
    print("Testing GPT4All initialization...")
    
    try:
        from gpt4all import GPT4All
        print("✓ GPT4All library imported successfully")
        
        # Test the exact path and model from the code
        model_path = r"C:\Users\Hp\AppData\Local\nomic.ai\GPT4All"
        available_models = [
            "Llama-3.2-1B-Instruct-Q4_0.gguf",
        ]
        
        print(f"Checking model path: {model_path}")
        if os.path.exists(model_path):
            print("✓ Model directory exists")
            print(f"Directory contents: {os.listdir(model_path)}")
        else:
            print("✗ Model directory does not exist")
            return False
        
        # Check for available models
        model_name = None
        for model in available_models:
            full_path = os.path.join(model_path, model)
            print(f"Checking model: {full_path}")
            if os.path.exists(full_path):
                model_name = model
                print(f"✓ Found model: {model_name}")
                break
            else:
                print(f"✗ Model not found: {model}")
        
        if not model_name:
            print("✗ No models found")
            return False
        
        # Try to initialize the model
        print(f"Attempting to initialize {model_name}...")
        local_model = GPT4All(
            model_name,
            model_path=model_path,
            verbose=False,
            device='cpu',
            n_threads=6,
            n_ctx=1024
        )
        print(f"✓ GPT4All {model_name} initialized successfully")
        
        # Test a simple query
        print("Testing simple query...")
        response = local_model.generate("Hello", max_tokens=10)
        print(f"✓ Test response: {response}")
        
        return True
        
    except ImportError as e:
        print(f"✗ GPT4All library not installed: {e}")
        print("Install with: pip install gpt4all")
        return False
    except Exception as e:
        print(f"✗ GPT4All initialization failed: {e}")
        return False

if __name__ == "__main__":
    success = test_gpt4all_init()
    if success:
        print("\n✓ GPT4All is working correctly!")
    else:
        print("\n✗ GPT4All test failed!")
    
    input("Press Enter to exit...")