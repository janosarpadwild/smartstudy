import datetime, os
def crash_report(error_message, error_code):
    if not os.path.isdir('crash-reports'):
        os.mkdir('crash-reports')
    file = f'crash-reports/crash-{datetime.datetime.now()}.txt'.replace(' ', '_').replace(':', '.')
    with open(file,'a',encoding='utf-8') as log:
        log.write(f'{error_message}\n{error_code}\n')
