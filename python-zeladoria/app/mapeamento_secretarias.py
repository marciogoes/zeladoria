"""
Mapeamento Categorias -> Secretarias
Sistema de Zeladoria Urbana - Belém/PA

Define qual secretaria é responsável por cada tipo de problema
"""

# Mapeamento de categorias para secretarias
CATEGORIA_SECRETARIA = {
    # INFRAESTRUTURA E URBANISMO -> SEURB
    "Iluminação Pública": "SEURB",
    "Buraco na Via": "SEURB",
    "Sinalização Danificada": "SEURB",
    "Calçada Danificada": "SEURB",
    "Obra Irregular": "SEURB",
    "Invasão de Via Pública": "SEURB",
    
    # SANEAMENTO -> SESAN
    "Esgoto Entupido": "SESAN",
    "Vazamento de Água": "SESAN",
    "Falta de Água": "SESAN",
    "Esgoto a Céu Aberto": "SESAN",
    "Drenagem Obstruída": "SESAN",
    "Alagamento": "SESAN",
    
    # MEIO AMBIENTE -> SEMMA
    "Coleta de Lixo": "SEMMA",
    "Lixo Acumulado": "SEMMA",
    "Poda de Árvore": "SEMMA",
    "Árvore Caída": "SEMMA",
    "Mato Alto": "SEMMA",
    "Descarte Irregular": "SEMMA",
    "Poluição Sonora": "SEMMA",
    "Poluição do Ar": "SEMMA",
    "Poluição da Água": "SEMMA",
    "Desmatamento Irregular": "SEMMA",
    "Maus Tratos a Animais": "SEMMA",
    
    # SAÚDE -> SESMA
    "Posto de Saúde": "SESMA",
    "Hospital": "SESMA",
    "Agente de Saúde": "SESMA",
    "Dengue": "SESMA",
    "Vacinação": "SESMA",
    "Controle de Pragas": "SESMA",
    "Fiscalização Sanitária": "SESMA",
    
    # EDUCAÇÃO -> SEMEC
    "Escola": "SEMEC",
    "Creche": "SEMEC",
    "Transporte Escolar": "SEMEC",
    "Merenda Escolar": "SEMEC",
    
    # ESPORTE E LAZER -> SEJEL
    "Praça": "SEJEL",
    "Parque": "SEJEL",
    "Quadra Esportiva": "SEJEL",
    "Equipamento de Lazer": "SEJEL",
    
    # SEGURANÇA -> GMB
    "Segurança Pública": "GMB",
    "Patrimônio Público": "GMB",
    "Câmeras de Segurança": "GMB",
    
    # CODEM -> Feiras e Mercados
    "Feira": "CODEM",
    "Mercado": "CODEM",
    "Comércio Ambulante": "CODEM",
    
    # OUVIDORIA -> OGM
    "Denúncia": "OGM",
    "Reclamação": "OGM",
    "Sugestão": "OGM",
    "Elogio": "OGM",
    
    # MULHER -> SEMULHER
    "Violência contra Mulher": "SEMULHER",
    "Políticas para Mulheres": "SEMULHER",
    
    # HABITAÇÃO -> SEHAB
    "Habitação": "SEHAB",
    "Regularização Fundiária": "SEHAB",
    "Moradia": "SEHAB",
    
    # OUTROS -> GABPREF
    "Outros": "GABPREF",
}


def get_secretaria_by_categoria(categoria_nome):
    """
    Retorna a sigla da secretaria responsável pela categoria
    
    Args:
        categoria_nome (str): Nome da categoria
        
    Returns:
        str: Sigla da secretaria responsável
    """
    return CATEGORIA_SECRETARIA.get(categoria_nome, "GABPREF")


def get_categorias_by_secretaria(sigla_secretaria):
    """
    Retorna todas as categorias de responsabilidade de uma secretaria
    
    Args:
        sigla_secretaria (str): Sigla da secretaria (ex: SEURB, SEMMA)
        
    Returns:
        list: Lista de categorias
    """
    return [
        categoria 
        for categoria, secretaria in CATEGORIA_SECRETARIA.items() 
        if secretaria == sigla_secretaria
    ]


# Exemplos de uso
if __name__ == "__main__":
    print("Exemplos de uso:\n")
    
    # Descobrir secretaria responsável
    print("1. Qual secretaria é responsável por 'Iluminação Pública'?")
    print(f"   → {get_secretaria_by_categoria('Iluminação Pública')}\n")
    
    print("2. Qual secretaria é responsável por 'Coleta de Lixo'?")
    print(f"   → {get_secretaria_by_categoria('Coleta de Lixo')}\n")
    
    # Listar categorias de uma secretaria
    print("3. Quais categorias a SEMMA é responsável?")
    categorias_semma = get_categorias_by_secretaria("SEMMA")
    for cat in categorias_semma:
        print(f"   • {cat}")
    print()
    
    print("4. Quais categorias a SEURB é responsável?")
    categorias_seurb = get_categorias_by_secretaria("SEURB")
    for cat in categorias_seurb:
        print(f"   • {cat}")
