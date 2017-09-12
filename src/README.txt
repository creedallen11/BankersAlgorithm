I created a class that keeps track of all data associated with banker's algorithm.
Threads call this class' simulate method (syncronized w/lock) and mutate the class
instance variables.

__init__ - initializes state and performs state check. if the state comes back unstable
no future work can be done on the instance.

safe_check - runs Banker's algorithm to check for potential deadlock

handle_request - attempt to request resources for a customer

handle_release - attempt to release resources for a customer

I surpressed a lot of output to make the text submission easier to read but banker has a to 
string method if you want to check my code. 