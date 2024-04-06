import threading
import time
import random

class ServerState:
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"

class LogEntry:
    def __init__(self, term, command):
        self.term = term
        self.command = command

class RaftNode:
    def __init__(self, node_id, all_nodes):
        # Initialize the RaftNode instance with node_id and list of all node_ids in the cluster
        self.node_id = node_id
        self.all_nodes = all_nodes
        # Reset the state of the node to initial values
        self.reset_state()

    def reset_state(self):
        # Reset the state of the node to follower
        self.state = ServerState.FOLLOWER
        # Initialize other state variables
        self.current_term = 0
        self.voted_for = None
        self.log = []
        self.commit_index = 0
        self.last_applied = 0
        self.next_index = {node_id: 1 for node_id in self.all_nodes}
        self.match_index = {node_id: 0 for node_id in self.all_nodes}
        self.votes_received = 0
        # Set initial election timeout
        self.election_timeout = time.time() + random.uniform(5, 10)
        self.heartbeat_received = False
        # Print initialization message
        print(f"{self.node_id} initialized as {self.state}")

    def send_request_vote(self, candidate_id):
        # Placeholder for sending RequestVote RPC
        pass

    def send_append_entries(self, leader_id):
        # Placeholder for sending AppendEntries RPC (also used for heartbeats)
        pass

    def become_candidate(self):
        # Transition to candidate state and start a new election term
        self.state = ServerState.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        self.votes_received = 1
        print(f"{self.node_id} becomes candidate for term {self.current_term}")
        self.start_election()

    def become_leader(self):
        # Transition to leader state and initialize next_index and match_index for each follower
        print(f"{self.node_id} becomes leader for term {self.current_term}")
        self.state = ServerState.LEADER
        for node_id in self.all_nodes:
            self.next_index[node_id] = len(self.log) + 1
            self.match_index[node_id] = 0

    def become_follower(self, term):
        # Transition to follower state and update current_term
        print(f"{self.node_id} becomes follower for term {self.current_term}")
        self.state = ServerState.FOLLOWER
        self.current_term = term
        self.voted_for = None
        self.reset_state()

    def start_election(self):
        # Start election by sending RequestVote RPCs to other nodes
        for node_id in self.all_nodes:
            if node_id != self.node_id:
                self.send_request_vote(node_id)
        self.election_timeout = time.time() + random.uniform(5, 10)

    def on_receive_vote(self, term, vote_granted):
        # Handle vote response from other nodes
        if self.state == ServerState.CANDIDATE and term == self.current_term and vote_granted:
            self.votes_received += 1
            if self.votes_received > len(self.all_nodes) // 2:
                self.become_leader()

    def on_receive_append_entries(self, term, leader_id, entries):
        # Handle AppendEntries RPCs from leader
        if term >= self.current_term:
            self.become_follower(term)
            self.heartbeat_received = True

    def main_loop(self):
        # Main loop of the node to handle state transitions
        print(f"{self.node_id} entering main loop as {self.state}")
        while True:
            if self.state == ServerState.FOLLOWER or self.state == ServerState.CANDIDATE:
                # Check for election timeout and transition to candidate state if necessary
                if time.time() >= self.election_timeout:
                    self.become_candidate()
            elif self.state == ServerState.LEADER:
                # Send heartbeats to followers
                self.send_append_entries(self.node_id)
                time.sleep(3)  # Sending heartbeat interval
            time.sleep(1)

if __name__ == "__main__":
    # Create RaftNode instances for each node_id and start their main loops in separate threads- PAIII HELP
    node_ids = ['node1', 'node2', 'node3']
    nodes = [RaftNode(node_id, node_ids) for node_id in node_ids]

    for node in nodes:
        threading.Thread(target=node.main_loop).start()
