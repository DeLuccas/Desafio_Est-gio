import click
import task_operations as player_ops

@click.group()
def cli():
    """Gerenciador de Jogadores de Futebol CLI"""
    pass

@cli.command("add-player") 
@click.option('--name', prompt='Nome do jogador', help='O nome do jogador.')
@click.option('--team', prompt='Time atual', help='O time atual do jogador.')
@click.option('--position', prompt='Posição', help='A posição em que o jogador atua.')
@click.option('--goals', prompt='Gols marcados', type=int, help='Número de gols marcados pelo jogador.')
def add_player_command(name, team, position, goals):
    """Adiciona um novo jogador ao elenco."""
    player = player_ops.add_player(name, team, position, goals)
    if player:
        click.echo(click.style(f"Jogador '{name}' (ID: {player['id']}) adicionado com sucesso ao time {team}!", fg='green'))
    else:
        click.echo(click.style("Erro ao adicionar jogador.", fg='red'))

@cli.command("list-players") 
@click.option('--team', help='Filtrar jogadores por time.')
@click.option('--position', help='Filtrar jogadores por posição.')
def list_players_command(team, position):
    """Lista os jogadores cadastrados."""
    players = player_ops.list_all_players()
    if not players:
        click.echo(click.style("Nenhum jogador encontrado no sistema.", fg='yellow'))
        return

    # Filtros
    filtered_players = players
    if team:
        filtered_players = [p for p in filtered_players if p.get('team', '').lower() == team.lower()]
    if position:
        filtered_players = [p for p in filtered_players if p.get('position', '').lower() == position.lower()]

    if not filtered_players:
        click.echo(click.style("Nenhum jogador encontrado com os filtros aplicados.", fg='yellow'))
        return

    click.echo(click.style("\n--- LISTA DE JOGADORES ---", bold=True, fg='blue'))
    for p in filtered_players:
        id_color = 'cyan'
        name_color = 'white'
        team_color = 'magenta'
        position_color = 'yellow'
        goals_color = 'green'

        click.echo(
            f"{click.style('ID:', fg=id_color)} {p['id']} | "
            f"{click.style('Nome:', fg=name_color)} {p['name']} | "
            f"{click.style('Time:', fg=team_color)} {p['team']} | "
            f"{click.style('Posição:', fg=position_color)} {p['position']} | "
            f"{click.style('Gols:', fg=goals_color)} {p.get('goals', 0)}"
        )
    click.echo(click.style("------------------------\n", bold=True, fg='blue'))

@cli.command("update-player")
@click.argument('player_id', type=int)
@click.option('--name', help='O novo nome do jogador.')
@click.option('--team', help='O novo time do jogador.')
@click.option('--position', help='A nova posição do jogador.')
@click.option('--goals', type=int, help='O novo número de gols do jogador.')
def update_player_command(player_id, name, team, position, goals):
    """Atualiza os dados de um jogador existente."""
    if name is None and team is None and position is None and goals is None:
        ctx = click.get_current_context()
        click.echo("Nenhum dado fornecido para atualização. Forneça ao menos uma opção.")
        click.echo(ctx.get_help())
        ctx.exit()

    player = player_ops.find_player_by_id(player_id)
    if not player:
        click.echo(click.style(f"Jogador com ID {player_id} não encontrado.", fg='red'))
        return

    updated_player = player_ops.update_player_details(player_id, name, team, position, goals)
    if updated_player:
        click.echo(click.style(f"Dados do jogador ID {player_id} atualizados com sucesso!", fg='green'))
        # Mostra quais campos foram alterados
        if name is not None:
            click.echo(f"  Nome alterado para: {updated_player['name']}")
        if team is not None:
            click.echo(f"  Time alterado para: {updated_player['team']}")
        if position is not None:
            click.echo(f"  Posição alterada para: {updated_player['position']}")
        if goals is not None:
            click.echo(f"  Gols alterados para: {updated_player['goals']}")
    else:
        click.echo(click.style(f"Erro ao atualizar jogador {player_id}.", fg='red'))

@cli.command("remove-player") # Renomeado de delete
@click.argument('player_id', type=int)
def remove_player_command(player_id):
    """Remove um jogador do sistema."""
    player = player_ops.find_player_by_id(player_id)
    if not player:
        click.echo(click.style(f"Jogador com ID {player_id} não encontrado.", fg='red'))
        return

    if player_ops.delete_player_by_id(player_id):
        click.echo(click.style(f"Jogador {player_id} ('{player['name']}') removido com sucesso!", fg='green'))
    else:
        click.echo(click.style(f"Erro ao remover jogador {player_id}.", fg='red'))


if __name__ == '__main__':
    cli() 