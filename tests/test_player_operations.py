import pytest
import json
import os
from typing import List, Dict, Any
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import task_operations as player_ops

TEST_PLAYERS_FILE = "test_players.json" 
ORIGINAL_PLAYERS_FILE = player_ops.PLAYERS_FILE

@pytest.fixture(autouse=True)
def setup_and_teardown():
    player_ops.PLAYERS_FILE = TEST_PLAYERS_FILE
    if os.path.exists(TEST_PLAYERS_FILE):
        os.remove(TEST_PLAYERS_FILE)
    yield
    if os.path.exists(TEST_PLAYERS_FILE):
        os.remove(TEST_PLAYERS_FILE)
    player_ops.PLAYERS_FILE = ORIGINAL_PLAYERS_FILE

def test_load_players_no_file():
    """Testa carregar jogadores quando o arquivo não existe."""
    assert player_ops.load_players() == []

def test_load_players_empty_or_malformed_file():
    """Testa carregar jogadores de um arquivo JSON vazio ou malformado."""
    with open(TEST_PLAYERS_FILE, 'w', encoding='utf-8') as f:
        f.write("[]")
    assert player_ops.load_players() == []
    
    if os.path.exists(TEST_PLAYERS_FILE):
        os.remove(TEST_PLAYERS_FILE)
    with open(TEST_PLAYERS_FILE, 'w', encoding='utf-8') as f:
        f.write("") # Arquivo vazio
    assert player_ops.load_players() == []

    if os.path.exists(TEST_PLAYERS_FILE):
        os.remove(TEST_PLAYERS_FILE)
    with open(TEST_PLAYERS_FILE, 'w', encoding='utf-8') as f:
        f.write("invalid json") # JSON malformado
    assert player_ops.load_players() == []

def test_save_and_load_players():
    """Testa salvar e carregar jogadores."""
    players_to_save = [
        {"id": 1, "name": "Test Player 1", "team": "Test Team FC", "position": "Atacante", "goals": 10}
    ]
    player_ops.save_players(players_to_save)
    loaded_players = player_ops.load_players()
    assert loaded_players == players_to_save

def test_get_next_id():
    """Testa a geração do próximo ID."""
    assert player_ops.get_next_id([]) == 1
    assert player_ops.get_next_id([{"id": 1}, {"id": 2}]) == 3
    assert player_ops.get_next_id([{"id": 5}]) == 6
    assert player_ops.get_next_id([{"id": 1, "name": "p1"}, {"id": 0, "name":"p0"}]) == 2

def test_add_player():
    """Testa adicionar um novo jogador."""
    player_ops.save_players([]) # Garante que começamos do zero
    player1 = player_ops.add_player("New Player 1", "Team A", "Meio-campo", 5)
    assert player1 is not None
    assert player1['id'] == 1
    assert player1['name'] == "New Player 1"
    assert player1['team'] == "Team A"
    assert player1['position'] == "Meio-campo"
    assert player1['goals'] == 5

    loaded_players = player_ops.load_players()
    assert len(loaded_players) == 1
    assert loaded_players[0] == player1

    player2 = player_ops.add_player("New Player 2", "Team B", "Defensor", 0)
    assert player2 is not None
    assert player2['id'] == 2
    loaded_players = player_ops.load_players()
    assert len(loaded_players) == 2

def test_list_all_players():
    """Testa listar todos os jogadores."""
    initial_players = [
        {"id": 1, "name": "P1", "team": "T1", "position": "ATK", "goals": 100},
        {"id": 2, "name": "P2", "team": "T2", "position": "DEF", "goals": 10}
    ]
    player_ops.save_players(initial_players)
    assert player_ops.list_all_players() == initial_players

def test_find_player_by_id():
    """Testa encontrar um jogador pelo ID."""
    players = [
        {"id": 1, "name": "Find Me", "team": "Seekers FC", "position": "Goleiro", "goals": 0},
        {"id": 2, "name": "Another Player", "team": "Others United", "position": "Lateral", "goals": 2}
    ]
    player_ops.save_players(players)
    
    found_player = player_ops.find_player_by_id(1)
    assert found_player is not None
    assert found_player['name'] == "Find Me"
    
    not_found_player = player_ops.find_player_by_id(3)
    assert not_found_player is None

