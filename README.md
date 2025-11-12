# Sistema de Gestão de Peças Industriais

Este repositório contém o script `sistema_gestao_pecas_v1.py`, um programa de linha de comando para gerenciar peças produzidas em uma linha de montagem, com controle de qualidade e organização em caixas.

## Requisitos

- Python 3.8+
- Biblioteca `colorama`

Instalação da dependência:

```bash
pip install colorama
```

## Como executar

No terminal, dentro desta pasta:

```bash
python sistema_gestao_pecas_v1.py
```

- Windows: recomenda-se usar `cmd` ou PowerShell (a limpeza de tela usa `cls`).
- Linux/macOS: usar um terminal padrão (a limpeza de tela usa `clear`).

## Funcionalidades

- Cadastro de peça com validação de qualidade (peso, cor e comprimento).
- Listagem de peças (todas, aprovadas, reprovadas) com formatação colorida.
- Remoção de peça.
- Organização automática de peças aprovadas em caixas de capacidade máxima 10; fechamento automático ao atingir a capacidade.
- Relatório consolidado com totais e motivos de reprovação.

## Critérios de qualidade

- Peso: entre 95g e 105g
- Cor: apenas `azul` ou `verde`
- Comprimento: entre 10cm e 20cm

Esses limites estão definidos no código como constantes e podem ser ajustados conforme necessário.

## Fluxo pelo menu

Ao iniciar, o sistema apresenta um menu interativo:

- `1` Cadastrar nova peça
- `2` Listar peças (todas/aprovadas/reprovadas)
- `3` Remover peça
- `4` Listar caixas fechadas
- `5` Gerar relatório final
- `0` Sair

## Estrutura de dados

- `pecas`: dicionário de peças indexado por ID, com atributos (peso, cor, comprimento, status).
- `caixas`: lista de caixas, cada uma com número, lista de IDs de peças e status (aberta/fechada).

## Principais funções

- Validação e status:
  - `validar_peca(peso, cor, comprimento)`: verifica os critérios de qualidade.
  - `obter_motivo_reprovacao(...)`: detalha por que a peça foi reprovada.
- Cadastro e remoção:
  - `cadastrar_peca(id_peca, peso, cor, comprimento)`: registra a peça e, se aprovada, envia para uma caixa.
  - `remover_peca(id_peca)`: exclui a peça; se estiver em caixa aberta, remove da caixa.
- Caixas:
  - `criar_nova_caixa()`: inicia uma caixa.
  - `adicionar_peca_a_caixa(peca_id)`: adiciona peças aprovadas na caixa aberta e fecha ao atingir capacidade.
  - `listar_caixas_fechadas()`: retorna caixas encerradas.
  - `formatar_caixa(caixa)`: exibe informação resumida.
- Listagem e relatório:
  - `listar_pecas(filtro)`: retorna IDs conforme filtro.
  - `formatar_peca(id_peca)`: imprime uma linha amigável e colorida.
  - `gerar_relatorio()`: dá visão geral de peças e caixas.
- Interface:
  - `exibir_menu()` e `main()`: controlam a interação via terminal.

## Exemplo de uso

1. Escolha `1` para cadastrar:
   - Informe `ID`, `Peso (g)`, `Cor (azul/verde)`, `Comprimento (cm)`.
   - Se aprovada, a peça será enviada automaticamente para a caixa atual.
2. Use `2` para listar peças e conferir o status.
3. Use `4` para ver caixas fechadas e seu conteúdo.
4. Use `5` para gerar o relatório final.

## Boas práticas e limitações

- Os dados são mantidos somente em memória; ao encerrar o programa, tudo é perdido. Para persistência, seria necessário integrar com arquivo/BD.
- IDs de peça devem ser únicos.
- A limpeza de tela depende do terminal; em alguns ambientes integrados ela pode não funcionar.

## Personalização

- Ajuste os limites de validação (peso, comprimento, cores) alterando as constantes no topo do arquivo.
- Modifique `CAPACIDADE_MAXIMA_CAIXA` para mudar a quantidade por caixa.
