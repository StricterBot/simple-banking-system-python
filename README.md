# Sistema Bancário em Python
[![Santander Bootcamp 2025](https://img.shields.io/badge/Santander%20Bootcamp%202025-DIO.me-red?style=for-the-badge)](https://www.dio.me/)

## Sobre o projeto

Este projeto é a versão 1 (MVP) de um sistema bancário desenvolvido em Python, como parte de um desafio prático do bootcamp de back-end.
O sistema executa as operações básicas de uma conta bancária: **depósito, saque e extrato**, com controle de limites e histórico de transações.

---

## Desafio

- Criar um sistema bancário com:
    - Depósito
    - Saque (máximo de 3 por dia, até R$500 cada)
    - Visualização de extrato (histórico completo)
- **Versão 1**: Apenas um usuário. Não é necessário agência ou número de conta.
- **Exigência**: Todas as movimentações devem ser listadas no extrato.

---

<h5 align="right">
<span> Este desafio foi proposto no bootcamp Santander 2025 - Back-End com Python oferecido pela DIO.me</span>
<a href="https://www.dio.me/">
<img align="center" width="40px" src="https://hermes.digitalinnovation.one/assets/diome/logo-minimized.png"></a>
</h5>

---

## Tecnologias Utilizadas

[![Python](https://custom-icon-badges.demolab.com/badge/-Python-3776AB?logo=python&logoColor=white&style=flat-square)](https://python.org/)
[![Visual Studio Code](https://custom-icon-badges.demolab.com/badge/-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white&style=flat-square)](https://code.visualstudio.com/)

---

## Como Usar

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/StricterBot/python-banking-cli.git
    cd python-banking-cli
    ```

2. **Execute o programa:**
    - Certifique-se de ter o Python 3+ instalado.
    - No terminal, rode:
        ```bash
        python banksys.py
        ```

3. **Siga o menu interativo:**
    - Digite `1` para depositar.
    - Digite `2` para sacar.
    - Digite `3` para visualizar o extrato.
    - Digite `4` para sair.

---

## Documentação e Acessibilidade

- O sistema apresenta mensagens claras e separadores visuais para facilitar o entendimento do usuário.
- Todas as mensagens podem ser exibidas em **português ou inglês**.  
  Basta ajustar a variável `LANG` no início do código para `"PT"` ou `"EN"`.
- As operações exibem feedback imediato, incluindo saldo atualizado após cada movimentação.

---

> [!IMPORTANT] 
> **Por que os valores estão em R$?**  
> O projeto foi idealizado e entregue em contexto brasileiro, seguindo o desafio original proposto no bootcamp.  
> O uso do símbolo R$ (Real brasileiro) mantém a fidelidade ao cenário do exercício e reforça o entendimento de limites, regras e práticas locais.

---

## O que você vai encontrar na minha versão

- **Histórico real de todas as operações, com data e hora.**
- **Mensagens internacionais (PT/EN)**, fácil de alterar.
- **Boas práticas de código Python**: clareza, nomes intuitivos, tratamento de erros de entrada.
- **Experiência de usuário com feedback visual** após cada operação.

---
### Sobre mim:
[![LinkedIn](https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?logo=linkedin-white&logoColor=fff)](https://www.linkedin.com/in/victor-moreira-4210b9358/)
[![GitHub](https://custom-icon-badges.demolab.com/badge/GitHub-181717?logo=github&logoColor=fff)](https://github.com/StricterBot)
