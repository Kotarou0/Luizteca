from getpass import getpass
from hashlib import sha256
import datetime
from classes import *
import os
import pickle

# Cadastrando o dono com a senha padrão
SEM_PERMISSAO = "Você não tem permissão para realizar esta ação."
DONO_PADRAO = Dono("Luiz de Moraes Sampaio", "426.704.238-17", "Guarulhos", "(11) 96061-8848", "luiz.sagitario@yahoo.com.br", 2, SENHA_PADRAO)

def clear(): # Limpa a tela.
    if os.name == "nt": os.system("cls")
    else: os.system("clear")

def fazer_login():
    print("Bem-vindo. Faça login ou deixe vazio para sair.")
    while True:
        email = input("Digite seu e-mail: ")
        senha = sha256(getpass("Digite sua senha: ").encode()).hexdigest() # Lê a senha sem mostrar na tela com GETPASS e a criptografa com SHA256.
        if email == "": quit()
        funcionario_atual = 0
        for funcionario in funcionarios: # Procura um funcionário com o email digitado.
            if funcionario.email == email: funcionario_atual = funcionario

        if funcionario_atual == 0: # Se nenhum funcionário com este email foi encontrado.
            print("Este e-mail não está cadastrado. Tente novamente.")
        else:
            if funcionario_atual.senha == senha: 
                print("Logado com sucesso.")
                break # Volta pro loop inicial
            else: print("Senha incorreta. Tente novamente.")
    return funcionario_atual

def listar_publicacoes(nome=""):
    i = 1
    nome = nome.lower() # Não é case sensitive.
    for p in publicacoes:
        if nome in p.titulo.lower():
            print(f"[{i}] {p.titulo}, ISBN {p.isbn}")
        i += 1

def listar_funcionarios():
    i = 1
    for fun in funcionarios:
        print(f"[{i}] {fun.nome}, CPF {fun.cpf}")
        i += 1

def listar_clientes():
    i = 1
    for c in clientes:
        print(f"[{i}] {c.nome}, CPF {c.cpf}")
        i += 1