def test_update_player_details():
    """Testa atualizar detalhes de um jogador (nome, time, posição, gols)."""
    player_ops.add_player("Original Name", "Original Team", "Original Pos", 10) # ID será 1

    # Atualiza nome
    updated_p = player_ops.update_player_details(1, name="New Name")
    assert updated_p is not None
    assert updated_p['name'] == "New Name"
    assert updated_p['team'] == "Original Team" 
    assert updated_p['goals'] == 10

    # Atualiza time
    updated_p = player_ops.update_player_details(1, team="New Team FC")
    assert updated_p is not None
    assert updated_p['team'] == "New Team FC"

    # Atualiza posição
    updated_p = player_ops.update_player_details(1, position="Nova Posição")
    assert updated_p is not None
    assert updated_p['position'] == "Nova Posição"

    # Atualiza gols
    updated_p = player_ops.update_player_details(1, goals=15)
    assert updated_p is not None
    assert updated_p['goals'] == 15

    # Atualiza múltiplos campos
    updated_p = player_ops.update_player_details(1, name="Final Name", team="Ultimate Team", goals=20)
    assert updated_p is not None
    assert updated_p['name'] == "Final Name"
    assert updated_p['team'] == "Ultimate Team"
    assert updated_p['goals'] == 20

    # Verifica se foi salvo
    loaded_player = player_ops.find_player_by_id(1)
    assert loaded_player['name'] == "Final Name"
    assert loaded_player['team'] == "Ultimate Team"
    assert loaded_player['goals'] == 20

    # Testa com ID inexistente
    non_existent_update = player_ops.update_player_details(99, name="No Chance")
    assert non_existent_update is None

def test_delete_player_by_id():
    """Testa excluir um jogador."""
    player_ops.add_player("To Delete", "Adios FC", "Zagueiro", 1) # ID 1
    player_ops.add_player("To Keep", "Stayers United", "Volante", 3)   # ID 2
    
    assert player_ops.delete_player_by_id(1) is True
    assert player_ops.find_player_by_id(1) is None
    
    remaining_player = player_ops.find_player_by_id(2)
    assert remaining_player is not None
    assert len(player_ops.load_players()) == 1
    
    assert player_ops.delete_player_by_id(99) is False
    assert len(player_ops.load_players()) == 1

def test_id_persistence_and_sequence_players():
    """Testa a persistência e sequência dos IDs dos jogadores."""
    player_ops.save_players([]) 
    
    p1 = player_ops.add_player("P1", "T1", "A", 1)
    assert p1['id'] == 1
    
    p2 = player_ops.add_player("P2", "T2", "B", 2)
    assert p2['id'] == 2
    
    player_ops.delete_player_by_id(1)
    
    p3 = player_ops.add_player("P3", "T3", "C", 3)
    assert p3['id'] == 3
    
    players = player_ops.load_players()
    ids = [p['id'] for p in players]
    assert ids == [2, 3]

    player_ops.save_players([{"id": 10, "name": "High ID Player", "team": "Top Team", "position": "FWD", "goals": 100}])
    player_after_high_id = player_ops.add_player("After High", "New Team", "MID", 5)
    assert player_after_high_id['id'] == 11

def test_load_players_ensures_goals_field():
    """Testa se load_players adiciona 'goals': 0 se o campo estiver faltando."""
    # Salva um jogador sem o campo 'goals'
    players_without_goals = [
        {"id": 1, "name": "No Goals Player", "team": "Test Team", "position": "Unknown"}
    ]
    with open(TEST_PLAYERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(players_without_goals, f, indent=2)
    
    loaded_players = player_ops.load_players()
    assert len(loaded_players) == 1
    assert loaded_players[0]['name'] == "No Goals Player"
    assert 'goals' in loaded_players[0]
    assert loaded_players[0]['goals'] == 0

    # Testa com um jogador que já tem gols
    players_with_goals = [
        {"id": 2, "name": "Goals Player", "team": "Test Team", "position": "Striker", "goals": 50}
    ]
    with open(TEST_PLAYERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(players_with_goals, f, indent=2)

    loaded_players = player_ops.load_players()
    assert len(loaded_players) == 1
    assert loaded_players[0]['name'] == "Goals Player"
    assert loaded_players[0]['goals'] == 50 