from requests import post
from requests.structures import CaseInsensitiveDict
from bs4 import BeautifulSoup
from unicodedata import normalize

class Utils () :
    r"""Class containing auxiliary library functions
    
    """

    API_URL = 'https://www.4devs.com.br'
    HEAD = CaseInsensitiveDict()
    HEAD["Content-Type"] = "application/x-www-form-urlencoded"

    def FORMAT_THE_RETURN (self, formatting: bool) :
        return {True: lambda: 'S', False: lambda: 'N'}[formatting]()

    def IS_BRAZILIAN_STATE (self, state_to_check: str) :
        return {'AC': lambda: 'AC', 'AL': lambda: 'AL', 'AM': lambda: 'AM', 'AP': lambda: 'AP', 'BA': lambda: 'BA', 'CE': lambda: 'CE', 'DF': lambda: 'DF', 'ES': lambda: 'ES', 'GO': lambda: 'GO', 'MA': lambda: 'MA', 'MG': lambda: 'MG', 'MS': lambda: 'MS', 'MT': lambda: 'MT', 'PA': lambda: 'PA', 'PB': lambda: 'PB', 'PE': lambda: 'PE', 'PI': lambda: 'PI', 'PR': lambda: 'PR', 'RJ': lambda: 'RJ', 'RN': lambda: 'RN', 'RS': lambda: 'RS', 'RO': lambda: 'RO', 'RR': lambda: 'RR', 'SC': lambda: 'SC', 'SE': lambda: 'SE', 'SP': lambda: 'SP', 'TO': lambda: 'TO'}[state_to_check.upper()]()

    def convert_html_to_list (self, html: str, value: str) :
        list = []
        html: BeautifulSoup = BeautifulSoup(html, 'html5lib')
        all_values = html.find_all(value)
        for value in all_values :
            list.append(value.text.strip())
        return list

    def convert_html_to_dictionary (self, html: str, key: str, value: str) :
        dictionary: dict = dict()
        html: BeautifulSoup = BeautifulSoup(html, 'html5lib')
        all_keys = html.select(key)
        all_values = html.select(value)
        for index in range(len(all_keys)) :
            _key = normalize('NFKD', all_keys[index].text).encode('ASCII','ignore').decode('ASCII')
            _value = normalize('NFKD', all_values[index].text).encode('ASCII','ignore').decode('ASCII')
            dictionary[_key] = _value
        return dictionary

    def convert_dictionary_to_urlencoded_parameters (self, dictionary: dict) :
        parameters: str = str()
        for key in dictionary : parameters += f'{key}={dictionary.get(key)}&'
        return parameters

    def make_API_request (self, type: str, data: dict) :
        parameters = self.convert_dictionary_to_urlencoded_parameters(data)
        response = post(f'{self.API_URL}/' + {
            'PROGRAM': lambda: 'ferramentas_online.php',
            'MATH': lambda: 'ferramentas_matematica.php'
        }[type](), data=parameters, headers=self.HEAD)
        return response.content.decode('utf-8')

