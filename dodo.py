def task_hello():
    """hello cmd """
    msg = 3 * "hi! "
    return {
        'actions': ['echo %s ' % msg],
        }

def task_python_version():
    return {
        'actions': [['python', '--version']]
        }