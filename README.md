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

```
/usr/share/centreon/nocPro2_auto/nocPro2_auto.py "$CONTACTNAME$" "$CONTACTEMAIL$" "3641" "$HOSTID$" "$LASTHOSTCHECK$" "$HOSTSTATE$" "$HOSTALIAS$" "$HOSTALIAS$" "$HOSTNOTES$" "$LASTHOSTCHECK$" "$HOSTALIAS$" "PoP"
```

No centreon central pela web definir o comando criado para notificação do usuário desejado.

No centreon central pela web habilitar a notificação para host/service desejados.