class Generator (Utils) :
    r"""Development plans:

        :generator: Credit Card

        :generator: Bank Account

        :generator: Certificates
            :state: finished

        :generator: CNH | CNPJ | CPF | RG
            :state: finished
        
        :generator: PIS/PASEP | RENAVAM

        :generator: Voter Title
            :state: finished
        
        :generator: State Registration
            :state: finished
    """

    def CPF (self, formatting: bool, brazilian_state: str) :
        r"""Generates a CPF number
            :return: text containing the generated CPF, with or without formatting.

            :param formatting: determines whether the resulting text will have formatting.
                :bool: True | False
            
            :param brazilian_state: Determines which Brazilian state the generated CPF belongs to.
                :str: AC | AL | AM | AP | BA | CE | DF | ES | GO | MA | MG | MS | MT | PA | PB | PE | PI | PR | RJ | RN | RS | RO | RR | SC | SE | SP | TO
        """

        return self.make_API_request('PROGRAM', 
            {'acao':'gerar_cpf',
            'pontuacao': self.FORMAT_THE_RETURN(formatting),
            'cpf_estado': self.IS_BRAZILIAN_STATE(brazilian_state)
            })

    def VOTER_TITLE (self, brazilian_state: str) :
        r"""Generates Voter Title
            :return: text containing the generated voter ttile, with or without formatting.

            :param formatting: determines whether the resulting text will have formatting.
                :bool: True | False
            
            :param brazilian_state: Determines which Brazilian state the generated voter ttile belongs to.
                :str: AC | AL | AM | AP | BA | CE | DF | ES | GO | MA | MG | MS | MT | PA | PB | PE | PI | PR | RJ | RN | RS | RO | RR | SC | SE | SP | TO
        """

        return self.make_API_request('PROGRAM', {'acao':'gerar_titulo_eleitor', 'estado':self.IS_BRAZILIAN_STATE(brazilian_state)})

    def RG (self, formatting: bool) :
            r"""Generates a RG number
                :return: text containing the generated RG, with or without formatting.

                :param formatting: determines whether the resulting text will have formatting.
                    :bool: True | False
            """

            return self.make_API_request('PROGRAM',
            {'acao':'gerar_rg', 'pontuacao':self.FORMAT_THE_RETURN(formatting)})
    
    def CNPJ (self, formatting: bool) :
            r"""Generates a CNPJ number
                :return: text containing the generated CNPJ, with or without formatting.

                :param formatting: determines whether the resulting text will have formatting.
                    :bool: True | False
            """

            return self.make_API_request('PROGRAM',
                {'acao':'gerar_cnpj', 'pontuacao':self.FORMAT_THE_RETURN(formatting)})

    def CNH (self) :
        r"""Generates a CNH number
            :return: text containing the generated CNH, with or without formatting.

            :param formatting: determines whether the resulting text will have formatting.
                :bool: True | False
        """

        return self.make_API_request('PROGRAM',
            {'acao':'gerar_cnh'})

    def STATE_REGISTRATION (self, formatting: bool, brazilian_state: str) :
        r"""Generates State Registration
            :return: text containing the generated state registration, with or without formatting.

            :param formatting: determines whether the resulting text will have formatting.
                :bool: True | False
            
            :param brazilian_state: Determines which Brazilian state the generated state registration belongs to.
                :str: AC | AL | AM | AP | BA | CE | DF | ES | GO | MA | MG | MS | MT | PA | PB | PE | PI | PR | RJ | RN | RS | RO | RR | SC | SE | SP | TO
        """

        return self.make_API_request('PROGRAM', {'acao':'gerar_ie','pontuacao':self.FORMAT_THE_RETURN(formatting),'estado':self.IS_BRAZILIAN_STATE(brazilian_state)})

    def CERTIFICATE (self, formatting: bool, type: str, ) :
        r"""Generates a Brazilian Certificate, which can be of the types: birth, marriage, religious marriage and death.
            
            :param formatting: determines whether the resulting text will have formatting.
                    :bool: True | False
            
            :param type: determines what type for certificate is generated.
                :str: N = Birth | C = Marriage | CR = Religious Marriage | O = Death
        """
        return self.make_API_request('PROGRAM', {
            'acao':'gerador_certidao', 'pontuacao':self.FORMAT_THE_RETURN(formatting), 'tipo_certidao': {
                'N': lambda: 'nascimento', 'C': lambda: 'casamento', 'CR': lambda: 'casamento_religioso', 'O': lambda: 'obito'
            }[type]()
        })
   
class Validator (Utils) :
    r"""Development plans:

        :validator: Credit Card

        :validator: Bank Account

        :validator: Certificates

        :validator: CNH | CNPJ | CPF | RG
        
        :validator: PIS/PASEP | RENAVAM

        :validator: Voter Title
        
        :validator: State Registration
    """
