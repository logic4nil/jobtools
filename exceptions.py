# -*- coding: utf-8 -*-

class ProjectError(RuntimeError):
    def __init__(self, *args, **kwargs):
        super(ProjectError, self).__init__(*args, **kwargs)

class ProjectConfigError(ProjectError):
    pass

class ProjectFileNotExistError(ProjectError):
    ''' Project File Not Exists '''
    pass

class TypeNotMatchError(ProjectError):
    pass

class ExpressionError(ProjectError):
    '''
    Expression Error
    '''
    pass
