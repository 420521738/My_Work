

params = {'get_configuration': '/api/configuration/1/?format=json',
          'post_monitor_data': '/api/monitor_data/',
          'get_asset_id': '/api/asset/',
          'config_md5': None,
          'server': '127.0.0.1',
          'port':8001,
          
          
          #########below for task allocation########
          
          'get_host_profile': '/api/host_profile/2/?format=json',
          'new_tasks': '/api/new_tasks',
          'report_result': '/api/task_result/',
          'task_log_path':'logs/tasks',
          #'last_task_id' : 'var\last_task_id',
          'last_task_id' : 'var/last_task_id',
          }
