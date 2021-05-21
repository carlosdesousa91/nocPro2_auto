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
        
    
    s.close()

    if response.json():
        data_json = response.json()
        return data_json[0]['id'], data_json[0]['number']
    else:
        return 0
    
    #return recuperado_id, ticket_existente, sessao_recuperado_id;
    #return data_json;


def cria_ticket(
    rule_data, 
    service_desc_centreon, 
    service_status_centreon,
    hora_eventoEp_start, 
    hora_eventoEp_centreon, 
    host_name_centreon, 
    user_centreon, 
    userEmail_centreon, 
    hora_evento_centreon, 
    email_cliente,
    service_id_centreon, 
    servico_otrs, 
    ic_local_uf, 
    conexao_centreon,
    service_note_centreon
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

            'request': service_desc_centreon,
            'briefDescription': service_desc_centreon,
            'callerLookup': [
                {'email': 'carlos.sousa@terceiro.rnp.br'}
            ],
            #o campo type refere-se ao tipo de chamado, incidente, requisição, etc. No contexto do nocpro ele será usada para outro fim e todos os chamado serão do tipo Incidente
            'callType': [
                {'name': 'Incidente'}
            ],
            'category': [
                {'id': '989624e9-4b7f-4bef-ab65-aa6135d52299'}
            ],
            'subcategory': [
                {'id': 'a0a77087-9029-4dcd-a8ab-13a40c8df466'}
            ],
            'object': [
                {'name': service_note_centreon}
            ],
            'sla': [
                {'id': 'cf6b5764-649e-49b9-abee-5277f1b84c3f'}
            ],
            'operator': [
                {'id': 'dc32c755-d276-4d71-a8ed-4ffd1c3f1176'}
            ],
            'operatorGroup': [
                {'id': 'dc32c755-d276-4d71-a8ed-4ffd1c3f1176'}
            ],
            'processingStatus': [
                {'id': 'a3e2ad64-16e2-4fe3-9c66-9e50ad9c4d69'}
            ],
            'optionalFields1': [
                {'date1': hora_evento_centreon}
            ],
            'entryType': [
                {'name': 'Monitoramento'}
            ]

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