def sistema(): # Chamado até sair da conta.
    print(f"Bem-vindo {funcionario_atual.nome}. Opções disponíveis: ")
    print("[1] Cadastrar funcionário.")
    print("[2] Demitir funcionário.")
    print("[3] Mudar sua senha.")
    print("[4] Cadastrar cliente.")
    print("[5] Adicionar publicação.")
    print("[6] Adicionar exemplar.")
    print("[7] Emprestar exemplar.")
    print("[8] Devolver exemplar.")
    print("[9] Buscar publicação por título.")
    print("[10] Listar funcionários.")
    print("[11] Listar exemplares emprestados.")
    print("[12] Multar exemplares não conservados.")
    print("[13] Ver detalhes de um cliente.")
    print("[14] Ver detalhes de um funcionário.")
    print("[15] Remover publicação.")
    print("[16] Ver detalhes de uma publicação.")
    
    print("[99] Sair da conta.")
    
    while True: # Tenta pegar uma escolha válida até conseguir.
        try:
            escolha = int(input("Escolha: "))
            break
        except:
            print("Você não digitou um número. Tente novamente.")

    match escolha:
        case 1:
            if e_dono:
                funcionarios.append(dono.cadastrar_funcionario(funcionarios)) # Adiciona o funcionário cadastrado na lista de funcionários.
            else:
                print(SEM_PERMISSAO) # Se não for dono, mostrar que não tem permissão.
        case 2:
            if e_dono:
                if len(funcionarios) == 1: 
                    print("Não há outros funcionários cadastrados.") # Apenas o dono está cadastrado.
                else:
                    funcionarios.remove(dono.remover_funcionario(funcionarios)) # Remove o funcionário escolhido.
            else:
                print(SEM_PERMISSAO)
        case 3:
            funcionario_atual.mudar_senha() # Função da classe Funcionario.
        case 4:
            clientes.append(funcionario_atual.cadastrar_cliente()) # Adiciona um cliente novo na lista de clientes.
        case 5:
            publicacoes.append(funcionario_atual.adicionar_publicacao()) # Adiciona uma publicação nova na lista de publicações.
        case 6:
            if len(publicacoes) == 0: # 0 publicações cadastradas, não dá para adicionar exemplares.
                print("Não há publicações cadastradas. Por favor, cadastre uma publicação primeiro.")
            else: 
                listar_publicacoes()
                funcionario_atual.adicionar_exemplar(publicacoes)
        case 7:
            while True:
                try:
                    if len(publicacoes) == 0:
                        print("Nenhuma publicação no sistema.")
                        break
                    if len(clientes) == 0:
                        print("Não há clientes cadastrados.")
                        break
                    listar_publicacoes()
                    n = int(input("Escolha uma dessas publicações para emprestar: "))
                    if n < 1 or n > len(publicacoes): raise Exception() # Verifica se o número escolhido corresponde a uma publicação.

                    p = publicacoes[n-1] # -1 porque listamos as publicações a partir do 1.
                    if p.quantidade_exemplares_emprestados() == p.quantidade_exemplares(): # Todos foram emprestados.
                        print("Não há exemplares disponíveis para esta publicação.")
                        break
                    else:
                        # Pede-se o CPF por motivos de segurança: não é muito legal o funcionário ter acesso a todos os clientes.
                        cpf = input("Qual cliente quer pegar este título emprestado? Digite o CPF (com pontuação): ")
                        cliente = 0
                        for c in clientes: # Verifica todos os clientes em busca de um CPF.
                            if c.cpf == cpf: cliente = c
                        if cliente == 0:
                            print("O CPF digitado não foi encontrado. Certifique-se de digitar o CPF com pontuação.")
                            raise Exception()
                        for e in p.exemplares: # Procura nos exemplares da publicação e empresta um.
                            if e.emprestado == False:
                                e.emprestar_exemplar(funcionario_atual, cliente, datetime.datetime.now())
                                break
                        clear()
                        print(f"Exemplar de {p.titulo} emprestado para {cliente.nome} com sucesso no dia {datetime.datetime.now()}.")
                        break
                except:
                    print("Você digitou um número fora do intervalo permitido ou não digitou um número. Tente novamente.")
        case 8:
            while True:
                try:
                    if len(publicacoes) == 0:
                        print("Nenhuma publicação no sistema.")
                        break
                    listar_publicacoes()
                    n = int(input("Digite o número da publicação que está sendo devolvida: "))
                    if n < 1 or n > len(publicacoes): raise Exception()

                    p = publicacoes[n-1]

                    if p.quantidade_exemplares_emprestados() == 0:
                        print("Nenhum exemplar desta publicação foi emprestado.")
                        break

                    p.listar_exemplares_emprestados()
                    n = int(input("Selecione um dos exemplares emprestados para devolver: "))
                    if n < 1 or n > p.quantidade_exemplares_emprestados():
                        raise Exception()

                    e = p.exemplares[n-1] # Exemplar escolhido.
                    estado = int(input("Qual é o estado de conservação deste exemplar?\n[1] Conservado.\n[2] Não conservado.\nResposta: "))
                    if estado < 1 or estado > 2: raise Exception()

                    e.devolver_exemplar(datetime.datetime.now())
                    if estado == 2: 
                        print("Uma multa será aplicada ao cliente de acordo com o dono da biblioteca.")
                        print("Exemplar removido do sistema.")
                        multar.append([p, e]) # Anexa o exemplar e a publicação para o dono multar.
                        p.exemplares.remove(e)
                    print("Exemplar devolvido em", datetime.datetime.now(),"com sucesso.")
                    break
                except:
                    print("Você digitou um número fora do intervalo permitido ou não digitou um número. Tente novamente.")
        case 9:
            nome = input("Digite parte do nome da publicação (ou deixe vazio para listar todas): ")
            print("Publicações encontradas: ")
            listar_publicacoes(nome)
        case 10:
            if e_dono:
                print("Os funcionários cadastrados são:")
                listar_funcionarios()
            else:
                print(SEM_PERMISSAO)
        case 11:
            print("Exemplares emprestados:")
            i = 1
            for p in publicacoes: # Procura nas publicações
                for e in p.exemplares: # Procura nos exemplares
                    if e.emprestado:
                        print(f"[{i}] {p.tipo()} {p.titulo}, ISBN {p.isbn}, emprestado por {e.funcionario.nome} para {e.cliente.nome} no dia {e.data_emprestimo}.")
                        i += 1
        case 12:
            if e_dono and len(multar) > 0:
                print("Entre em contato com um dos clientes abaixo e dê baixa escolhendo uma das opções abaixo.")
                while True:
                    try:
                        i = 1
                        for m in multar:
                            p = m[0]
                            e = m[1]
                            print(f"[{i}] {p.tipo()} {p.titulo}, ISBN {p.isbn}, emprestado por {e.funcionario.nome} (CPF {e.funcionario.cpf}) para {e.cliente.nome} com CPF {e.cliente.cpf} e número de telefone {e.cliente.telefone}, emprestado no dia {e.data_emprestimo} e devolvido no dia {e.data_devolucao}.")
                            i += 1
                        n = int(input("Qual dos exemplares você quer dar baixa? "))
                        if n < 1 or n > i: raise Exception()
                        multar.remove(multar[n-1])
                        print("Sucesso.")
                        break
                    except:
                        print("Você digitou algo errado. Tente novamente.")
            else:
                if not e_dono: print(SEM_PERMISSAO)
                else: print("Não há exemplares para multar.")
        case 13:
            if len(clientes) != 0:
                while True:
                    try:
                        listar_clientes()
                        n = int(input("Escolha um cliente para ver detalhes: "))
                        if n < 1 or n > len(clientes): raise Exception()
                        cliente = clientes[n-1]
                        print(cliente)
                        break
                    except:
                        print("Você digitou algo errado. Tente novamente.")
            else:
                print("Não há clientes cadastrados.")
        case 14:
            if e_dono:
                while True:
                    try:
                        listar_funcionarios()
                        n = int(input("Escolha um funcionário para ver detalhes: "))
                        if n < 1 or n > len(funcionarios): raise Exception()
                        fun = funcionarios[n-1]
                        print(fun)
                        break
                    except:
                        print("Você digitou algo errado. Tente novamente.")
            else:
                print(SEM_PERMISSAO)
        case 15:
            while True:
                if len(publicacoes) == 0:
                    print("Não há publicações cadastradas.")
                    break
                try:
                    nome = input("Digite parte do nome da publicação que você quer remover: ")
                    listar_publicacoes(nome)
                    n = int(input("Digite o número correspondente à publicação que você quer remover: "))
                    if n < 1 or n > len(publicacoes): raise Exception()
                    publicacoes.remove(publicacoes[n-1])
                    print("Publicação e seus exemplares removidos com sucesso.")
                    break
                except:
                    print("Você digitou algo errado. Tente novamente.")
        case 16:
            while True:
                if len(publicacoes) == 0:
                    print("Não há publicações cadastradas.")
                    break
                try:
                    nome = input("Digite parte do nome da publicação: ")
                    listar_publicacoes(nome)
                    n = int(input("Escolha uma publicação: "))
                    if n < 1 or n > len(publicacoes): raise Exception()
                    print(publicacoes[n-1])
                    break
                except:
                    print("Digite apenas números inteiros no intervalo dado.")
        case _:
            print("Você não digitou uma opção válida.")
    return escolha

