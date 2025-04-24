import abc

class BaseAgent(abc.ABC):

    def __init__(self, client, model, system_prompt: str, user_prompt: str):
        self.client = client
        self.model = model
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

    @abc.abstractmethod
    def predict(self, example):
        pass

    def _call_model(self, filled_user_prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user",
                "content": filled_user_prompt},
            ],
            temperature=0,
            stream=False
        )

        return response.choices[0].message.content

    @abc.abstractmethod
    def extract_answer(self, answer: str):
        pass