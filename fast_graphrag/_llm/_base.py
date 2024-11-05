"""LLM Services module."""

from dataclasses import dataclass, field
from typing import Any, Optional, Tuple, Type

import numpy as np

from fast_graphrag._prompt import PROMPTS
from fast_graphrag._types import GTResponseModel


async def format_and_send_prompt(
    prompt_key: str,
    llm: "BaseLLMService",
    format_kwargs: dict[str, Any],
    response_model: Type[GTResponseModel] | None = None,
    **args: Any,
) -> Tuple[GTResponseModel, list[dict[str, str]]]:
    """Get a prompt, format it with the supplied args, and send it to the LLM.

    Args:
        prompt_key (str): The key for the prompt in the PROMPTS dictionary.
        llm (BaseLLMService): The LLM service to use for sending the message.
        response_model (Type[GTResponseModel]): The expected response model.
        format_kwargs (dict[str, Any]): Dictionary of arguments to format the prompt.
        model (str | None): The model to use for the LLM. Defaults to None.
        max_tokens (int | None): The maximum number of tokens for the response. Defaults to None.
        **args (Any): Additional keyword arguments to pass to the LLM.

    Returns:
        GTResponseModel: The response from the LLM.
    """
    # Get the prompt from the PROMPTS dictionary
    prompt = PROMPTS[prompt_key]

    # Format the prompt with the supplied arguments
    formatted_prompt = prompt.format(**format_kwargs)

    # Send the formatted prompt to the LLM
    return await llm.send_message(prompt=formatted_prompt, response_model=response_model, **args)


@dataclass
class BaseLLMService:
    """Base class for Language Model implementations."""

    @dataclass
    class Config:
        model: Optional[str] = field(default=None)
        base_url: Optional[str] = field(default=None)

    config: Config = field(default_factory=lambda: BaseLLMService.Config())
    llm_async_client: Any = field(init=False, default=None)

    async def send_message(
        self,
        prompt: str,
        model: str | None = None,
        system_prompt: str | None = None,
        history_messages: list[dict[str, str]] | None = None,
        response_model: Type[GTResponseModel] | None = None,
        **kwargs: Any,
    ) -> Tuple[GTResponseModel, list[dict[str, str]]]:
        """Send a message to the language model and receive a response.

        Args:
            prompt (str): The input message to send to the language model.
            model (str): The name of the model to use.
            system_prompt (str, optional): The system prompt to set the context for the conversation. Defaults to None.
            history_messages (list, optional): A list of previous messages in the conversation. Defaults to empty.
            response_model (Type[T], optional): The Pydantic model to parse the response. Defaults to None.
            **kwargs: Additional keyword arguments that may be required by specific LLM implementations.

        Returns:
            str: The response from the language model.
        """
        raise NotImplementedError


@dataclass
class BaseEmbeddingService:
    """Base class for Language Model implementations."""

    @dataclass
    class Config:
        embedding_dim: int = field(default=1536)
        model: Optional[str] = field(default="text-embedding-3-small")
        base_url: Optional[str] = field(default=None)

    config: Config = field(default_factory=lambda: BaseEmbeddingService.Config())
    embedding_async_client: Any = field(init=False, default=None)

    async def get_embedding(
        self, texts: list[str], model: Optional[str] = None
    ) -> np.ndarray[Any, np.dtype[np.float32]]:
        """Get the embedding representation of the input text.

        Args:
            texts (str): The input text to embed.
            model (str): The name of the model to use.

        Returns:
            list[float]: The embedding vector as a list of floats.
        """
        raise NotImplementedError

    def validate_embedding_dim(self, embedding_dim: int) -> bool:
        """Validate the embedding dimension.

        Args:
            embedding_dim (int): The embedding dimension to validate.

        Returns:
            bool: True if the embedding dimension is valid, False otherwise.
        """
        raise NotImplementedError
