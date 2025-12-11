from pydantic import BaseModel, Field
from typing import List, Optional
import time


class Agent(BaseModel):
    """Represents an AI agent that can participate in a development cycle."""

    id: str = Field(
        description="Unique identifier for the agent (e.g., 'blackbox', 'gemini')."
    )
    name: str = Field(
        description="Display name for the agent (e.g., 'Blackbox', 'Gemini QA')."
    )
    role: str = Field(
        description="Role of the agent in the cycle (e.g., 'Full Stack Engineer', 'QA Senior')."
    )
    model: Optional[str] = Field(
        None,
        description="The specific AI model the agent uses (e.g., 'blackboxai/meta-llama/llama-3.1-8b-instruct').",
    )


class GitHubLink(BaseModel):
    """Represents a link to a GitHub issue or pull request."""

    issue_url: Optional[str] = Field(None, description="URL of the GitHub issue.")
    pr_url: Optional[str] = Field(None, description="URL of the GitHub pull request.")
    branch_name: Optional[str] = Field(
        None, description="Name of the associated git branch."
    )


class ChatMessage(BaseModel):
    """Represents a single message in a chat thread."""

    sender: str = Field(description="Who sent the message ('user' or agent's id).")
    text: str = Field(description="The content of the message.")
    timestamp: float = Field(
        default_factory=time.time,
        description="Unix timestamp of when the message was created.",
    )


class DevelopmentCycle(BaseModel):
    """Represents a single workspace or tab for a multi-agent development cycle."""

    id: str = Field(description="Unique identifier for the development cycle.")
    title: str = Field(
        description="A descriptive title for the cycle (e.g., 'Feature X Backend')."
    )
    messages: List[ChatMessage] = Field(
        default_factory=list, description="The chat history for this cycle."
    )
    active_agents: List[Agent] = Field(
        default_factory=list,
        description="A list of agents participating in this cycle.",
    )
    github_link: Optional[GitHubLink] = Field(
        None, description="An optional link to a related GitHub issue/PR."
    )
    created_at: float = Field(default_factory=time.time)
