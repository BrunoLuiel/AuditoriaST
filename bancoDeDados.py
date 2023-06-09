import sqlite3

class DataBase():
    def __init__(self, name = 'DataBase.db') -> None:
        self.name = name

    def conecta(self): 
        self.conection=sqlite3.connect(self.name)
    
    def close_conection(self):
        try:
            self.conection.close()
        except:
            pass

    def create_table(self):
        try:
            cursor=self.conection.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS SubstituicaoTributaria (
                vigente text, 
                item text, 
                descricao text, 
                cest text, 
                ncm text, 
                mvaAtac numeric, 
                mvaInd numeric, 
                mva4 numeric, 
                mva7 numeric, 
                mva12 numeric, 
                classificacao text
                );""")
        except AttributeError:
            print("Faça conexão/Erro na criação da tabela")

    def insert_dados_st(self, vigente, item, descricao, cest, ncm, mvaatac, mvaind, mva4, mva7, mva12, classif):
        try:
            cursor = self.conection.cursor()
            cursor.execute("""
            INSERT INTO SubstituicaoTributaria(vigente, item, descricao, cest, ncm, mvaatac, mvaind, mva4, mva7, mva12, classificacao) VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
            (vigente, item, descricao, cest, ncm, mvaatac, mvaind, mva4, mva7, mva12, classif ) )
            self.conection.commit()
            print('Inserção de dados concluídos com sucesso!')
        except:
            print("Erro ao inserir dados no SubstituicaoTributaria.db")

    def check_st(self, ncm, cest):
        try:
            cursor = self.conection.cursor()
            for a in [len(ncm), len(ncm)-1, len(ncm)-2, len(ncm)-3, len(ncm)-4]:
                cursor.execute(f"""SELECT * FROM SubstituicaoTributaria WHERE ncm = {ncm[0:a]}""")
                resultado = cursor.fetchall()
                    #Não fiz a exceção de CEST incorreto, pois será mais interessante criar outro código pra verificação de CEST
                for i in resultado:
                    if i[0]=='s' and str(i[4]) == str(ncm[0:a]) and i[3] == cest:
                        return f"NCM e CEST sujeitos a substituição tributária|conforme item {i[1]} {i[10]}|{i[2]}"                        
                    elif i[0]=='s' and i[4] == ncm[0:a] and cest=="":
                        return f"NCM Localizado mas nao foi declarado CEST|item {i[1]} {i[10]}|{i[2]}"
                    else:
                        pass
                    
            return "O NCM pesquisado NAO E SUJEITO a Substituição tributária"
        except:
            print("Erro ao consultar NCM/CEST")



if __name__ == '__main__':
    a=DataBase()
    a.conecta()
    print(a.check_st("87072999", ""))
    a.close_conection()