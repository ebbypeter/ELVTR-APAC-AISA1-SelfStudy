# Lesson 3 Tests

# Imports 
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# Initialize OpenAI Wrapper
agent_openai_gpt4o = ChatOpenAI(
    name="OpenAI GPT-4o",
    model="gpt-4o",
    temperature=0.7,
    api_key=os.getenv('OPENAI_API_KEY'),
    organization=os.getenv('OPENAI_ORG_ID') if os.getenv('OPENAI_ORG_ID') else None
) 
print("ℹ️  OpenAI client initialized successfully with GPT-4o mode")

agent_openai_gpt52 = ChatOpenAI(
    name="OpenAI gpt-5.2",
    model="gpt-5.2",
    temperature=0.7,
    api_key=os.getenv('OPENAI_API_KEY'),
    organization=os.getenv('OPENAI_ORG_ID') if os.getenv('OPENAI_ORG_ID') else None
) 
print("ℹ️  OpenAI client initialized successfully with gpt-5.2 mode")

agent_anthropic_claudesonnet45 = ChatAnthropic(
    name="Anthropic Claude Sonnet-4.5",
    model="claude-sonnet-4-5",
    temperature=0.7,
    api_key=os.getenv('CLAUDE_API_KEY')
)
print("ℹ️  Anthropic client initialized successfully with Claude Sonnet-4.5 mode")

print("=" * 70)
# ---------------------------------------------------------------------------------------

# Test 1: Simple Prompt with GPT-4o & gpt-5.2
print ("\nTest 1: Simple Prompt with GPT-4o & GPT-5.2")
prompt_template = ChatPromptTemplate.from_template(
    """You are a helpful technical writer.
    Write a brief explanation of the following concept for {audience}.
    Concept: {concept}
    
    Keep the explanation concise and clear, and constriant it to {word_count} words."""
    )

# Chains
chain_openai_gpt4o = prompt_template | agent_openai_gpt4o | StrOutputParser()
chain_openai_gpt52 = prompt_template | agent_openai_gpt52 | StrOutputParser()
chain_antropic_claudesonnet45 = prompt_template | agent_anthropic_claudesonnet45 | StrOutputParser()

prompt_template.format(audience="beginner programmers", concept="Asynchronous Programming", word_count=50)

print("🔷  GPT-4o Response:")
response_gpt4o = chain_openai_gpt4o.invoke({
    "audience": "beginner programmers",
    "concept": "Asynchronous Programming",
    "word_count": 50
})
print(f"{response_gpt4o}\n")

print("🔷  GPT-5.2 Response:")
response_gpt52 = chain_openai_gpt52.invoke({
    "audience": "beginner programmers",
    "concept": "Asynchronous Programming",
    "word_count": 50
})
print(f"{response_gpt52}\n")

print("🔷  Claude Sonnet-4.5 Response:")
response_claudesonnet45 = chain_antropic_claudesonnet45.invoke({
    "audience": "beginner programmers",
    "concept": "Asynchronous Programming",
    "word_count": 50
})
print(f"{response_claudesonnet45}\n")
print("=" * 70)
# ---------------------------------------------------------------------------------------

