from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')

# Mensagem padrão do Django 4.0 para testar se o servidor está funcionando.
assert 'The install worked successfully! Congratulations!' in browser.title