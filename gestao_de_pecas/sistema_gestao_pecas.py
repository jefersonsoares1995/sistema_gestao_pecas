import os
from colorama import init, Fore, Style
init(autoreset=True)

"""
Sistema de Gestão de Peças Industriais
Este programa auxilia no controle de produção e qualidade de peças fabricadas em linha de montagem.
"""

# Constantes para validação
PESO_MINIMO = 95
PESO_MAXIMO = 105
CORES_VALIDAS = ['azul', 'verde']
COMPRIMENTO_MINIMO = 10
COMPRIMENTO_MAXIMO = 20
CAPACIDADE_MAXIMA_CAIXA = 10

# Estruturas de dados globais
pecas = {}  # Dicionário de peças: {id: {atributos}}
caixas = []  # Lista de caixas: [{atributos}]

def limpar_tela():
    """Limpa o terminal de forma compatível com Windows e Linux/macOS."""
    os.system('cls' if os.name == 'nt' else 'clear')


def validar_peca(peso, cor, comprimento):
    """Valida se a peça atende aos critérios de qualidade."""
    peso_valido = PESO_MINIMO <= peso <= PESO_MAXIMO
    cor_valida = cor.lower() in CORES_VALIDAS
    comprimento_valido = COMPRIMENTO_MINIMO <= comprimento <= COMPRIMENTO_MAXIMO
    
    return peso_valido and cor_valida and comprimento_valido


def obter_motivo_reprovacao(peso, cor, comprimento):
    """Obtém o motivo da reprovação da peça."""
    motivos = []
    
    if not (PESO_MINIMO <= peso <= PESO_MAXIMO):
        motivos.append(f"Peso fora do padrão ({peso}g)")
    
    if cor.lower() not in CORES_VALIDAS:
        motivos.append(f"Cor inválida ({cor})")
    
    if not (COMPRIMENTO_MINIMO <= comprimento <= COMPRIMENTO_MAXIMO):
        motivos.append(f"Comprimento fora do padrão ({comprimento}cm)")
    
    return ", ".join(motivos)


def criar_nova_caixa():
    """Cria uma nova caixa e a adiciona à lista de caixas."""
    numero = len(caixas) + 1
    nova_caixa = {
        'numero': numero,
        'pecas': [],
        'fechada': False
    }
    caixas.append(nova_caixa)
    return nova_caixa


def adicionar_peca_a_caixa(peca_id):
    """Adiciona uma peça aprovada a uma caixa disponível."""
    # Verifica se a peça existe e está aprovada
    if peca_id not in pecas or not pecas[peca_id]['aprovada']:
        return False
    
    # Verifica se há uma caixa aberta
    if not caixas or caixas[-1]['fechada']:
        criar_nova_caixa()
    
    caixa_atual = caixas[-1]
    
    # Adiciona a peça à caixa
    caixa_atual['pecas'].append(peca_id)
    
    # Verifica se a caixa atingiu a capacidade máxima
    if len(caixa_atual['pecas']) >= CAPACIDADE_MAXIMA_CAIXA:
        caixa_atual['fechada'] = True
    
    return True


def cadastrar_peca(id_peca, peso, cor, comprimento):
    """Cadastra uma nova peça no sistema."""
    # Verifica se já existe uma peça com o mesmo ID
    if id_peca in pecas:
        return False, f"Já existe uma peça com o ID {id_peca}"
    
    # Valida a peça
    aprovada = validar_peca(peso, cor, comprimento)
    
    # Cria a nova peça
    nova_peca = {
        'id': id_peca,
        'peso': peso,
        'cor': cor,
        'comprimento': comprimento,
        'aprovada': aprovada,
        'motivo_reprovacao': None if aprovada else obter_motivo_reprovacao(peso, cor, comprimento)
    }
    
    # Adiciona a peça ao dicionário
    pecas[id_peca] = nova_peca
    
    # Se a peça for aprovada, tenta adicioná-la a uma caixa
    if aprovada:
        adicionar_peca_a_caixa(id_peca)
    
    status = "aprovada" if aprovada else "reprovada"
    return True, f"Peça {id_peca} cadastrada com sucesso e {status}"


