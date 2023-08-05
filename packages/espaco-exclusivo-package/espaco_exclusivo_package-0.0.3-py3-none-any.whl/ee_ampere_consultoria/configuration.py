# -*- coding: utf-8 -*-
"""
    --------------------------------------------------------------------------------------------------------------------

    Description: 
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Obs.: 

    Author:           @diego.yosiura
    Last Update:      21/07/2021 14:56
    Created:          21/07/2021 14:56
    Copyright:        (c) Ampere Consultoria Ltda
    Original Project: espaco_exclusivo_package
    IDE:              PyCharm
"""
import re
import sys
import traceback

from datetime import datetime


class Configuration:
    ERROR_TEMPLATE = """
    # ######################################################################################################################
    # Title: {title}
    # Date: {exception_date}
    # Description: {description}
    # File Name: {file_name}
    # Code Line: {code_line}
    # Code Name: {code_name}
    # Exception Type: {exception_type}
    #
    # ----------------------------------------------------------------------------------------------------------------------
    # [TRACEBACK]
    # ===========
    # 
    # {traceback}
    # ######################################################################################################################
    """

    Debug = True
    BaseURL = 'https://exclusivo.ampereconsultoria.com.br'
    URI = {
        'auth': {
            'get_auth_code': ['{}/automated-login/'.format(BaseURL), 'PUT'],
            'check_user_permission': ['{}/admin/contratos/current-user-has-permission/'.format(BaseURL), 'GET']
        },
        'file_viewer': {
            'list': ['{}/produtos/file-viewer/get-file-list/'.format(BaseURL), 'GET'],
            'download': ['{}/produtos/file-viewer/get-file/'.format(BaseURL), 'GET']
        },
        'meteorologia': {
            'get_images': ['{}/produtos/meteorologia/imagens-clima/'.format(BaseURL), 'GET'],
            'comparador': ['{}/produtos/meteorologia/comparador-imagens-clima/'.format(BaseURL), 'POST']
        },
        'flux': {
            'automatico': {
                'get_list': ['{}/produtos/previvaz-automatico/get-list/'.format(BaseURL), 'GET'],
                'download_zip': ['{}/produtos/previvaz-automatico/get-zip/'.format(BaseURL), 'GET']
            },
            'historico': {
                'get_data': ['{}/produtos/previvaz-historico/get-data/'.format(BaseURL), 'GET'],
                'download_zip': ['{}/produtos/previvaz-historico/download-data/'.format(BaseURL), 'GET']
            }
        }
    }

    @staticmethod
    def get_uri(uri):
        try:
            ref = Configuration.URI.copy()
            spl_uri_args = str(uri).split('?')
            spl_uri = str(spl_uri_args[0]).split('.')
            for u in spl_uri:
                ref = ref[u]
            if len(spl_uri_args) == 2:
                ref[0] += '?' + spl_uri_args[1]
            return ref
        except Exception as e:
            error = "[EE RequestManager] - Erro não tratado: {}\nURI Ref: {}".format(str(e), uri)
            Configuration.debug_print(error, e)
            raise Exception(error)

    @staticmethod
    def debug_print(message, exception=None):
        if Configuration.Debug:
            if exception is not None:
                e_type, e_value, e_traceback = sys.exc_info()
                print(Configuration.ERROR_TEMPLATE.format(
                    title=message,
                    description='\n#              '.join(str(exception).split('\n')),
                    file_name=str(e_traceback.tb_frame.f_code.co_filename),
                    code_line=str(e_traceback.tb_lineno),
                    code_name=str(e_traceback.tb_frame.f_code.co_name),
                    exception_type=str(e_type.__name__),
                    exception_date=datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S'),
                    traceback=re.sub(r'\n', '\n# ', traceback.format_exc())
                ))

        else:
            print(message)
