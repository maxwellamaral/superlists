"""
Testes funcionais do Django.
"""
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

# Edith ouviu falar de uma nova aplicação online interessante para lista de tarefas. Ela decide
# verificar sua homepage.

# * Mensagem padrão do Django 4.0 para testar se o servidor está funcionando.
assert 'The install worked successfully! Congratulations!' in browser.title

# Ela percebe que o título da página e o cabeçalho mencionam listas de tarefas (to-do)
assert 'To-Do' in browser.title

# Ela é convidada a inserir um item de tarefa imediatamente.

# Ela digita "Buy peacock feathers" (Comprar penas de pavão) em uma caixa de texto (o hobby
# de Edith é fazer iscas # para pesca com fly).

# Quando ela tecla enter, a página é atualizada, e agora a página lista
# "1: Buy peacock feathers" como um item em uma lista de tarefas.

# Ainda continua havendo uma caixa de texto convidando-a a acrescentar outro item.
# Ela insere "Use peacock feathers to make a fly" (Usar penas de pavão para fazer
# um fly - Edith é bem metódica).

# A página é atualizada novamente e agora mostra os dois itens em sua lista.

# Edith se pergunta se o site lembrará de sua lista. Então ela nota que o site gerou um URL
# único para ela - há um pequeno texto explicativo para isso.

# Ela acessa esse URL - sua lista de tarefas continua lá.

# Satisfeita, ela volta a dormir.
