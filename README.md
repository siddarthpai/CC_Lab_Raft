Cloud Computing Final Project
Cluster Setup:
The optimal number of nodes, considering the trade-off between fault tolerance and the complexity of managing more nodes. We are choosing a cluster of three nodes, which allows a failure while still maintaining two nodes for maintaining majority for consensus.

Raft roles: follower, candidate, and leader.
Follower: 
The default state
 receives and logs updates from the leader.
Candidate: 
A node transitions to this state if it hasn't heard from the leader in a while
Starting an election.
Leader: Manages log replication across the cluster and handles client requests.

Triggers causing Transitions:
Follower State:
Timeout on Receiving Heartbeat:If a follower does not receive a heartbeat within an election timeout, transitions to the candidate state, initiating a leader election.
Candidate State:
Timeout on Becoming Leader: If a candidate does not receive a majority of votes (2 nodes) within the election timeout, it triggers a new election by restarting its election timer and transitioning back to the candidate state.
Receiving Votes from Majority: If a candidate receives votes from a majority of nodes(2 nodes) in the cluster, it transitions to the leader state.
Leader State:
Timeout on Sending Heartbeat: Leaders regularly send heartbeat messages to followers to maintain their authority. If a leader does not send a heartbeat within heartbeat timeout, triggers a new leader election process by transitioning to the candidate state.
Loss of Majority Support: If a leader detects that it no longer has the support of a majority of nodes due to network partition or node failures, it steps down from its leadership role and transitions to the follower state.
Received Request for Leadership Change: If a leader receives a request for leadership change from another node with a higher term number, it steps down and transitions to the follower state.

Things we need to implement: Log Replication (RPL module), Heartbeat mech. 

Communication Protocol Def:
Nodes need to communicate with each other to reach a consensus. This communication protocol includes messages such as:
RequestVote: Sent by candidates to request votes from other nodes.
AppendEntries: Sent by leaders to replicate log entries and to act as a heartbeat.
Response messages for each type of request.
Implement Raft Algorithm:
The core of the Raft algorithm involves implementing the roles of followers, candidates, and leaders, along with their associated behaviors.
Implement the mechanisms for leader election, log replication, and safety properties.
Ensure that the state transitions and timeouts defined in the Raft algorithm specification are correctly implemented.
Test and Validate:
Test scenarios could include network partitions, node failures, message delays, and various combinations of these conditions.
Validate that the implementation satisfies the safety and liveness properties of the Raft algorithm.
Benchmark the implementation to measure its performance under different workloads and configurations.

