import networkx as nx
import random
class GameState:
    def __init__(self, display_callback=None):
        self.graph = nx.MultiDiGraph()
        self.player_id = None
        self.display_callback = display_callback
    def tool_response(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if self.display_callback:
                self.display_callback({
                    "tool_name": func.__name__,
                    "response": result
                })
            return result
        return wrapper
    @tool_response
    def create_room(self, room_id, description=''):
        if self.graph.has_node(room_id):
            raise ValueError(f"Room '{room_id}' already exists.")
        self.graph.add_node(room_id, type='room', description=description) 
        return(f"Room '{room_id}' created in the neon-lit cityscape.")
    @tool_response
    def connect_rooms(self, room1_id, room2_id, direction, reverse_direction=None):
        if not (self.graph.has_node(room1_id) and self.graph.has_node(room2_id)):
            raise ValueError("Both rooms must exist to create a connection.")
        self.graph.add_edge(room1_id, room2_id, type='connected_to', direction=direction)
        if reverse_direction:
            self.graph.add_edge(room2_id, room1_id, type='connected_to', direction=reverse_direction)
        return(f"Neon tunnels between '{room1_id}' and '{room2_id}' are linked ({direction}).")
    @tool_response
    def create_player(self, player_id, name):
        if self.player_id is not None:
            raise Exception("Player already exists.")
        if self.graph.has_node(player_id):
            raise ValueError(f"Entity '{player_id}' already exists.")
        self.player_id = player_id
        self.graph.add_node(player_id, type='player', name=name)
        return(f"Cyber-protagonist '{name}' with ID '{player_id}' created in the urban sprawl.")
    @tool_response
    def move_player(self, player_id, to_room_id):
        if not self.graph.has_node(to_room_id):
            raise ValueError(f"Room '{to_room_id}' does not exist.")
        for edge in list(self.graph.edges(player_id, data=True, keys=True)):
            if edge[3]['type'] == 'located_in':
                self.graph.remove_edge(*edge[:3])
        self.graph.add_edge(player_id, to_room_id, type='located_in')
        return(f"Cyber-agent '{player_id}' relocated to room '{to_room_id}'.")
    @tool_response
    def create_npc(self, npc_id, name):
        if self.graph.has_node(npc_id):
            raise ValueError(f"Entity '{npc_id}' already exists.")
        self.graph.add_node(npc_id, type='npc', name=name)
        return(f"NPC '{name}' with ID '{npc_id}' created in the shadows of the city.")
    @tool_response
    def move_npc(self, npc_id, to_room_id):
        if not self.graph.has_node(to_room_id):
            raise ValueError(f"Room '{to_room_id}' does not exist.")
        for edge in list(self.graph.edges(npc_id, data=True, keys=True)):
            if edge[3]['type'] == 'located_in':
                self.graph.remove_edge(*edge[:3])
        self.graph.add_edge(npc_id, to_room_id, type='located_in')
        return(f"NPC '{npc_id}' moved to room '{to_room_id}'.")
    @tool_response
    def create_object(self, object_id, name):
        if self.graph.has_node(object_id):
            raise ValueError(f"Entity '{object_id}' already exists.")
        self.graph.add_node(object_id, type='object', name=name)
        return(f"Object '{name}' with ID '{object_id}' created — perfect for the high-tech world.")
    @tool_response
    def add_object_to_room(self, object_id, room_id):
        if not (self.graph.has_node(object_id) and self.graph.has_node(room_id)):
            raise ValueError(f"Both object and room must exist.")
        for edge in list(self.graph.edges(object_id, data=True, keys=True)):
            if edge[3]['type'] in ('located_in', 'held_by'):
                self.graph.remove_edge(*edge[:3])
        self.graph.add_edge(object_id, room_id, type='located_in')
        return(f"Object '{object_id}' placed in room '{room_id}' — could it be a trap or treasure?")
    @tool_response
    def player_take_object(self, player_id, object_id):
        if not (self.graph.has_node(player_id) and self.graph.has_node(object_id)):
            raise ValueError("Both player and object must exist.")
        player_room = self.get_player_room(player_id)
        object_room = self.get_object_location(object_id)
        if player_room != object_room:
            raise ValueError("Object is not in the same room as the player.")
        for edge in list(self.graph.edges(object_id, data=True, keys=True)):
            if edge[3]['type'] in ('located_in', 'held_by'):
                self.graph.remove_edge(*edge[:3])
        self.graph.add_edge(player_id, object_id, type='holds')
        return(f"Player '{player_id}' grabbed object '{object_id}' — it's now in their possession.")
    @tool_response
    def player_drop_object(self, player_id, object_id):
        if not (self.graph.has_node(player_id) and self.graph.has_node(object_id)):
            raise ValueError("Both player and object must exist.")
        for edge in list(self.graph.edges(player_id, data=True, keys=True)):
            if edge[1] == object_id and edge[3]['type'] == 'holds':
                self.graph.remove_edge(*edge[:3])
                break
        else:
            raise ValueError(f"Player '{player_id}' does not hold object '{object_id}'.")
        room_id = self.get_player_room(player_id)
        self.graph.add_edge(object_id, room_id, type='located_in')
        return(f"Player '{player_id}' dropped object '{object_id}' in room '{room_id}'.")
    @tool_response
    def get_player_room(self, player_id):
        for edge in self.graph.edges(player_id, data=True):
            if edge[2]['type'] == 'located_in':
                return edge[1]
        return 'None'
    @tool_response
    def get_object_location(self, object_id):
        for edge in self.graph.edges(object_id, data=True):
            if edge[2]['type'] == 'located_in':
                return edge[1]
        return 'None'
    @tool_response
    def get_room_players(self, room_id):
        players = []
        for edge in self.graph.in_edges(room_id, data=True):
            if edge[2]['type'] == 'located_in':
                node = edge[0]
                if self.graph.nodes[node]['type'] == 'player':
                    players.append(node)
        return ','.join(players)
    @tool_response
    def get_room_npcs(self, room_id):
        npcs = []
        for edge in self.graph.in_edges(room_id, data=True):
            if edge[2]['type'] == 'located_in':
                node = edge[0]
                if self.graph.nodes[node]['type'] == 'npc':
                    npcs.append(node)
        return ','.join(npcs)
    @tool_response
    def get_player_objects(self, player_id):
        objects = []
        for edge in self.graph.edges(player_id, data=True):
            if edge[2]['type'] == 'holds':
                objects.append(edge[1])
        return ','.join(objects)
    @tool_response
    def get_room_objects(self, room_id):
        objects = []
        for edge in self.graph.in_edges(room_id, data=True):
            if edge[2]['type'] == 'located_in':
                node = edge[0]
                if self.graph.nodes[node]['type'] == 'object':
                    objects.append(node)
        return ','.join(objects)
    @tool_response
    def get_room_description(self, room_id):
        if self.graph.has_node(room_id):
            return self.graph.nodes[room_id].get('description', 'None')
        return 'None'
    @tool_response
    def get_player_name(self, player_id):
        return self.graph.nodes[player_id].get('name', '')
    @tool_response
    def get_npc_name(self, npc_id):
        return self.graph.nodes[npc_id].get('name', '')
    @tool_response
    def get_object_name(self, object_id):
        return self.graph.nodes[object_id].get('name', '')
    @tool_response
    def get_room_exits(self, room_id):
        exits = {}
        for edge in self.graph.edges(room_id, data=True):
            if edge[2]['type'] == 'connected_to':
                direction = edge[2]['direction']
                exits[direction] = edge[1]
        return exits
    @tool_response
    def move_player_direction(self, player_id, direction):
        current_room = self.get_player_room(player_id)
        exits = self.get_room_exits(current_room)
        if direction in exits:
            self.move_player(player_id, exits[direction])
            return True
        else:
            print(f"No exit in direction '{direction}' from room '{current_room}'.")
            return False    
    @tool_response
    def roll_dice(self, num_dice=1, num_sides=20):
        rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
        total = sum(rolls)
        result = f"Rolled {total} ({num_dice}d{num_sides})"
        if num_dice > 1:
            result += f" [rolls: {', '.join(map(str, rolls))}]"
        return result