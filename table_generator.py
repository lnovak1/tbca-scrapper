import math
import pandas as pd 
from datetime import datetime
ALIMENT_INTAKE=[
    {'Ingredientes' : 'Farinha de grao de bico',
    'Qtde (g)': 115
    },
    {'Ingredientes' : 'Fécula de batata, crua',
    'Qtde (g)': 86
    },
    {'Ingredientes' : 'Arroz, farinha, crua (média de diferentes marcas), Orysa sativa L.',
    'Qtde (g)': 81
    },
    {'Ingredientes' : 'Inhame, s/ casca, assado, s/ óleo, s/ sal, Colocasia esculenta',
    'Qtde (g)': 52
    },
    {'Ingredientes' : 'Azeite, oliva, cozido',
    'Qtde (g)': 47
    },
    {'Ingredientes' : 'Sal, refinado',
    'Qtde (g)': 7
    },
    {'Ingredientes' : 'Goma xantana',
    'Qtde (g)': 3
    },
    {'Ingredientes' : 'Tofu soft organico',
    'Qtde (g)': 93
    },
    {'Ingredientes' : 'Espinafre, cozido, drenado, s/ óleo, s/ sal, Tetragonia expansa',
    'Qtde (g)': 78
    },
    {'Ingredientes' : 'Cebola, branca, assada, s/ óleo, s/ sal, Allium cepa L.',
    'Qtde (g)': 23
    },
    {'Ingredientes' : 'Cenoura, s/ casca, cozida, drenada, s/ óleo, s/ sal, Daucus carota L.',
    'Qtde (g)': 23
    },
    {'Ingredientes' : 'Orégano, seco, Origanum vulgare',
    'Qtde (g)': 2
    },
    {'Ingredientes' : 'Noz moscada, em pó, Myristica fragrans',
    'Qtde (g)': 2
    }]

auxiliar_dict = {}

file_path = './alimentos.txt'
with open(file_path, "r", encoding='utf-8') as file:
    for line in file:
        removed_multi_space =  " ".join(line.split())
        obj = eval(removed_multi_space)
        nutrient_dict = {}
        for nutri in obj['nutrientes']:
            nutrient_dict[nutri['Componente']] = nutri
        obj['nutrientes'] = nutrient_dict
        auxiliar_dict[  obj['descricao']] = obj
file.close()

def get_values(qnt:str, value_for_hundred:str):
    if value_for_hundred == 'tr':
        return None
    num_qnt =  float(str(qnt).replace(',','.'))
    num_value_for_hundred =  float(str(value_for_hundred).replace(',','.'))
    return num_qnt * (num_value_for_hundred/100)

for aliment in ALIMENT_INTAKE:
    aliment['Ingredientes'] = aliment['Ingredientes'].strip()
    ingredient_info = auxiliar_dict.get(aliment['Ingredientes'])
    if not ingredient_info is None:
        # if not auxiliar_dict[aliment['Ingredientes']] is None:
        aliment['Calorias (Kcal)'] = get_values(aliment['Qtde (g)'],(ingredient_info['nutrientes']['Energia']['Valor por 100g']))
        aliment['Carb tot (g)'] = get_values(aliment['Qtde (g)'],ingredient_info['nutrientes']['Carboidrato total']['Valor por 100g'])
        aliment['Açúcares adc (g)'] = get_values(aliment['Qtde (g)'],ingredient_info['nutrientes']['Açúcar de adição']['Valor por 100g'])
        aliment['Proteínas (g)'] = get_values(aliment['Qtde (g)'],ingredient_info['nutrientes']['Proteína']['Valor por 100g'])
        aliment['Gord total (g)'] = get_values(aliment['Qtde (g)'],ingredient_info['nutrientes']['Lipídios']['Valor por 100g'])
        aliment['Gord sat (g)'] = get_values(aliment['Qtde (g)'],ingredient_info['nutrientes']['Ácidos graxos saturados']['Valor por 100g'])
        aliment['Gord trans (g)'] = get_values(aliment['Qtde (g)'],ingredient_info['nutrientes']['Ácidos graxos trans']['Valor por 100g'])
        aliment['Fibras (g)'] = get_values(aliment['Qtde (g)'],ingredient_info['nutrientes']['Fibra alimentar']['Valor por 100g'])
        aliment['Sódio (mg)'] = get_values(aliment['Qtde (g)'],ingredient_info['nutrientes']['Sódio']['Valor por 100g'])

total_obj = {'Ingredientes' : 'TOTAL',
             'Qtde (g)': 0,
             'Calorias (Kcal)':0,
             'Carb tot (g)':0,
             'Açúcares adc (g)':0,
             'Proteínas (g)':0,
             'Gord total (g)':0,
             'Gord sat (g)':0,
             'Gord trans (g)':0,
             'Fibras (g)':0,
             'Sódio (mg)':0,
    }
for aliment in ALIMENT_INTAKE:
    for key in aliment.keys():
        if key != 'Ingredientes':
            if not aliment[key] is None and not math.isnan(aliment[key]):
                total_obj[key] = total_obj[key] + aliment[key]
ALIMENT_INTAKE.append(total_obj)
df=  pd.DataFrame(ALIMENT_INTAKE)
date_now = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
with pd.ExcelWriter(f"table{date_now}.xlsx") as writer:
    df.to_excel(writer)