#!/usr/bin/python3
#coding: utf-8
import io
import sys
#import requests
import json
#import smtplib
#from email.mime.text import MIMEText
import nocPro_access
import traceback
from _class import topdesk_class
import nocPro_mail
import datetime

try:

    ##argumentos centreon
    user_centreon = sys.argv[1]
    user_centreon = user_centreon.replace("_", " ")
    userEmail_centreon = sys.argv[2]
    servico_otrs = sys.argv[3]
    service_id_centreon = sys.argv[4]
    hora_evento_centreon = sys.argv[5]
    hora_evento_centreon = datetime.datetime.fromtimestamp(int(hora_evento_centreon)).strftime('%Y-%m-%dT%H:%M:%S.000') + '+03'
    service_status_centreon = sys.argv[6]
    service_desc_centreon = sys.argv[7]
    service_nome_centreon = sys.argv[8]
    service_note_centreon = sys.argv[9]
    hora_eventoEp_centreon = sys.argv[10]
    hora_eventoEp_start = int(hora_eventoEp_centreon) - 10800
    host_name_centreon = sys.argv[11]
    conexao_centreon = sys.argv[12]

    #params = otrs_class.testa_sessao();
    verifica_ticket = topdesk_class.verificaTicket(service_note_centreon, hora_evento_centreon, nocPro_access.rule_data)
    #print(verifica_ticket)
    ticket_existente = verifica_ticket

    #não tem ticket e é uma falha
    if ticket_existente == 0 and service_status_centreon != "UP" and service_status_centreon != "OK":
        #buscar campos para abertura do ticket
        campos = topdesk_class.camposTicket(
            nocPro_access.rule_data,
            service_status_centreon,
            service_note_centreon,
            service_desc_centreon,
            user_centreon,
            userEmail_centreon,
            hora_evento_centreon
        )
        # criar ticket
        TicketAberto_value = topdesk_class.cria_ticket(
            nocPro_access.rule_data,
            campos
            #service_desc_centreon,
            #service_status_centreon,
            #hora_eventoEp_start,
            #hora_eventoEp_centreon,
            #host_name_centreon,
            #user_centreon,
            #userEmail_centreon,
            #hora_evento_centreon,
            #email_cliente,
            #service_id_centreon,
            #servico_otrs,
            #ic_local_uf,
            #conexao_centreon,
            #service_note_centreon
        )

        erro_valor = "não houve erro, ticket foi aberto."  + str(TicketAberto_value)

    #não tem ticket e é uma normalização
    elif ticket_existente == 0 and (service_status_centreon == "UP" or service_status_centreon == "OK"):
        #notificar informando que o ticket não foi aberto.
        erro_valor = "não houve erro, não há ticket a ser fechado."

    #tem ticket e é uma falha
    elif ticket_existente != 0 and service_status_centreon != "UP" and service_status_centreon != "OK":
        #atualiza o ticket
        erro_valor = "não houve erro, ticket foi atualizado. " + str(ticket_existente[0])

    #tem ticket e é uma normalização
    else:    
        #fecha o ticket
        erro_valor = "não houve erro, ticket foi finalizado. " + str(ticket_existente[0])


    ##envia email
    nocPro_mail.envia_email(sys.argv, erro_valor)
    ##Encerra request
    #requests.session().close()




except Exception:
    erro_valor = traceback.format_exc()
    ##envia email
    nocPro_mail.envia_email(sys.argv, erro_valor)
    ##Encerra request
    #requests.session().close()

##Criado por - Carlos Araújo de Sousa
##carlos.sousa@terceiro.rnp.br
##carlos.desousa91@outlook.com
## NOC - RNP - Rede Nacional de Ensino e pesquisa
