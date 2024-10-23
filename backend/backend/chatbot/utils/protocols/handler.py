from typing import Protocol, Any

class Handler(Protocol):
    key: str

    def __init__(self, state: dict[str, Any] | None):
        raise NotImplementedError("Not Implemented")

    def match_intent(self, query: str) -> float | None:
        """
        Returns the id and similarity of the matched

        :param query: user input

        :returns: similarity
            the cosine similarity score of the matched intent
        """
        raise NotImplementedError("Not Implemented")

    async def generate_initial_response(self) -> tuple[str, bool]:
        """
        Returns the response, as well as if the response requires further prompts

        :returns: (response, finished)
            response: the output to print,
            is_finished: whether the reponse requires further prompt
        """
        raise NotImplementedError("Not Implemented")

    async def generate_followup_response(self, query: str) -> tuple[str, bool]:
        """
        Returns the response, as well as if the response requires further prompts

        :param query: user input

        :returns: (response, finished)
            response: the output to print,
            is_finished: whether the reponse requires further prompt
        """
        raise NotImplementedError("Not Implemented")

    def export_state(self) -> dict[str, Any]:
        """
        Exports the internal states to be stored and imported next time
        """
        raise NotImplementedError("Not Implemented")
