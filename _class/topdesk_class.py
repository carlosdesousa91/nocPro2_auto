#!/usr/bin/python3
#coding: utf-8
import io
import sys
import requests
import json
#import smtplib
#from email.mime.text import MIMEText
#import nocPro_access
#import traceback
import base64


def verificaTicket(id_relacinamento, horadafalha, rule_data):
    
    with requests.Session() as s:
        #s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
        
        base_url = 'https://'
        base_url += rule_data['address']
        base_url += rule_data['path'] + '/api';
        base_url += '/incidents?fields=id,number,optionalFields1.date1&'
        base_url += 'object_name=' + id_relacinamento + '&'
        #estados em atendimento, abertos, retomar contato, encaminhado, Aguardando fornecedor
        base_url += 'processing_status=2817418e-5afc-4a8e-b2e4-7e4ff104e095&processing_status=a3e2ad64-16e2-4fe3-9c66-9e50ad9c4d69&processing_status=662d4cd8-f9d7-4ba1-bcae-3569c4ccc711&processing_status=a4008966-27b6-4163-9d75-2ca5edf5c171&processing_status=dc36014f-d7c2-4f84-a23f-129ed93ee5d5'

        api_user = rule_data['username']
        api_senha = rule_data['password']
        data_string = api_user + ":" + api_senha
        authorization = data_string.encode("utf-8")
        authorization = base64.b64encode(authorization)
        authorization = authorization.decode("utf-8")
        authorization = "Basic " + str(authorization)
                
        response = s.get(base_url, headers={'content-type': 'application/json', 'Authorization': authorization}, verify=False, stream=False)
        #data_json = response.json()
    
    s.close()
    try:
        data_json = response.json()
        return data_json[0]['id'], data_json[0]['number']
    except: 
        return 0

    #if data_json:
    #    return data_json[0]['id'], data_json[0]['number']
    #else:
    #    return 0
    
    #return recuperado_id, ticket_existente, sessao_recuperado_id;
    #return data_json;


def cria_ticket(
    rule_data,
    campos
    ):

    with requests.Session() as s:
    #s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
        
        base_url = 'https://'
        base_url += rule_data['address']
        base_url += rule_data['path'] + '/api';
        base_url += '/incidents'
        
        api_user = rule_data['username']
        api_senha = rule_data['password']
        data_string = api_user + ":" + api_senha
        authorization = data_string.encode("utf-8")
        authorization = base64.b64encode(authorization)
        authorization = authorization.decode("utf-8")
        authorization = "Basic " + str(authorization)

        ticket_create_json = {

            'request': campos['request'],
            'briefDescription': campos['briefDescription'],
            'callerLookup': {
                'email': campos['email_cliente']
            },
            #o campo type refere-se ao tipo de chamado, incidente, requisição, etc. No contexto do nocpro ele será usada para outro fim e todos os chamado serão do tipo Incidente
            'callType': {
                'name': 'Incidente'
            },
            'category': {
                'id': campos['category_id']
                
            },
            'subcategory': 
                {'id': campos['subcategory_id']}
            ,
            'object': 
                {'name': campos['object_name']}
            ,
            'sla': 
                {'id': campos['sla_id']}
            ,
            'operator': 
                {'id': campos['operator_id']}
            ,
            'operatorGroup': 
                {'id': campos['operatorgroup_id']}
            ,
            'processingStatus': 
                {'id': campos['processingStatus_id']}
            ,
            'optionalFields1': 
                {'date1': campos['hora_falha']}
            ,
            'entryType': 
                {'name': 'Monitoramento'}            

        }
                
        response = s.post(
            base_url, 
            headers={'content-type': 'application/json', 'Authorization': authorization}, 
            data=json.dumps(ticket_create_json),
            verify=False, 
            stream=False
        )

        data_json = response.json()
    
    s.close()

    return data_json


