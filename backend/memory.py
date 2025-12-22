class SessionMemory:
    def __init__(self):
        # Store history in a dictionary:
        # { session_id: [ {"role": "user", "content": "..."} ] }
        self.sessions = {}

    def get_history(self, session_id: str):
        """
        Return the history for the session.
        If no history exists, return an empty list.
        """
        return self.sessions.get(session_id, [])

    def add_message(self, session_id: str, role: str, content: str):
        """
        Add a message to the history for this session.
        """
        if session_id not in self.sessions:
            self.sessions[session_id] = []

        self.sessions[session_id].append({
            "role": role,
            "content": content
        })

    def clear(self, session_id: str):
        """
        Reset the session history (optional).
        """
        if session_id in self.sessions:
            del self.sessions[session_id]

