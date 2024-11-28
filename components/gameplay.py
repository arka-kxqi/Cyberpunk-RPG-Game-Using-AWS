from agent_interaction import ConverseAgent
from interaction_tools import ConverseToolManager
from tool_registry import register_game_tools
from world_state import GameState
class Game:
    def __init__(self, model_id='anthropic.claude-3-5-haiku-20241022-v1:0', display_callback=None):
        self.display_callback = display_callback
        self.state = GameState(display_callback=self.game_state_display_callback)
        self.tools = ConverseToolManager()
        register_game_tools(self.tools, self.state)
        self.agent = ConverseAgent(model_id=model_id)
        self.agent.system_prompt = open("system.txt", "r").read()
        self.agent.tools = self.tools
        self.agent.response_output_tags = ['<response>', '</response>']
    def game_state_display_callback(self, message):
        try:
            if message['tool_name'] == 'roll_dice':
                if 'response' in message:
                    self.display_callback(f"🎲 {message['response']}", "dice")
        except Exception as e:
            print(f"Error in display callback: {str(e)}")
    def start_game(self, theme):
        start_prompt = f"Booting up a {theme} cyberpunk adventure. Your neon-lit journey begins now..."
        return self.agent.invoke_with_prompt(start_prompt)
    def process_command(self, command):
        if not command:
            return None, None            
        response = self.agent.invoke_with_prompt(command)
        room_info = ""
        inventory_info = ""
        if self.state.player_id:
            current_sector = self.state.get_player_room(self.state.player_id)
            if current_sector:
                sector_desc = self.state.get_room_description(current_sector)
                room_info = f"Current Zone: {current_sector}: {sector_desc}"

            player_inventory = self.state.get_player_objects(self.state.player_id)
            if player_inventory:
                inventory_info += f"Cyber Gear: {player_inventory}"
        return response, room_info, inventory_info