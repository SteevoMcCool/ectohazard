import sys

def __getitem__(name):
    return sys.modules[f"EntityBehaviors.{name}"]