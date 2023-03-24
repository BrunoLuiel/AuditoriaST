import os
import xml.etree.ElementTree as Et
from bancoDeDados import DataBase

class Read_xml():
    def __init__(self, directory) -> None:
        self.directory = directory
        lista = ['Resultado da auditoria.txt', 'CORRIGIR - Produtos que não são S.T.txt', 'CORRIGIR - Produtos que são S.T.txt']
        for i in lista:
            with open(self.directory + '\\' + i, 'w', encoding='utf-8') as arq:
                arq.write('Código|Descrição|NCM|NF-e|CFOP|CST|CEST|Resultado da auditoria\n')
            arq.close()
        
        directory = self.all_files()
        for i in directory:
            self.check_chave(i)

    
    def all_files(self):
        return [ os.path.join(self.directory, arq) for arq in os.listdir(self.directory) if arq.lower().endswith('.xml')]

    def check_chave(self, xml):

        self.xml = xml
        root = Et.parse(self.xml).getroot()
        nsNFe = {"ns":"http://www.portalfiscal.inf.br/nfe"}
        nsCTe = {"ns":"http://www.portalfiscal.inf.br/cte"}

        chaveNfe = self.check_none(root.find('./ns:protNFe/ns:infProt/ns:chNFe', nsNFe))
        chaveCte = self.check_none(root.find('./ns:protCTe/ns:infProt/ns:chCTe', nsCTe))

        if chaveNfe != '':
            self.nfe_data(self.xml)
        
        elif chaveCte != '':
            self.cte_data(self.xml)

        else:
            pass
            #print(f'Não identificado provavelmente não se trata de NF-e ou CT-e {self.xml}')
            #quit()


    def nfe_data(self, xml):
        root = Et.parse(xml).getroot()
        nsNFe = {"ns":"http://www.portalfiscal.inf.br/nfe"}

        #Dados da NF-e
        chave = self.check_none(root.find('./ns:protNFe/ns:infProt/ns:chNFe', nsNFe))
        nfe = self.check_none(root.find("./ns:NFe/ns:infNFe/ns:ide/ns:nNF", nsNFe))
        
        #Dados Emitente
        if self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CPF', nsNFe)) != '':
            doc_emit = self.format_cnpj_cpf(self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CPF', nsNFe)))
        elif  self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFe)) != '':
            doc_emit = self.format_cnpj_cpf(self.check_none(root.find('./ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', nsNFe)))
        else:
            print('erro na definição do emitente')
            quit()


        #Item da nota
        itemNota = 1
        prod = []

        for item in root.findall("./ns:NFe/ns:infNFe/ns:det", nsNFe):
            cod_item =  self.check_none(item.find(".ns:prod/ns:cProd", nsNFe))
            descricao_item = self.check_none(item.find('.ns:prod/ns:xProd', nsNFe))
            ncm = self.check_none(item.find('.ns:prod/ns:NCM', nsNFe))
            cest = self.check_none(item.find('.ns:prod/ns:CEST', nsNFe))
            cfop = self.check_none(item.find('.ns:prod/ns:CFOP', nsNFe))
            un_medida = self.check_none(item.find('.ns:prod/ns:uCom', nsNFe))
            qtd_item = self.check_none(item.find('.ns:prod/ns:qCom', nsNFe))
            vlr_unit_item = self.check_none(item.find('.ns:prod/ns:vUnCom', nsNFe))
            vlr_item = self.check_none(item.find('.ns:prod/ns:vProd', nsNFe))

            v_un_trib = self.check_none(item.find('.ns:prod/ns:vUnTrib', nsNFe))
            v_frete = self.check_none(item.find('.ns:prod/ns:vFrete', nsNFe))
            v_seg = self.check_none(item.find('.ns:prod/ns:vSeg', nsNFe))
            v_desc = self.check_none(item.find('.ns:prod/ns:vDesc', nsNFe))
            v_outro = self.check_none(item.find('.ns:prod/ns:vOutro', nsNFe))
            ind_tot = self.check_none(item.find('.ns:prod/ns:indTot', nsNFe))

            #Imposto
            v_tot_trib = self.check_none(item.find('.ns:imposto/ns:vTotTrib', nsNFe))
            codigos = ['/ns:ICMS00', '/ns:ICMS10', '/ns:ICMS20', '/ns:ICMS30', '/ns:ICMS40', '/ns:ICMS51', '/ns:ICMS60', '/ns:ICMS70', '/ns:ICMS90', '/ns:ICMSSN101', '/ns:ICMSSN102', '/ns:ICMSSN201', '/ns:ICMSSN202', '/ns:ICMSSN500', '/ns:ICMSSN900']
            
            #Conecta banco de dados           
            ob = DataBase()
            ob.conecta()

            for cada in codigos:
                if self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:orig', nsNFe)) == '':
                    pass
                else:
                    orig = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:orig', nsNFe))
                    if self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:CST', nsNFe)) == '':
                        cst_csosn = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:CSOSN', nsNFe))
                    else:
                        cst_csosn = self.check_none(item.find(f'.ns:imposto/ns:ICMS{cada}/ns:CST', nsNFe))
                                       
                    check_ncm = ob.check_st(ncm, cest)

                    #Escreve na planilha completa
                    with open(self.directory + '\Resultado da auditoria.txt', 'a', encoding="utf-8") as arq:
                        arq.write(f"{cod_item}|{descricao_item}|{str(ncm)}|{nfe}|{cfop}|{cst_csosn}|{str(cest)}|{check_ncm}\n")
                    arq.close()

                    #Alternar entre os principais produtos a serem alterados:
                    if check_ncm[0:50] == 'NCM e CEST é substituição tributária|conforme item' and cfop == '5101' or check_ncm[0:50] == 'NCM e CEST é substituição tributária|conforme item'and cfop == '5102':
                        with open(self.directory + '\CORRIGIR - Produtos que não são S.T.txt', 'a', encoding="utf-8") as arq:
                            arq.write(f"{cod_item}|{descricao_item}|{str(ncm)}|{nfe}|{cfop}|{cst_csosn}|{str(cest)}|{check_ncm}\n")
                        arq.close()
                    elif check_ncm[0:46] == 'O NCM pesquisado não é Substituição tributária' and cfop == '5405':
                        with open(self.directory + '\CORRIGIR - Produtos que são S.T.txt', 'a', encoding="utf-8") as arq:
                            arq.write(f"{cod_item}|{descricao_item}|{str(ncm)}|{nfe}|{cfop}|{cst_csosn}|{str(cest)}|{check_ncm}\n")
                        arq.close()

            #Fecha banco de dados
            ob.close_conection()


    def check_none(self, var):
        if var == None:
            return ''
        else:
            try:
                return var.text.replace('.',',')
            except:
                return var.text
    
    def format_cnpj_cpf(self, doc):
        if len(doc) == 14:
            try:
                doc = f'{doc[:2]}.{doc[2:5]}.{doc[5:8]}/{doc[8:12]}-{doc[12:14]}'
                return doc

            except:
                return ""
        elif len(doc) == 11:
                try:
                    doc = f'{doc[:3]}.{doc[3:6]}.{doc[6:9]}-{doc[9:11]}'
                    return doc
                except:
                    return ''
        else:
            print('erro na validação do CPF ou CNPJ')
            quit()
            

if __name__ == '__main__':

        #Sobrescreve dados anteriores com cabeçalho


    xml  = Read_xml('C:\\Users\\ADM\\Documents\\Python\\Auditoria de ST\\022023')
    # all = xml.all_files()
    # for i in all:
    #     a = xml.check_chave(i)
