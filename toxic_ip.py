import re
import paramiko 

host = '88.198.9.173'
user = 'eiz'
port = 49022
password = 'dq17tYPy'

path_file_log_nginx = '/var/log/nginx/'
name_file_error_log_nginx = 'error.log'
name_file_acces_log_nginx = 'access.log'

path_file_log_httpd = '/var/log/httpd/'
name_file_error_log_httpd = 'error_log'
name_file_acces_log_httpd = 'access_log'

set_log = set()


re_expression = r"(?:wget|[.]env|wp-login|wp-content).*\"(\d{,3}[.]\d{,3}[.]\d{,3}[.]\d{,3})"
re_expression_route = r"address=(\d{,3}.\d{,3}.\d{,3}.\d{,3})"
name_list = 'Drop_list'

re_expression_accces_httpd = r"(?:wget|[.]env|wp-login|wp-content).*/(\d{,3}[.]\d{,3}[.]\d{,3}[.]\d{,3})"
re_expression_errors_httpd = r"client\s*(\d{,3}[.]\d{,3}[.]\d{,3}[.]\d{,3}).*(?:wget|[.]env|wp-login|wp-content)"
re_expression_errors_nginx = r"client:\s*(\d{,3}[.]\d{,3}[.]\d{,3}[.]\d{,3}).*(?:wget|[.]env|wp-login|wp-content)"
try:
   with open(f'{path_file_log_nginx}{name_file_error_log_nginx}', 'r') as log:
      text = log.read()
      set_log= set_log | set(re.findall(re_expression_errors_nginx, text))

   with open(f'{path_file_log_nginx}{name_file_acces_log_nginx}', 'r') as log:
      text = log.read()
      set_log= set_log | set(re.findall(re_expression_accces_httpd, text))

   with open(f'{path_file_log_httpd}{name_file_error_log_httpd}', 'r') as log:
      text = log.read()
      set_log= set_log | set(re.findall(re_expression_errors_httpd, text))

   with open (f'{path_file_log_httpd}{name_file_acces_log_httpd}', 'r') as log:
      text = log.read()
      set_log= set_log | set(re.findall(re_expression_accces_httpd, text))


   try:
      client = paramiko.SSHClient()
      client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      client.connect(hostname=host, username=user, port=port, password=password)
   except paramiko.ssh_exception.NoValidConnectionsError:
      print ('Неверный хост')
   except paramiko.BadHostKeyException:
      print ("не удалось проверить ключ хоста сервера")
   except paramiko.AuthenticationException :
      print ("проверка подлинности не удалась")
   except paramiko.SSHException :
      print ("произошла какая-либо другая ошибка при подключении или установлении сеанса SSH")
   except:
      print ("неизвестная ошибка проверьте данные")
   else:
      stdin, stdout, stderr = client.exec_command('/ip fi ad export')
      set_spam_rout = set(re.findall(re_expression_route, str(stdout.read())))

      not_in_blocked_list = set_log.difference(set_spam_rout) 
      for itter in not_in_blocked_list:
         stdin, stdout, stderr = client.exec_command(f'/ip fi ad add address="{itter}" list={name_list}')
      stdout.read()
      print (f'Добавлено новых IP адресов: {len(not_in_blocked_list)}')
      client.close()
except FileNotFoundError as file_exeption:
   print (f'Файл не найден: {file_exeption.filename}')




