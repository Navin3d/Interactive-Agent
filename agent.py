from deepagents import create_deep_agent

from dotenv import load_dotenv
load_dotenv()

agent = create_deep_agent(
    model="google_genai:gemini-flash-lite-latest",
)

def ask_llm(question):
    for namespace, data in agent.stream(
            {"messages": [{"role": "user", "content": f"{question}"}]},
            stream_mode="messages",
            subgraphs=True,
    ):
        token, metadata = data
        if token.content:
            if len(token.content) > 0:
                if type(token.content) is list:
                    yield token.content[0]["text"]

if __name__ == "__main__":
    for namespace, data in agent.stream(
            {"messages": [{"role": "user", "content": "Your query"}]},
            stream_mode="messages",
            subgraphs=True,
    ):
        token, metadata = data
        # print(token)
        if token.content:
            if len(token.content) > 0:
                # print(type(token.content))
                if type(token.content) is list:
                    print(token.content[0]["text"], end="", flush=True)
