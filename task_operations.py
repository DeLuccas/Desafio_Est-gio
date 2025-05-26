import json
import os
from typing import List, Dict, Any, Optional

ARQUIVO_JOGADORES = "players.json"

def carregar_jogadores() -> List[Dict[str, Any]]:
    if not os.path.isfile(ARQUIVO_JOGADORES):
        return []

    try:
        with open(ARQUIVO_JOGADORES, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        [j.setdefault("goals", 0) for j in dados]

        return dados

    except (json.JSONDecodeError, ValueError):
        print(f"Atenção: o arquivo {ARQUIVO_JOGADORES} está corrompido ou vazio.")
    except Exception as erro:
        print(f"Erro ao tentar ler os dados: {erro}")
    
    return []

def salvar_jogadores(lista: List[Dict[str, Any]]) -> None:
    try:
        with open(ARQUIVO_JOGADORES, "w", encoding="utf-8") as arquivo:
            json.dump(lista, arquivo, indent=2, ensure_ascii=False)
    except Exception as erro:
        print(f"Erro ao salvar dados dos jogadores: {erro}")

def proximo_id(lista: List[Dict[str, Any]]) -> int:
    return max((j.get("id", 0) for j in lista), default=0) + 1

def adicionar_jogador(nome: str, time: str, posicao: str, gols: int) -> Optional[Dict[str, Any]]:
    jogadores = carregar_jogadores()
    novo_jogador = {
        "id": proximo_id(jogadores),
        "name": nome,
        "team": time,
        "position": posicao,
        "goals": gols
    }
    jogadores.append(novo_jogador)
    salvar_jogadores(jogadores)
    return novo_jogador

def listar_jogadores() -> List[Dict[str, Any]]:
    return carregar_jogadores()

def buscar_jogador_por_id(identificador: int) -> Optional[Dict[str, Any]]:
    return next((j for j in carregar_jogadores() if j.get("id") == identificador), None)

def atualizar_jogador(
    identificador: int,
    nome: Optional[str] = None,
    time: Optional[str] = None,
    posicao: Optional[str] = None,
    gols: Optional[int] = None
) -> Optional[Dict[str, Any]]:
    
    jogadores = carregar_jogadores()

    for j in jogadores:
        if j.get("id") != identificador:
            continue

        j.update({
            "name": nome or j["name"],
            "team": time or j["team"],
            "position": posicao or j["position"],
            "goals": gols if gols is not None else j["goals"]
        })

        salvar_jogadores(jogadores)
        return j

    return None

def remover_jogador(identificador: int) -> bool:
    jogadores = carregar_jogadores()
    nova_lista = [j for j in jogadores if j.get("id") != identificador]

    if len(nova_lista) != len(jogadores):
        salvar_jogadores(nova_lista)
        return True

    return False