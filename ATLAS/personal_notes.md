TypedDict

From typing module.

Lets you define a dictionary with fixed keys and type hints.

Example:

from typing import TypedDict

class User(TypedDict):
    name: str
    age: int


Now User is expected to be {"name": "Alice", "age": 25}.

👉 In your case, AcademicState is a TypedDict describing what keys the global state should have.


Annotated

From typing module too.

Lets you attach extra metadata to a type.

Example:

from typing import Annotated

Age = Annotated[int, "must be > 0"]


LangGraph uses this trick: you give it a type and a “reducer function” (how to merge values across steps).

So:

messages: Annotated[List[BaseMessage], add]


means “this is a list of BaseMessage objects, and when merging states, use add to combine them.”

add

That’s the reducer function for lists, imported from operator.

It tells LangGraph: “if two nodes return messages, merge them by concatenating (list1 + list2).”

BaseMessage

From LangChain.

Base class for all messages (HumanMessage, AIMessage, SystemMessage).

Lets you keep a conversation history as structured objects, not just strings.


profile, calendar, tasks, results

These are just the keys of your global state (AcademicState):

profile → a dictionary of student info (major, learning style, etc.).

Merges via dict_reducer (deep merge).

calendar → dictionary of scheduled events.

Merges via dict_reducer.

tasks → dictionary of to-do items.

Merges via dict_reducer.

results → dictionary where agents drop their outputs (like "calendar_analysis", "final_plan").

Merges via dict_reducer.

Type hint: Dict[str, Any] → keys are strings, values can be anything.

Academic state is a dictionary with lots of dictionaries inside