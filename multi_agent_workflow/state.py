from typing import Dict, List
from .models import DevelopmentCycle, Agent


class AppState:
    """
    A singleton class to hold the in-memory state of the application.
    This includes all development cycles and available agents.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AppState, cls).__new__(cls)
            cls._instance.cycles: Dict[str, DevelopmentCycle] = {}
            cls._instance.available_agents: Dict[str, Agent] = {
                "blackbox": Agent(
                    id="blackbox",
                    name="Blackbox",
                    role="Full Stack + Cloud Engineer",
                    model="blackboxai/meta-llama/llama-3.1-8b-instruct",
                ),
                "gemini": Agent(
                    id="gemini",
                    name="Gemini",
                    role="Senior QA Engineer",
                    model="gemini/gemini-1.5-pro-latest",  # Placeholder model
                ),
                "jules": Agent(
                    id="jules",
                    name="Jules",
                    role="Code Reviewer",
                    model="anthropic/claude-3-sonnet-20240229",  # Placeholder model
                ),
            }
        return cls._instance

    def get_cycle(self, cycle_id: str) -> DevelopmentCycle:
        return self.cycles.get(cycle_id)

    def add_cycle(self, cycle: DevelopmentCycle):
        self.cycles[cycle.id] = cycle

    def get_all_cycles(self) -> List[DevelopmentCycle]:
        return list(self.cycles.values())

    def get_available_agents(self) -> List[Agent]:
        return list(self.available_agents.values())


# Create a single instance of the app state
app_state = AppState()
