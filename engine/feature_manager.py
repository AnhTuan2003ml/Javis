"""
Feature Manager - Modular system for extending dual_ai functionality
Allows adding new features without modifying the main dual_ai.py file
"""

import os
import importlib
import inspect
from typing import Dict, List, Callable, Any

class FeatureManager:
    def __init__(self):
        self.features = {}
        self.natural_language_mappings = {}
        self.feature_responses = {}
        self.load_all_features()
    
    def load_all_features(self):
        """Load all feature modules from the features directory"""
        features_dir = os.path.join(os.path.dirname(__file__), 'features')
        if not os.path.exists(features_dir):
            os.makedirs(features_dir)
            return
        
        for filename in os.listdir(features_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                self.load_feature(module_name)
    
    def load_feature(self, module_name: str):
        """Load a specific feature module"""
        try:
            module = importlib.import_module(f'engine.features.{module_name}')
            
            # Get feature class
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and hasattr(obj, 'feature_name'):
                    feature_instance = obj()
                    feature_name = feature_instance.feature_name
                    
                    # Register feature methods
                    self.features[feature_name] = feature_instance
                    
                    # Register natural language mappings
                    if hasattr(feature_instance, 'natural_language_mappings'):
                        self.natural_language_mappings.update(feature_instance.natural_language_mappings)
                    
                    # Register responses
                    if hasattr(feature_instance, 'responses'):
                        self.feature_responses.update(feature_instance.responses)
                    
                    print(f"Loaded feature: {feature_name}")
                    break
        except Exception as e:
            print(f"Error loading feature {module_name}: {e}")
    
    def execute_feature(self, command: str, *args, **kwargs):
        """Execute a feature command"""
        # Check natural language mappings first
        mapped_command = self.natural_language_mappings.get(command.lower())
        if mapped_command:
            command = mapped_command
        
        # Find and execute the command
        for feature_name, feature_instance in self.features.items():
            if hasattr(feature_instance, command):
                method = getattr(feature_instance, command)
                try:
                    result = method(*args, **kwargs)
                    return result
                except Exception as e:
                    return f"Error executing {command}: {e}"
        
        return None
    
    def get_response(self, func_name: str) -> str:
        """Get response message for a function"""
        return self.feature_responses.get(func_name, "Feature executed successfully.")
    
    def get_all_commands(self) -> List[str]:
        """Get list of all available commands"""
        commands = []
        for feature_instance in self.features.values():
            for name, method in inspect.getmembers(feature_instance, predicate=inspect.ismethod):
                if not name.startswith('_'):
                    commands.append(name)
        return commands
    
    def get_natural_language_mappings(self) -> Dict[str, str]:
        """Get all natural language mappings"""
        return self.natural_language_mappings

# Global feature manager instance
feature_manager = FeatureManager()