def camposTicket(
        rule_data,
        service_status_centreon,
        service_note_centreon,
        service_desc_centreon,
        user_centreon,
        userEmail_centreon,
        hora_evento_centreon
    ):

    specification = consultaAtivo(rule_data, service_note_centreon)
    specification = specification[0]['specification']

    campos = {
        'email_cliente': 'oper@ceo.rnp.br',
        'request': """Prezados,<br/><br/> O <b>""" + specification + "</b>encontra-se isolado:<br/> " + """Host indisponível: """ +
        service_desc_centreon + "<br/>status:" + service_status_centreon +
        """<br/><br/><b>Atenciosamente,</b><br/>""" + user_centreon + "<br/>" + userEmail_centreon +
        """<br/>RNP – Rede Nacional de Ensino e Pesquisa<br/>https://www.rnp.br""" ,
        'briefDescription': 'Abertura - Isolamento - ' + specification,
        'category_id': '989624e9-4b7f-4bef-ab65-aa6135d52299',
        'subcategory_id': 'a0a77087-9029-4dcd-a8ab-13a40c8df466',
        'object_name': service_note_centreon,
        'sla_id': 'd5940571-9b7d-4fc7-aec5-9c5a0475c2be',
        'operator_id': 'dc32c755-d276-4d71-a8ed-4ffd1c3f1176',
        'operatorgroup_id': 'dc32c755-d276-4d71-a8ed-4ffd1c3f1176',
        'processingStatus_id': 'a3e2ad64-16e2-4fe3-9c66-9e50ad9c4d69',
        'hora_falha': hora_evento_centreon
    }

    return campos


def consultaAtivo(rule_data, service_note_centreon):
    with requests.Session() as s:
        base_url = 'https://'
        base_url += rule_data['address']
        base_url += rule_data['path'] + '/api'
        base_url += "/assetmgmt/assets?fields=specification,name&$filter=name eq '" + service_note_centreon + "'"
        
        api_user = rule_data['username']
        api_senha = rule_data['password']
        data_string = api_user + ":" + api_senha
        authorization = data_string.encode("utf-8")
        authorization = base64.b64encode(authorization)
        authorization = authorization.decode("utf-8")
        authorization = "Basic " + str(authorization)
                
        response = s.get(base_url, headers={'content-type': 'application/json', 'Authorization': authorization}, verify=False, stream=False)
        data_json = response.json()
    s.close()

    return data_json['dataSet']


def normalizacao_ticket(
    rule_data,
    campos,
    ticket_id,
    service_desc_centreon,
    service_status_centreon
    ):

    with requests.Session() as s:
    #s.get('https://httpbin.org/cookies/set/sessioncookie/123456789')
        
        base_url = 'https://'
        base_url += rule_data['address']
        base_url += rule_data['path'] + '/api'
        base_url += '/incidents/id/' + ticket_id
        
        api_user = rule_data['username']
        api_senha = rule_data['password']
        data_string = api_user + ":" + api_senha
        authorization = data_string.encode("utf-8")
        authorization = base64.b64encode(authorization)
        authorization = authorization.decode("utf-8")
        authorization = "Basic " + str(authorization)

        ticket_create_json = {

            'processingStatus': 
                {'id': campos['processingStatus_id']}
            ,
            'optionalFields1': 
                {'date2': campos['hora_normaliza']}
            ,
            'action': """Prezados,<br/>O ativo encontra-se normalizado: """ + service_desc_centreon + 
            """<br/>status: """ + service_status_centreon +
            """<br/>O campo Hora da normalização foi atualizado"""
            #"""<br/><a href='https://monitoramento.rnp.br/centreon/monitoring/resources?details=%7B%22id%22%""" +
	        #    3A14632 +
            #    """%2C%22parentId%22%""" +
            #    3A205 +
            #    """%2C%22parentType%22%3A%22host%22%2C%22tab%22%3A%22timeline%22%2C%22type%22%3A%22service%22%2C%22uuid%22%3A%22%22%7D'>""" +
            #    """Conferir no centreon</a>"""

        }
                
        response = s.put(
            base_url, 
            headers={'content-type': 'application/json', 'Authorization': authorization}, 
            data=json.dumps(ticket_create_json),
            verify=False, 
            stream=False
        )

        data_json = response.json()
    
    s.close()

    return data_json