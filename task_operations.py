import json
import os
from typing import List, Dict, Any, Optional

PLAYERS_FILE = "players.json"

def load_players() -> List[Dict[str, Any]]:
    """Carrega os jogadores do arquivo JSON."""
    if not os.path.exists(PLAYERS_FILE):
        return []
    try:
        with open(PLAYERS_FILE, 'r', encoding='utf-8') as f:
            players = json.load(f)
        
        for player in players:
            if 'goals' not in player:
                player['goals'] = 0 
        return players
    except json.JSONDecodeError:
        print(f"Aviso: O arquivo {PLAYERS_FILE} está vazio ou malformado. Iniciando com lista vazia.")
        return []
    except Exception as e:
        print(f"Erro inesperado ao carregar jogadores: {e}")
        return []

def save_players(players: List[Dict[str, Any]]) -> None:
    """Salva os jogadores no arquivo JSON."""
    try:
        with open(PLAYERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(players, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Erro inesperado ao salvar jogadores: {e}")

def get_next_id(items: List[Dict[str, Any]]) -> int:
    """Gera o próximo ID sequencial para um novo item."""
    if not items:
        return 1
    return max(item.get('id', 0) for item in items) + 1

def add_player(name: str, team: str, position: str, goals: int) -> Optional[Dict[str, Any]]:
    """Adiciona um novo jogador."""
    players = load_players()
    new_id = get_next_id(players)
    new_player = {
        "id": new_id,
        "name": name,
        "team": team,
        "position": position,
        "goals": goals
    }
    players.append(new_player)
    save_players(players)
    return new_player

def list_all_players() -> List[Dict[str, Any]]:
    """Retorna todos os jogadores."""
    return load_players()

def find_player_by_id(player_id: int) -> Optional[Dict[str, Any]]:
    """Encontra um jogador pelo seu ID."""
    players = load_players()
    for player in players:
        if player.get('id') == player_id:
            return player
    return None

def update_player_details(player_id: int, name: Optional[str] = None, team: Optional[str] = None, position: Optional[str] = None, goals: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Atualiza nome, time, posição e/ou gols de um jogador."""
    players = load_players()
    player_updated = False
    updated_player_data = None
    for player in players:
        if player.get('id') == player_id:
            if name is not None:
                player['name'] = name
            if team is not None:
                player['team'] = team
            if position is not None:
                player['position'] = position
            if goals is not None: 
                player['goals'] = goals
            player_updated = True
            updated_player_data = player
            break
    if player_updated:
        save_players(players)
        return updated_player_data
    return None

def delete_player_by_id(player_id: int) -> bool:
    """Exclui um jogador pelo seu ID."""
    players = load_players()
    initial_len = len(players)
    players = [player for player in players if player.get('id') != player_id]
    if len(players) < initial_len:
        save_players(players)
        return True
    return False 