def remover_peca(id_peca):
    """Remove uma peça do sistema."""
    if id_peca not in pecas:
        return False, f"Não existe peça com o ID {id_peca}"
    
    peca = pecas[id_peca]
    
    # Se a peça estiver em alguma caixa, precisa removê-la
    if peca['aprovada']:
        for caixa in caixas:
            if id_peca in caixa['pecas'] and not caixa['fechada']:
                caixa['pecas'].remove(id_peca)
                break
    
    # Remove a peça do dicionário
    del pecas[id_peca]
    
    return True, f"Peça {id_peca} removida com sucesso"


def listar_pecas(filtro=None):
    """Lista as peças cadastradas, com opção de filtro."""
    resultado = []
    
    for id_peca, peca in pecas.items():
        if filtro == "aprovadas" and peca['aprovada']:
            resultado.append(id_peca)
        elif filtro == "reprovadas" and not peca['aprovada']:
            resultado.append(id_peca)
        elif filtro is None:
            resultado.append(id_peca)
    
    return resultado


def formatar_peca(id_peca):
    """Formata as informações de uma peça para exibição."""
    peca = pecas[id_peca]

    # Define cores de status
    if peca["aprovada"]:
        status_texto = f"{Fore.GREEN}APROVADA{Style.RESET_ALL}"
    else:
        status_texto = f"{Fore.RED}REPROVADA{Style.RESET_ALL}"

    # Função auxiliar para formatar campos
    def campo(rotulo, valor, cor=Fore.CYAN):
        return f"{cor}{rotulo}:{Style.RESET_ALL} {valor}"

    # Monta a linha de informações básicas
    partes = [
        campo("ID", peca["id"]),
        campo("Peso", f"{peca['peso']}g"),
        campo("Cor", peca["cor"]),
        campo("Comprimento", f"{peca['comprimento']}cm"),
        campo("Status", status_texto),
    ]

    info = " | ".join(partes)

    # Adiciona motivo de reprovação, se houver
    if not peca["aprovada"]:
        info += f" | {Fore.YELLOW}Motivo:{Style.RESET_ALL} {peca['motivo_reprovacao']}"
        
    return info


def listar_caixas_fechadas():
    """Lista as caixas fechadas."""
    return [caixa for caixa in caixas if caixa['fechada']]


def formatar_caixa(caixa):
    """Formata as informações de uma caixa para exibição."""
    status = "FECHADA" if caixa['fechada'] else "ABERTA"
    return f"Caixa #{caixa['numero']} | Status: {status} | Peças: {len(caixa['pecas'])}/{CAPACIDADE_MAXIMA_CAIXA}"


def gerar_relatorio():
    """Gera um relatório consolidado do sistema."""
    pecas_aprovadas = [p for p in pecas.values() if p['aprovada']]
    pecas_reprovadas = [p for p in pecas.values() if not p['aprovada']]
    
    # Contagem de motivos de reprovação
    motivos = {}
    for peca in pecas_reprovadas:
        for motivo in peca['motivo_reprovacao'].split(", "):
            motivos[motivo] = motivos.get(motivo, 0) + 1
    
    # Caixas utilizadas (fechadas + a atual se tiver peças)
    caixas_fechadas = len(listar_caixas_fechadas())
    caixas_utilizadas = caixas_fechadas
    if caixas and not caixas[-1]['fechada'] and len(caixas[-1]['pecas']) > 0:
        caixas_utilizadas += 1
    
    return {
        "total_pecas": len(pecas),
        "pecas_aprovadas": len(pecas_aprovadas),
        "pecas_reprovadas": len(pecas_reprovadas),
        "motivos_reprovacao": motivos,
        "caixas_utilizadas": caixas_utilizadas,
        "caixas_fechadas": caixas_fechadas
    }


def exibir_menu():
    """Exibe o menu de opções do sistema."""
    print(f"{Fore.BLUE}{"\n" + "=" * 50}")
    print("SISTEMA DE GESTÃO DE PEÇAS INDUSTRIAIS")
    print(f"{Fore.BLUE}{"=" * 50}")
    print(f"{Fore.GREEN}1.{Style.RESET_ALL} Cadastrar nova peça")
    print(f"{Fore.GREEN}2.{Style.RESET_ALL} Listar peças aprovadas/reprovadas")
    print(f"{Fore.GREEN}3.{Style.RESET_ALL} Remover peça cadastrada")
    print(f"{Fore.GREEN}4.{Style.RESET_ALL} Listar caixas fechadas")
    print(f"{Fore.GREEN}5.{Style.RESET_ALL} Gerar relatório final")
    print(f"{Fore.RED}0.{Style.RESET_ALL} Sair ❌")
    print(f"{Fore.BLUE}{"=" * 50}")


