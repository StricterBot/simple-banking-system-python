# Sistema Bancário Simples em Python (CLI)
[![Santander Bootcamp 2025](https://img.shields.io/badge/Santander%20Bootcamp%202025-Backend%20com%20Python-red?style=for-the-badge)](https://www.dio.me/)

## Sobre o projeto

Este projeto é um sistema bancário desenvolvido em Python, como parte de um desafio prático do bootcamp de back-end.

O sistema, executado via terminal (CLI), evoluiu de um script procedural para uma **arquitetura robusta orientada a objetos**. 

Ele simula as operações de um banco, permitindo criar clientes, associar múltiplas contas e realizar transações de **depósito e saque**, com controle de limites e histórico completo por conta.

---

## Desafio

- Criar um sistema bancário com:
    - Depósito
    - Saque (máximo de 3 por dia, até R$500 cada)
    - Visualização de extrato (histórico completo)
- **Versão 1**: Apenas um usuário. Não é necessário agência ou número de conta. Todas as movimentações devem ser listadas no extrato.
- **Versão 2**: Modular todas as operações em funções. Adicionar três novas operações: Cadastrar usuário, criar conta e listar usuários.
- **Versão 2.5**: Reescrita completa do sistema utilizando **Programação Orientada a Objetos**. Criação de classes para todas as entidades (`Cliente`, `Conta`, `Transacao`, etc.), aplicando conceitos como **encapsulamento, herança e polimorfismo** para um código mais robusto, seguro e escalável.
- **Testes de todas as funções foram adicionados apartir da versão 2.**

---

<h5 align="right">
<i><span> Este desafio foi proposto no bootcamp Santander 2025 - Back-End com Python oferecido pela DIO.me e Santander Academy</span>
</h5></i>

---

## Tecnologias Utilizadas

[![Python](https://custom-icon-badges.demolab.com/badge/-Python-3776AB?logo=python&logoColor=white&style=flat-square)](https://python.org/)
[![Pytest](https://custom-icon-badges.demolab.com/badge/-Pytest-0A9B71?logo=pytest&logoColor=white&style=flat-square)](https://pytest.org/)
[![Visual Studio Code](https://custom-icon-badges.demolab.com/badge/-VS%20Code-007ACC?logo=visualstudiocode&logoColor=white&style=flat-square)](https://code.visualstudio.com/)

---

## Como Usar
1. **Clone o repositório:**
    ```bash
    git clone https://github.com/StricterBot/simple-banking-system-python.git
    cd simple-banking-system-python
    ```

2.  **(Opcional) Instale as dependências para teste:**
    ```bash
    pip install pytest
    ```

3.  **Execute o programa:**
    - Certifique-se de ter o Python 3+ instalado.
    - No terminal, rode:
        ```bash
        python banksys.py
        ```
4.  **Siga o menu interativo:**<br>
    O menu agora inclui a gestão de clientes e contas:
    - Digite `1` para Depositar
    - Digite `2` para Sacar
    - Digite `3` para Extrato
    - Digite `4` para Novo Cliente
    - Digite `5` para Nova Conta
    - Digite `6` para Listar Contas
    - Digite `7` para Sair

## Documentação

- Sistema bancário que possibilita explorar funções como depósito, saque e extrato.
- O sistema apresenta mensagens claras e separadores visuais para facilitar o entendimento do usuário.
- As transações de saque e depósito são encapsuladas, garantindo que todas as regras de negócio (limites, saldo, etc.) e o registro no histórico sejam sempre aplicados.
- Suporte completo para criar múltiplos clientes e associar múltiplas contas a um mesmo cliente.
- O sistema foi completamente refatorado para utilizar uma arquitetura Orientada a Objetos, com classes que representam as entidades do banco de forma coesa e desacoplada.
- Utilizando `pytest`, a suíte de testes foi atualizada para validar o comportamento de cada classe e os principais cenários de uso, incluindo a interação entre múltiplas contas de um mesmo cliente

---

## O que você vai encontrar na minha versão

- **Histórico real de todas as operações, com data e hora;
- **Proteção de dados sensíveis** da conta, como o saldo, com métodos seguros que garantem a integridade das operações;
- **Mensagens internacionais (PT/EN)**, fácil de alterar. *(Removido temporariamente na v2.5)*;
- **Herança e Polimorfismo**;
- **Testes automatizados**, cobertura de testes com `pytest` que validam o comportamento de cada classe e cenários de uso complexos, como um cliente com múltiplas contas;
- **Boas práticas de código Python**: clareza, nomes intuitivos, tratamento de erros de entrada;
- **Experiência de usuário com feedback visual** após cada operação.

---

> [!IMPORTANT] 
> **Por que os valores estão em R$?**  
> O projeto foi idealizado e entregue em contexto brasileiro, seguindo o desafio original proposto no bootcamp.  
> O uso do símbolo R$ (Real brasileiro) mantém a fidelidade ao cenário do exercício e reforça o entendimento de limites, regras e práticas locais.

---
### Sobre mim:
[![LinkedIn](https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?logo=linkedin-white&logoColor=fff)](https://www.linkedin.com/in/victor-moreira-4210b9358/)
[![GitHub](https://custom-icon-badges.demolab.com/badge/GitHub-181717?logo=github&logoColor=fff)](https://github.com/StricterBot)
