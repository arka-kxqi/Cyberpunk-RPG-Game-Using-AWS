import boto3, json, re
class ConverseAgent:
    def __init__(self, model_id, region='us-west-2', system_prompt='You are a rogue AI assistant in a dystopian future.'):
        self.model_id = model_id
        self.region = region
        self.client = boto3.client('bedrock-runtime', region_name=self.region)
        self.system_prompt = system_prompt
        self.messages = []
        self.tools = None
        self.response_output_tags = []
    def invoke_with_prompt(self, prompt):
        content = [{'text': prompt}]
        return self.invoke(content)
    def invoke(self, content):
        self.messages.append({"role": "user", "content": content})
        response = self._get_converse_response()
        return self._handle_response(response)
    def _get_converse_response(self):
        response = self.client.converse(
            modelId=self.model_id,
            messages=self.messages,
            system=[{"text": self.system_prompt}],
            inferenceConfig={"maxTokens": 1024, "temperature": 0.7},
            toolConfig=self.tools.get_tools()
        )
        return response
    def _handle_response(self, response):
        self.messages.append(response['output']['message'])
        stop_reason = response['stopReason']
        if stop_reason in ['end_turn', 'stop_sequence']:
            try:
                message = response.get('output', {}).get('message', {})
                content = message.get('content', [])
                text = content[0].get('text', '')
                if self.response_output_tags:
                    pattern = f"(?s).*{re.escape(self.response_output_tags[0])}(.*?){re.escape(self.response_output_tags[1])}"
                    match = re.search(pattern, text)
                    if match:
                        return match.group(1)
                return text
            except (KeyError, IndexError):
                return ''