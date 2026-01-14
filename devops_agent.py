
import subprocess
from langchain_community.llms import Ollama
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from command_policy import is_command_allowed
import shlex

# -----------------------------
# SAFE COMMAND EXECUTOR
# -----------------------------
def safe_run_command(command: str) -> str:
    allowed, reason = is_command_allowed(command)
    if not allowed:
        return reason
    try:
        result = subprocess.run(
            shlex.split(command),
            capture_output=True,
            text=True,
            timeout=10
        )
        output = (result.stdout + "\n" + result.stderr).strip()
        return output if output else "✅ Command executed successfully"
    except Exception as e:
        return f"Execution error: {str(e)}"
# -----------------------------
# LANGCHAIN TOOL
# -----------------------------
shell_tool = Tool(
    name="RunLinuxCommand",
    func=safe_run_command,
    description=(
        "Run ONE Linux command at a time. "
        "Do NOT use pipes (|), redirection, grep, awk, sed, or shell operators. "
        "Return full raw output; filtering must be done by reasoning."
    )
)
# -----------------------------
# LLM (OLLAMA)
# -----------------------------
llm = Ollama(
    model="llama3",
    temperature=0
)
# -----------------------------
# MEMORY
# -----------------------------
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
# -----------------------------
# AGENT
# -----------------------------
agent = initialize_agent(
    tools=[shell_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)
# -----------------------------
# RUNNER
# -----------------------------
def run_devops_agent(goal: str):
    print("\n🧠 DevOps Agent Started")
    print("🎯 Goal:", goal)
    print("-" * 60)
    result = agent.run(goal)
    print("\n✅ FINAL RESULT")
    print("-" * 60)
    print(result)
# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    goal = input("\nEnter DevOps task:\n> ")
    run_devops_agent(goal)
