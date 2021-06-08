import time

from .component_registry import COMPONTENTS


def init_active_learning_component(al_config):
    try:
        Component = COMPONTENTS[al_config.model_name]
        return Component()
    except KeyError:
        raise Exception(
            f"Invalid component name {al_config.model_name} or component is not registered in component station"
        )
