import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response



# Create your views here.

@csrf_exempt
@api_view(['POST'])
def get_curriculo(request):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(executable_path='../venv/geckodriver.exe', options=options)
    driver.get('https://www.linkedin.com/login')

    sleep(10)

    dados = request.data
    usuario = dados['usuario']
    senha = dados['senha']


    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(usuario)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(senha)

    driver.find_element(By.XPATH, '//*[@class="login__form_action_container "]/button').click()
    sleep(5)


    driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/div/div[1]/div[1]/a/div[2]').click()
    sleep(2)


    dadosUsuario = {
        'informacoesPessoais': {
            'nome':'',
            'sobrenome':'',
            'imagem':'',
            'cargo':'',
            'telefone':'',
            'email':'',
            'links':[],
            'perfilLinkedIn':'',
            'dataNascimento':'',
            'localizacao':'',

        },
        'sobre':'',
        'experiencia':[],
        'formacoes':[],
        'licencasCertificados':[],
        'competencias':[],
        'projetos':[],
        'idiomas':[],
    }


    nome = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]/h1').text
    cargo = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[2]').text
    localizacao = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[2]/span[1]').text
    imagem = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[2]/div/div/main/section[1]/div[2]/div[1]/div[1]/div/div/button/img').get_attribute('src')

    dadosUsuario['informacoesPessoais']['nome'] = nome.split(' ')[0]
    #unir elementos da lista em string
    dadosUsuario['informacoesPessoais']['sobrenome'] = ' '.join(nome.split(' ')[1:])
    dadosUsuario['informacoesPessoais']['cargo'] = cargo
    dadosUsuario['informacoesPessoais']['imagem'] = imagem
    dadosUsuario['informacoesPessoais']['localizacao'] = localizacao

    irInformacoesContato = driver.find_element(By.XPATH, '//*[@id="top-card-text-details-contact-info"]').click()
    sleep(2)

    linkedin = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/section/div/section[1]/div/a').text
    link = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/section/div/section[2]/ul/li/a').text
    telefone = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/section/div/section[3]/ul/li/span[1]').text
    email = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div[2]/section/div/section[4]/div/a').text

    dadosUsuario['informacoesPessoais']['perfilLinkedIn'] = linkedin
    dadosUsuario['informacoesPessoais']['links'].append(link)
    dadosUsuario['informacoesPessoais']['telefone'] = telefone
    dadosUsuario['informacoesPessoais']['email'] = email


    fechar = driver.find_element(By.XPATH, '//*[@class="artdeco-modal__dismiss artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view"]').click()
    sleep(2)


    sobre = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[2]/div/div/main/section[4]/div[3]/div/div/div/span[1]').text
    dadosUsuario['sobre'] = sobre


    irExperiencias = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[2]/div/div/main/section[6]/div[2]/div/div[2]/div[2]/a').click()
    sleep(2)


    listExperiencia = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul')
    #quantidade de experiencias
    qtdExperiencias = len(listExperiencia.find_elements(By.XPATH, 'li'))
    dadosExperiencia = []
    for experiencia in range(qtdExperiencias):
        cargo = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{experiencia+1}]/div/div/div[2]/div[1]/div[1]/div/span/span[1]').text
        EmpresaTipo = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{experiencia+1}]/div/div/div[2]/div[1]/div[1]/span[1]/span[1]').text
        periodo = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{experiencia+1}]/div/div/div[2]/div[1]/div[1]/span[2]/span[1]').text
        localizacao = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{experiencia+1}]/div/div/div[2]/div[1]/div[1]/span[3]/span[1]').text
        competencias = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{experiencia+1}]/div/div/div[2]/div[2]/ul/li/div/ul/li/div/div/div/span[1]').text
        dadosExperiencia.append({
            'cargo':cargo,
            'EmpresaTipo':EmpresaTipo,
            'periodo':periodo,
            'localizacao':localizacao,
            'competencias':competencias,
        })

    voltar = driver.find_element(By.XPATH, '//*[@class="artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--3 artdeco-button--tertiary ember-view"]').click()
    sleep(2)
    dadosUsuario['experiencia'] = dadosExperiencia



    irFormacoes = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[2]/div/div/main/section[7]/div[2]/div/div[2]/div[2]/a').click()
    sleep(2)


    formacoes = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul')
    qtdformacoes = len(formacoes.find_elements(By.XPATH, 'li'))
    dadosFormacoes = []
    for formacao in range(qtdformacoes):
        instituicao = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{formacao+1}]/div/div/div[2]/div[1]/a/div/span/span[1]').text
        curso = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{formacao+1}]/div/div/div[2]/div[1]/a/span[1]/span[1]').text
        periodo = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{formacao+1}]/div/div/div[2]/div[1]/a/span[2]/span[1]').text

        dadosFormacoes.append({
            'instituicao':instituicao,
            'curso':curso,
            'periodo':periodo,
        })

    voltar = driver.find_element(By.XPATH, '//*[@class="artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--3 artdeco-button--tertiary ember-view"]').click()
    sleep(2)
    dadosUsuario['formacoes'] = dadosFormacoes


    irLicencas = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[2]/div/div/main/section[8]/div[2]/div/div[2]/div[2]/a').click()
    sleep(2)

    certificadosLicencas = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul')
    qtdcertificadosLicencas = len(certificadosLicencas.find_elements(By.XPATH, 'li'))
    dadosCertificadosLicencas = []
    for certificadoLicenca in range(qtdcertificadosLicencas):
        titulo = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{certificadoLicenca+1}]/div/div/div[2]/div[1]/a/div/span/span[1]').text
        instituicao = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{certificadoLicenca+1}]/div/div/div[2]/div[1]/a/span[1]/span[1]').text
        periodo = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{certificadoLicenca+1}]/div/div/div[2]/div[1]/a/span[2]/span[1]').text

        dadosCertificadosLicencas.append({
            'titulo':titulo,
            'instituicao':instituicao,
            'periodo':periodo,
        })

    voltar = driver.find_element(By.XPATH, '//*[@class="artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--3 artdeco-button--tertiary ember-view"]').click()
    sleep(2)
    dadosUsuario['certificadosLicencas'] = dadosCertificadosLicencas



    irCompetencias = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[2]/div/div/main/section[9]/div[2]/div/div[2]/div[2]/a').click()
    sleep(2)

    competencias = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul')
    qtdcompetencias = len(competencias.find_elements(By.XPATH, 'li'))
    dadosCompetencias = []
    for competencia in range(qtdcompetencias):
        nome = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div[2]/div/div/div[1]/ul/li[{competencia+1}]/div/div/div[2]/div[1]/a/div/span/span[1]').text
        
        dadosCompetencias.append({
            'nome':nome,
        })

    voltar = driver.find_element(By.XPATH, '//*[@class="artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--3 artdeco-button--tertiary ember-view"]').click()
    dadosUsuario['competencias'] = dadosCompetencias
    sleep(2)
        


    irProjetos = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[2]/div/div/main/section[10]/div[2]/div/div[2]/div[2]/a').click()
    sleep(2)

    projetos = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul')
    qtdprojetos = len(projetos.find_elements(By.XPATH, 'li'))
    dadosProjetos = []
    for projeto in range(qtdprojetos):
        titulo = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{projeto+1}]/div/div/div[2]/div[1]/div[1]/div/span/span[1]').text
        
        try:
            periodo = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{projeto+1}]/div/div/div[2]/div[1]/div[1]/span/span[1]').text
        except:
            periodo = None
        try:
            associado = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{projeto+1}]/div/div/div[2]/div[2]/ul/li[1]/div/div[2]/div/div/span[1]').text
        except:
            associado = None
        descricao = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{projeto+1}]/div/div/div[2]/div[2]/ul/li[2]/div/ul/li/div/div/div/span[1]').text
        try:
            link = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{projeto+1}]/div/div/div[2]/div[2]/ul/li[1]/div/a').get_attribute('href')
        except:
            link = None
        
        dadosProjetos.append({
            'titulo':titulo,
            'periodo':periodo,
            'associado':associado,
            'descricao':descricao,
            'link':link,
        })

    voltar = driver.find_element(By.XPATH, '//*[@class="artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--3 artdeco-button--tertiary ember-view"]').click()
    dadosUsuario['projetos'] = dadosProjetos
    sleep(2)


    irIdiomas = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div/div[2]/div/div/main/section[11]/div[2]/div/div[2]/div[2]/a').click()
    sleep(2)

    idiomas = driver.find_element(By.XPATH, '/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul')
    qtdidiomas = len(idiomas.find_elements(By.XPATH, 'li'))
    dadosIdiomas = []
    for idioma in range(qtdidiomas):
        nome = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{idioma+1}]/div/div/div[2]/div/div[1]/div/span/span[1]').text
        nivel = driver.find_element(By.XPATH, f'/html/body/div[5]/div[3]/div/div/div[2]/div/div/main/section/div[2]/div/div[1]/ul/li[{idioma+1}]/div/div/div[2]/div/div[1]/span/span[1]').text


        dadosIdiomas.append({
            'nome':nome,
            'nivel':nivel,
        })

    voltar = driver.find_element(By.XPATH, '//*[@class="artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--3 artdeco-button--tertiary ember-view"]').click()
    dadosUsuario['idiomas'] = dadosIdiomas
    sleep(2)

    driver.quit()   

    return Response(dadosUsuario)
