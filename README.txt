Simulation of Banker's Algorithm for resource allocation and deadlock avoidance algorithm.

EXAMPLE INPUT:
First line contains resources, processes.
Second line is available of each type.

Part 1 checks the safety of the state for each input file.
Part 2 actually simulates Banker's on "example2.txt".

Sample Output:
...
Customer 0 successfully released [0, 0, 0].
Customer 1 successfully released [1, 0, 0].
Customer 2 request exceed maximum resources and cannot be processed at this time.
Customer 2 failed to acquire [1, 0, 1].
Customer 3 request exceed maximum resources and cannot be processed at this time.
Customer 3 failed to acquire [1, 1, 2].
Customer 4 successfully released [0, 0, 2].
CHECK RESULTED IN SAFE STATE
SAFE: Request is valid and produces a safe state.
Customer 2 successfully requested [4, 0, 0].
Customer 4 successfully released [0, 0, 0].
Customer 2 successfully released [4, 0, 0].
....

I created a class that keeps track of all data associated with banker's algorithm.
Threads call this class' simulate method (syncronized w/lock) and mutate the class
instance variables.

__init__ - initializes state and performs state check. if the state comes back unstable
no future work can be done on the instance.

safe_check - runs Banker's algorithm to check for potential deadlock

handle_request - attempt to request resources for a customer

handle_release - attempt to release resources for a customer

I surpressed a lot of output to make the text submission easier to read but banker has a toString method implemented if you want to see the details.
