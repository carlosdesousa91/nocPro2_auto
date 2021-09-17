# nocPro2_auto

O NOC Pro Auto 2 realiza abertura automatica de tickets no topdesk através do rescurso de notificações do centreon, sem a nacessidade de autorização do analista.

#### Configuração

No poller clonar este repositorio em /usr/share/centreon

Criar o arquivo nocPro_access.py

```
#!/usr/bin/python3
#coding: utf-8

#variaveis conexão
ip_centreon =  ""
user_autoLogin_centreon = ""
token_autoLogin_centreon = ""

rule_data = {
    'address': '',
    'path': '/tas',
    'username': '',
    'password': ''
}
```

No centreon central pela web criar o comando de notificação seguinte:

Host:

```
/usr/share/centreon/nocPro2_auto/nocPro2_auto.py "$CONTACTNAME$" "$CONTACTEMAIL$" "3641" "$HOSTID$" "$LASTHOSTCHECK$" "$HOSTSTATE$" "$HOSTALIAS$" "$HOSTALIAS$" "$HOSTNOTES$" "$LASTHOSTCHECK$" "$HOSTALIAS$" "PoP"
```
Service:

```
/usr/share/centreon/nocPro2_auto/nocPro2_auto.py "$CONTACTNAME$" "$CONTACTEMAIL$" "3641" "$HOSTID$" "$LASTSERVICECHECK$" "$SERVICESTATE$" "$SERVICEDESC$" "$HOSTALIAS$" "$SERVICENOTES$" "$LASTHOSTCHECK$" "$HOSTALIAS$" "PoP"
```
No centreon central pela web definir o comando criado para notificação do usuário desejado.

No centreon central pela web habilitar a notificação para host/service desejados.

### RN001 - preenchimento da hora de normalização automaticamente

- sempre que um ticket estiver com a hora de normalização null e a notificação do centreon for do tipo UP/OK ele será atualizado.
- Se o ticket ja estiver com a hora da normalização preenchida e com status "retomar contato" ele não será atualizado.
- Ticket com o Status "retomar contato" somente será atualizado se a hora da normalização estiver Null.
- O campo Registro do chamado deve estar preenchido com "Monitoramento".

### RN002 - Ativos que não possuem Ics cadastrados no centreon

- O IC é "montado" usando a seguinte estrutura : "CENTREON_" + host_id + "_" + service_id 

### RN003 - Envio e-mail normalização

- incluir metodo de envio de email no arquivo nocPro_mail.py