def main():
    """Função principal que executa o sistema."""
    if not caixas:
        criar_nova_caixa()
    
    while True:
        limpar_tela()  # limpa antes de mostrar o menu
        exibir_menu()
        
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida! Por favor, digite um número.")
            input("\nPressione Enter para continuar...")
            continue
        
        limpar_tela()  # 👉 limpa antes de executar a ação escolhida
        
        if opcao == 0:
            print("Encerrando o sistema...")
            break
        
        elif opcao == 1:
            print("\n--- CADASTRO DE NOVA PEÇA ---")
            id_peca = input("ID da peça: ")
            
            try:
                peso = float(input("Peso (g): "))
                cor = input("Cor (azul/verde): ")
                comprimento = float(input("Comprimento (cm): "))
                
                sucesso, mensagem = cadastrar_peca(id_peca, peso, cor, comprimento)
                print(mensagem)
            except ValueError:
                print("Erro: Os valores de peso e comprimento devem ser números.")
        
        elif opcao == 2:
            print("\n--- LISTAGEM DE PEÇAS ---")
            print("1. Listar todas as peças")
            print("2. Listar peças aprovadas")
            print("3. Listar peças reprovadas")
            
            try:
                sub_opcao = int(input("Escolha uma opção: "))
                
                if sub_opcao == 1:
                    ids_pecas = listar_pecas()
                    filtro = "todas"
                elif sub_opcao == 2:
                    ids_pecas = listar_pecas("aprovadas")
                    filtro = "aprovadas"
                elif sub_opcao == 3:
                    ids_pecas = listar_pecas("reprovadas")
                    filtro = "reprovadas"
                else:
                    print("Opção inválida!")
                    continue
                
                if not ids_pecas:
                    print(f"Não há peças {filtro} cadastradas.")
                else:
                    print(f"\nListagem de peças {filtro}:")
                    for id_peca in ids_pecas:
                        print(formatar_peca(id_peca))
            except ValueError:
                print("Opção inválida! Por favor, digite um número.")
        
        elif opcao == 3:
            print("\n--- REMOÇÃO DE PEÇA ---")
            id_peca = input("ID da peça a ser removida: ")
            
            sucesso, mensagem = remover_peca(id_peca)
            print(mensagem)
        
        elif opcao == 4:
            print("\n--- LISTAGEM DE CAIXAS FECHADAS ---")
            caixas_fechadas = listar_caixas_fechadas()
            
            if not caixas_fechadas:
                print("Não há caixas fechadas.")
            else:
                print(f"Total de caixas fechadas: {len(caixas_fechadas)}")
                for caixa in caixas_fechadas:
                    print(formatar_caixa(caixa))
                    print(f"  Peças na caixa:")
                    for id_peca in caixa['pecas']:
                        print(f"  - {formatar_peca(id_peca)}")
        
        elif opcao == 5:
            print("\n--- RELATÓRIO FINAL ---")
            relatorio = gerar_relatorio()
            
            print(f"{Fore.CYAN}Total de peças cadastradas: {Style.RESET_ALL} {relatorio['total_pecas']}")
            print(f"{Fore.GREEN}Total de peças aprovadas: {Style.RESET_ALL} {relatorio['pecas_aprovadas']}")
            print(f"{Fore.RED}Total de peças reprovadas: {Style.RESET_ALL} {relatorio['pecas_reprovadas']}")
            
            if relatorio['motivos_reprovacao']:
                print(f"{Fore.YELLOW}Motivos de reprovação:{Style.RESET_ALL}")
                for motivo, quantidade in relatorio['motivos_reprovacao'].items():
                    print(f"  - {motivo}: {quantidade} peça(s)")
            
            print(f"{Fore.MAGENTA}📦 Caixas utilizadas: {Style.RESET_ALL} {relatorio['caixas_utilizadas']}")
            print(f"{Fore.MAGENTA}📦 Caixas fechadas: {Style.RESET_ALL} {relatorio['caixas_fechadas']}")
        
        else:
            print("Opção inválida! Por favor, escolha uma opção válida.")
        
        input("\nPressione Enter para continuar...")


if __name__ == "__main__":
    main()