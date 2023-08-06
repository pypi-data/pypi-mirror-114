from utils import *

def numero_certidoes (pontuacao: str = 'N', tipo_certidao: str = '') :
    r"""Gera uma Certidão
        :return: Retorna uma String contendo a Certidão gerada, com ou sem formatação.
        
        :param pontuacao: Determina se a String resultante terá formatação.
            :str: N | S

        :param tipo_certidao: Determina o tipo de Certidão gerada.
            :str: nascimento | casamento | casamento_religioso | obito
    """
    return newRequest(
        'PROGRAM', {
            'acao': 'gerador_certidao',
            'pontuacao': pontuacao,
            'tipo_certidao': tipo_certidao
        })

def numero_CNH () :
    r"""Gera uma CNH
    :return: Retorna uma string contendo o CNH gerado.
    """

    return newRequest(
        'PROGRAM',
        {'acao':'gerar_cnh'}
    )

def conta_bancaria (banco: str = '', estado: str = 'BA') :
    r"""Gera uma Conta Bancaria
        :return: Retorna um dicionario de Strings, contendo as chaves [Conta Corrente, Agencia, Banco, Cidade, Estado] e seus respectivos valores.

        :param banco: Texto responsavel por determinar o Banco a qual a conta gerada pertence.
            :str: BB = Banco do Brasil | BD = Banco do Bradesco | CB = Banco Citibank | BI = Banco Itaú | BS = Banco Santader
        
        :param estado: Texto resposavel por determinar o Estado a qual a conta gerada pertence.
            :str: AC | AL | AM | AP | BA | CE | DF | ES | GO | MA | MG | MS | MT | PA | PB | PE | PI | PR | RJ | RN | RS | RO | RR | SC | SE | SP | TO
    """
    
    if   banco == 'BB' : banco = 2
    elif banco == 'BD' : banco = 121
    elif banco == 'CB' : banco = 85
    elif banco == 'BI' : banco = 120
    elif banco == 'BS' : banco = 151
    
    return htmlForDictionary(newRequest('PROGRAM', {
            'acao': 'gerar_conta_bancaria',
            'estado': estado,
            'banco': banco
        }), key='.output-subtitle', value='.output-txt')

def numero_CPF (pontuacao: str = 'N', estado: str = 'BA') :
    r"""Gera um CPF
        :return: Retorna uma String contendo o CPF gerado, com ou sem formatação.

        :param pontuacao: Determina se a String resultante terá formatação.
            :str: N | S
        
        :param estado: Determina a qual Estado o CPF gerado pertence.
            :str: AC | AL | AM | AP | BA | CE | DF | ES | GO | MA | MG | MS | MT | PA | PB | PE | PI | PR | RJ | RN | RS | RO | RR | SC | SE | SP | TO
    """

    return newRequest('PROGRAM', {'acao':'gerar_cpf', 'pontuacao':pontuacao, 'cpf_estado': estado})

def numeros_aleatorios (numeros_unicos: bool = False, quantidade: int = 10, range: list[int] = [0,10], ordenacao: str = 'rand') :
    r"""Gera Números Aleatorios
        :return: Retornar uma Lista contendo todos os numeros gerados.

        :param numeros_unicos: Determina se os número serão unicos na Lista.
            :bool: True | False

        :param quantidade: Determina a quantidade de números a serem gerados.
            :int: Limitado há 10 mil números.
        
        :param range: Determina o range limite em qual os números serão gerados.
            :list[int]: Fornecer uma lista com dois Inteiros.
        
        :param ordenacao: Determina a ordenação da lista de números.
            :str: rand = Aleatória | asc = Crescente | desc = Decrescente
    """

    if quantidade > 10000 : return ['Erro: A quantidade de Números é superior ao limite.']   
    if numeros_unicos :
        numeros_unicos = 1
        if quantidade > range[1] : return ['Erro: A quantidade de Números é superior ao Range selecionado. Limite aplicado pelo Parametro Numeros Unicos.']

    return htmlForList(newRequest(
        'PROGRAM', {
            'acao':'gerar_numeros_aleatorios',
            'txt_quantidade':quantidade,
            'txt_entre_de':range[0],
            'txt_entre_para':range[1],
            'txt_colunas':'1',
            'chk_unico':numeros_unicos,
            'sel_ordem':ordenacao,
            'sel_listar':'coluna'
        }
    ), 'td')

def numero_PIS_PASEP (pontuacao: str = 'N') :
    r"""Gera um PIS/PASEP
        :return: Retornar uma String contendo o PIS/PASEP gerado.

        :param pontuacao: Determina se a String resultante terá formatação.
            :str: N | S
    """
    
    return newRequest(
        'PROGRAM', {
            'acao':'gerar_pis',
            'pontuacao':pontuacao
        }
    )

def numero_RENAVAM () :
    r"""Gera um RENAVAM
    :return: Retorna uma string contendo o RENAVAM gerado.
    """

    return newRequest(
        'PROGRAM',
        {'acao':'gerar_renavam'}
    )

def numero_CNPJ (pontuacao: str = 'N') :
    r"""Gera um CNPJ
        :return: Retorna uma String contendo o CNPJ gerado, com ou sem formatação.

        :param pontuacao: Determina se a String resultante terá formatação.
            :str: N | S
    """

    return newRequest('PROGRAM', {'acao':'gerar_cnpj', 'pontuacao':pontuacao})

def numero_RG (pontuacao: str = 'N') :
    r"""Gera um RG (SSP-SP)
        :return: Retorna uma String contendo o RG gerado, com ou sem formatação.

        :param pontuacao: Determina se a String resultante terá formatação.
            :str: N | S
    """

    return newRequest('PROGRAM', {'acao':'gerar_rg', 'pontuacao':pontuacao})

def inscricao_estadual (pontuacao: str = 'N', estado: str = 'BA') :
    r"""Gera uma Inscrição Estadual
        :return: Retorna uma String contendo o número de Inscrição Estadual gerado, com ou sem formatação.

        :param pontuacao: Determina se a String resultante terá formatação.
            :str: N | S
        
        :param estado: Determina a qual Estado a Inscrição gerada pertence.
            :str: AC | AL | AM | AP | BA | CE | DF | ES | GO | MA | MG | MS | MT | PA | PB | PE | PI | PR | RJ | RN | RS | RO | RR | SC | SE | SP | TO
    """

    return newRequest('PROGRAM', {'acao':'gerar_ie', 'pontuacao':pontuacao, 'estado': estado})

def titulo_de_eleitor (estado: str = 'BA') :
    r"""Gera um Título de Eleitor
        :return: Retorna uma String contendo o número do Título de Eleitor gerado.
        
        :param estado: Determina a qual Estado o Título de Eleitor gerado pertence.
            :str: AC | AL | AM | AP | BA | CE | DF | ES | GO | MA | MG | MS | MT | PA | PB | PE | PI | PR | RJ | RN | RS | RO | RR | SC | SE | SP | TO
    """

    return newRequest('PROGRAM', {'acao':'gerar_titulo_eleitor', 'estado':estado})

