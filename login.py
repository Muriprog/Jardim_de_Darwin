import re

def validar_email(email):
    # Padrão de email do Gmail
    padrao_gmail = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
    # padrao_outlook = 
    # padrao_terra = 

    # Verificar se o email corresponde ao padrão
    if re.match(padrao_gmail, email):
        return True
    else:
        return False

def login():
    print("Por favor, faça login.")
    email = input("Email: ")
    senha = input("Senha: ")

    if validar_email(email) and len(senha) >= 6:
        print("Login bem-sucedido! Bem-vindo à sua página inicial.")
    elif  len(senha) < 6:
        print("Senha de tamanho incorreto. Senha deve ser maior ou igual a 6")
    else:
        print("Email, senha ou formato de email incorretos. Tente novamente.")

if __name__ == "__main__":
    login()
