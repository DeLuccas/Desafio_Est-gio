import click
import task_operations as jogador_ops

@click.group()
def cli():
    """Ferramenta de linha de comando para gerenciar jogadores."""
    pass

@cli.command("add-player")
@click.option('--name', prompt='Nome do jogador', help='Informe o nome do jogador.')
@click.option('--team', prompt='Time', help='Informe o time atual do jogador.')
@click.option('--position', prompt='Posição', help='Posição em que o jogador atua.')
@click.option('--goals', prompt='Gols marcados', type=int, help='Total de gols que o jogador marcou.')
def adicionar_jogador(name, team, position, goals):
    """Cadastra um novo jogador."""
    novo = jogador_ops.adicionar_jogador(name, team, position, goals)
    if novo:
        click.echo(click.style(f"✅ Jogador '{name}' (ID: {novo['id']}) cadastrado com sucesso!", fg='green'))
    else:
        click.echo(click.style("❌ Erro ao adicionar jogador.", fg='red'))

@cli.command("list-players")
@click.option('--team', help='Filtrar por time.')
@click.option('--position', help='Filtrar por posição.')
def listar_jogadores(team, position):
    """Exibe a lista de jogadores salvos."""
    jogadores = jogador_ops.listar_jogadores()

    if not jogadores:
        click.echo(click.style("Nenhum jogador cadastrado ainda.", fg='yellow'))
        return

    filtrados = jogadores
    if team:
        filtrados = [j for j in filtrados if j.get("team", "").lower() == team.lower()]
    if position:
        filtrados = [j for j in filtrados if j.get("position", "").lower() == position.lower()]

    if not filtrados:
        click.echo(click.style("Nenhum jogador encontrado com os filtros aplicados.", fg='yellow'))
        return

    click.echo(click.style("\nJogadores Encontrados:", bold=True, fg='blue'))
    for j in filtrados:
        click.echo(
            f"{click.style('ID:', fg='cyan')} {j['id']} | "
            f"{click.style('Nome:', fg='white')} {j['name']} | "
            f"{click.style('Time:', fg='magenta')} {j['team']} | "
            f"{click.style('Posição:', fg='yellow')} {j['position']} | "
            f"{click.style('Gols:', fg='green')} {j.get('goals', 0)}"
        )

@cli.command("update-player")
@click.argument('player_id', type=int)
@click.option('--name', help='Novo nome do jogador.')
@click.option('--team', help='Novo time do jogador.')
@click.option('--position', help='Nova posição.')
@click.option('--goals', type=int, help='Novo número de gols.')
def atualizar_jogador(player_id, name, team, position, goals):
    """Atualiza os dados de um jogador já existente."""
    if not any([name, team, position, goals]):
        click.echo("⚠️ Nenhuma informação foi fornecida para atualização.")
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()

    jogador = jogador_ops.buscar_jogador_por_id(player_id)
    if not jogador:
        click.echo(click.style(f"Jogador com ID {player_id} não encontrado.", fg='red'))
        return

    atualizado = jogador_ops.atualizar_jogador(player_id, name, team, position, goals)
    if atualizado:
        click.echo(click.style(f"✅ Jogador ID {player_id} atualizado com sucesso!", fg='green'))
        if name: click.echo(f"  ➜ Novo nome: {atualizado['name']}")
        if team: click.echo(f"  ➜ Novo time: {atualizado['team']}")
        if position: click.echo(f"  ➜ Nova posição: {atualizado['position']}")
        if goals is not None: click.echo(f"  ➜ Gols atualizados: {atualizado['goals']}")
    else:
        click.echo(click.style("❌ Não foi possível atualizar o jogador.", fg='red'))

@cli.command("remove-player")
@click.argument('player_id', type=int)
def remover_jogador(player_id):
    """Remove um jogador do sistema."""
    jogador = jogador_ops.buscar_jogador_por_id(player_id)
    if not jogador:
        click.echo(click.style(f"Jogador com ID {player_id} não encontrado.", fg='red'))
        return

    sucesso = jogador_ops.remover_jogador(player_id)
    if sucesso:
        click.echo(click.style(f"✅ Jogador '{jogador['name']}' removido com sucesso.", fg='green'))
    else:
        click.echo(click.style("❌ Ocorreu um erro ao tentar remover o jogador.", fg='red'))

if __name__ == '__main__':
    cli()