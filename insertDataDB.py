import pandas as pd
from bancoDeDados import DataBase
class insertDataDB():
    def dados(self):
        plan = pd.read_excel('Banco de dados S.T..xlsm', sheet_name=0, dtype={'VIGENTE':str, 'ITEM':str, 'DESCRICAO':str, 'CEST':str, 'NCM':str, 'ATACAD':float, 'IND': float, 'MVA4':float, 'MVA7':float, 'MVA12':float, 'CLASSIFICACAO':str})
        for lin in range(0,1045):
            vig = str(plan['VIGENTE'][lin])
            it = str(plan['ITEM'][lin])
            des = str(plan['DESCRICAO'][lin])
            cest = str(plan['CEST'][lin])
            ncm = str(plan['NCM'][lin])
            atac = float(plan['ATACAD'][lin])
            ind = float(plan['IND'][lin])
            mva4 = float(plan['MVA4'][lin])
            mva7 = float(plan['MVA7'][lin])
            mva12 = float(plan['MVA12'][lin])
            clas = str(plan['CLASSIFICACAO'][lin])
            
            
            self.data = DataBase()
            self.data.conecta()
            self.data.insert_dados_st(vig, it, des, cest, ncm, atac, ind, mva4, mva7, mva12, clas)
            self.data.close_conection()

# if __name__ == '__main__':
#     a=insertDataDB()
#     a.dados()