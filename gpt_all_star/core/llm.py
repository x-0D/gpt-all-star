import os
from enum import Enum

import openai
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models import ChatYandexGPT
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_openai import AzureChatOpenAI, ChatOpenAI


class LLM_TYPE(str, Enum):
    OPENAI = "OPENAI"
    AZURE = "AZURE"
    ANTHROPIC = "ANTHROPIC"
    MISTRAL = "MISTRAL"
    YANDEXGPT = "YANDEXGPT"


def create_llm(llm_name: LLM_TYPE) -> BaseChatModel:
    if llm_name == LLM_TYPE.OPENAI:
        return _create_chat_openai(
            model_name=os.getenv("OPENAI_API_MODEL", "gpt-4o"),
            temperature=0.1,
        )
    elif llm_name == LLM_TYPE.AZURE:
        return _create_azure_chat_openai(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            openai_api_version=os.getenv(
                "AZURE_OPENAI_API_VERSION", "2024-05-01-preview"
            ),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
            model_name=os.getenv("AZURE_OPENAI_API_MODEL", "gpt-4o"),
            temperature=0.1,
        )
    elif llm_name == LLM_TYPE.ANTHROPIC:
        return _create_chat_anthropic(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
            model_name=os.getenv("ANTHROPIC_API_MODEL", "claude-3-opus-20240229"),
            temperature=0.1,
        )
    elif llm_name == LLM_TYPE.MISTRAL:
        return _create_chat_mistral(
            model_name=os.getenv("MISTRAL_API_MODEL", "codestral-latest"),
            temperature=0.1,
        )
    elif llm_name == LLM_TYPE.YANDEXGPT:
        return _create_chat_yandexgpt(
            model_name=os.getenv("YANDEXGPT_API_MODEL", "yandexgpt-lite"),
            folder_id=os.getenv("YANDEXGPT_FOLDER_ID"),
            temperature=0.1,
        )
    else:
        raise ValueError(f"Unsupported LLM type: {llm_name}")


def _create_chat_openai(model_name: str, temperature: float) -> ChatOpenAI:
    openai.api_type = "openai"
    return ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
        streaming=True,
        client=openai.chat.completions,
    )


def _create_azure_chat_openai(
    api_key: str,
    azure_endpoint: str,
    openai_api_version: str,
    deployment_name: str,
    model_name: str,
    temperature: float,
) -> AzureChatOpenAI:
    openai.api_type = "azure"
    return AzureChatOpenAI(
        api_key=api_key,
        azure_endpoint=azure_endpoint,
        openai_api_version=openai_api_version,
        deployment_name=deployment_name,
        model_name=model_name,
        temperature=temperature,
        streaming=True,
    )


def _create_chat_anthropic(
    anthropic_api_key: str, model_name: str, temperature: float
) -> ChatAnthropic:
    return ChatAnthropic(
        anthropic_api_key=anthropic_api_key,
        model=model_name,
        temperature=temperature,
        streaming=True,
    )

def _create_chat_mistral(model_name: str, temperature: float) -> ChatMistralAI:
    return ChatMistralAI(
        model=model_name,
        temperature=temperature,
        maxRetries=2,  # Optional: specify how many times to retry on failure
    )

def _create_chat_yandexgpt(folder_id: str ,model_name: str, temperature: float) -> ChatYandexGPT:
    return ChatYandexGPT(
        folder_id=folder_id,
        model_name=model_name,
        temperature=temperature
    )