def carregar_arquivos():
    if not os.path.isfile('funcionarios.pkl'): return
    if not os.path.isfile('publicacoes.pkl'): return
    if not os.path.isfile('clientes.pkl'): return
    if not os.path.isfile('multar.pkl'): return

    with open('funcionarios.pkl', 'rb') as inp:
        while True:
            try:
                o = pickle.load(inp)
                if type(o) is Dono:
                    d = o
            except EOFError:
                break
            funcionarios.append(o)
    
    with open('publicacoes.pkl', 'rb') as inp:
        while True:
            try:
                o = pickle.load(inp)
            except EOFError:
                break
            publicacoes.append(o)

    with open('clientes.pkl', 'rb') as inp:
        while True:
            try:
                o = pickle.load(inp)
            except EOFError:
                break
            clientes.append(o)

    with open('multar.pkl', 'rb') as inp:
        while True:
            try:
                o = pickle.load(inp)
            except EOFError:
                break
            multar.append(o)

    return d

def salvar_arquivos():
#    funcionarios.remove(dono)
    with open('funcionarios.pkl', 'wb') as outp:
        for fun in funcionarios:
            pickle.dump(fun, outp, pickle.HIGHEST_PROTOCOL)
#    funcionarios.append(dono)

    with open('publicacoes.pkl', 'wb') as outp:
        for p in publicacoes:
            pickle.dump(p, outp, pickle.HIGHEST_PROTOCOL)

    with open('clientes.pkl', 'wb') as outp:
        for c in clientes:
            pickle.dump(c, outp, pickle.HIGHEST_PROTOCOL)

    with open('multar.pkl', 'wb') as outp:
        for m in multar:
            pickle.dump(m, outp, pickle.HIGHEST_PROTOCOL)

funcionarios = []
clientes = []
publicacoes = []
multar = []

dono = None
dono = carregar_arquivos()
if dono == None: 
    dono = DONO_PADRAO
    funcionarios.append(dono)

while True: # Loop do sistema
    funcionario_atual = fazer_login()
    e_dono = funcionario_atual == dono # A variável e_dono (é dono) diz se o funcionário logado é dono.
    while True:
        escolha_sistema = sistema()
        if escolha_sistema != 99: input("Aperte ENTER para continuar...")
        clear()
        if escolha_sistema == 99: 
            salvar_arquivos()
            break
