"""
State Models and Data Structures

This module contains the core state management classes and helper functions
for the ATLAS academic assistance system.
"""
from typing import TypedDict, Annotated, List, Dict, Any, TypeVar
from operator import add
from langchain_core.messages import BaseMessage

T = TypeVar('T')


def dict_reducer(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge two dictionaries recursively.

    This function is used by LangGraph to merge state updates across different
    agents and workflow steps.

    Args:
        dict1: First dictionary to merge
        dict2: Second dictionary to merge

    Returns:
        Dict[str, Any]: Merged dictionary with recursive merging for nested dicts

    Example:
        >>> dict1 = {"a": {"x": 1}, "b": 2}
        >>> dict2 = {"a": {"y": 2}, "c": 3}
        >>> result = dict_reducer(dict1, dict2)
        >>> # result = {"a": {"x": 1, "y": 2}, "b": 2, "c": 3}
    """
    merged = dict1.copy()
    for key, value in dict2.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = dict_reducer(merged[key], value)
        else:
            merged[key] = value 
    
    return merged 


class AcademicState(TypedDict):
    """
    Master state container for the academic assistance system.
    
    This TypedDict defines the structure of the state that flows through
    the LangGraph workflow. Each field has an associated reducer function
    that determines how updates are merged.
    
    Attributes:
        messages: List of conversation messages (appended with add)
        profile: Student profile data (merged with dict_reducer)
        calendar: Calendar and scheduling data (merged with dict_reducer)
        tasks: Task and assignment data (merged with dict_reducer)
        results: Agent analysis results (merged with dict_reducer)
    """
    messages: Annotated[List[BaseMessage], add]
    profile: Annotated[Dict, dict_reducer]
    calendar: Annotated[Dict, dict_reducer]
    tasks: Annotated[Dict, dict_reducer]
    results: Annotated[Dict[str, Any], dict_reducer]
