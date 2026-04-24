import numpy as np
import skfuzzy as fuzz

class FuzzySystem:
    def __init__(self):
        self.mfs = {}
        self.rules = []
        
    def create_membership_function(self, name, x, mf_type='triangular', params=None):
        """
        Criar funções de pertencimento
        mf_type: 'triangular', 'trapezoidal', 'gaussian', 'sigmoid'
        """
        if mf_type == 'triangular' and params:
            self.mfs[name] = fuzz.trimf(x, params)
        elif mf_type == 'trapezoidal' and params:
            self.mfs[name] = fuzz.trapmf(x, params)
        elif mf_type == 'gaussian' and params:
            mean, sigma = params
            self.mfs[name] = fuzz.gaussmf(x, mean, sigma)
        elif mf_type == 'sigmoid' and params:
            x0, a = params
            self.mfs[name] = fuzz.sigmf(x, x0, a)
            
    def get_membership_value(self, name):
        """Retorna os valores da função de pertencimento"""
        return self.mfs.get(name)
    
    def apply_rule(self, membership1, membership2, operation='and'):
        """
        Aplicar operações lógicas fuzzy
        operation: 'and' (min), 'or' (max), 'not'
        """
        if operation == 'and':
            return np.minimum(membership1, membership2)
        elif operation == 'or':
            return np.maximum(membership1, membership2)
        elif operation == 'not':
            return 1 - membership1
        
    def defuzzify(self, mf_value, x, method='centroid'):
        """
        Converter saída fuzzy em valor crisp
        method: 'centroid', 'bisector', 'mom' (middle of maximum)
        """
        if method == 'centroid':
            return fuzz.defuzz(x, mf_value, 'centroid')
        elif method == 'bisector':
            return fuzz.defuzz(x, mf_value, 'bisector')
        elif method == 'mom':
            return fuzz.defuzz(x, mf_value, 'mom')


class HeightPersistenceSystem:
    """
    Sistema de lógica fuzzy para classificar altura e persistência
    Entrada: altura (cm) e persistência (0-10)
    Saída: classificação de grupo
    """
    def __init__(self):
        # Definir universo de discurso
        self.altura = np.arange(130, 210, 1)
        self.persistencia = np.arange(0, 11, 0.5)
        self.output = np.arange(0, 11, 1)
        
        # Funções de pertencimento para altura
        self.altura_baixa = fuzz.trimf(self.altura, [130, 130, 160])
        self.altura_media = fuzz.trimf(self.altura, [155, 170, 185])
        self.altura_alta = fuzz.trimf(self.altura, [180, 210, 210])
        
        # Funções de pertencimento para persistência
        self.persistencia_baixa = fuzz.trimf(self.persistencia, [0, 0, 3.5])
        self.persistencia_media = fuzz.trimf(self.persistencia, [2.5, 5, 7.5])
        self.persistencia_alta = fuzz.trimf(self.persistencia, [6.5, 10, 10])
        
        # Funções de pertencimento da saída
        self.grupo_inicial = fuzz.trimf(self.output, [0, 0, 4])
        self.grupo_intermediario = fuzz.trimf(self.output, [3, 5, 7])
        self.grupo_avancado = fuzz.trimf(self.output, [6, 10, 10])
    
    def evaluate(self, altura_val, persistencia_val):
        """
        Avalia entrada e retorna classificação fuzzy
        """
        # Grau de pertencimento das entradas
        altura_b = fuzz.interp_membership(self.altura, self.altura_baixa, altura_val)
        altura_m = fuzz.interp_membership(self.altura, self.altura_media, altura_val)
        altura_a = fuzz.interp_membership(self.altura, self.altura_alta, altura_val)
        
        persist_b = fuzz.interp_membership(self.persistencia, self.persistencia_baixa, persistencia_val)
        persist_m = fuzz.interp_membership(self.persistencia, self.persistencia_media, persistencia_val)
        persist_a = fuzz.interp_membership(self.persistencia, self.persistencia_alta, persistencia_val)
        
        # Regras fuzzy
        rule1 = np.minimum(altura_a, persist_a)  # Alta altura E Alta persistência -> Avançado
        rule2 = np.minimum(altura_b, persist_b)  # Baixa altura E Baixa persistência -> Inicial
        rule3 = np.maximum(
            np.minimum(altura_m, persist_m),     # Média altura E Média persistência -> Intermediário
            np.minimum(altura_a, persist_b)      # Ou Alta altura E Baixa persistência
        )
        
        # Agregação das regras
        output_inicial = np.minimum(rule2, self.grupo_inicial)
        output_inter = np.minimum(rule3, self.grupo_intermediario)
        output_avanc = np.minimum(rule1, self.grupo_avancado)
        
        # Agregação final
        output_agg = np.maximum(output_inicial, np.maximum(output_inter, output_avanc))
        
        # Defuzzificação
        try:
            resultado = fuzz.defuzz(self.output, output_agg, 'centroid')
        except:
            resultado = 5  # Valor padrão se defuzzificação falhar
            
        return {
            'altura_b': altura_b,
            'altura_m': altura_m,
            'altura_a': altura_a,
            'persist_b': persist_b,
            'persist_m': persist_m,
            'persist_a': persist_a,
            'output': output_agg,
            'resultado': resultado
        }
