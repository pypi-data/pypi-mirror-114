def validate(request, validation_data):
    '''Validate incoming payload.
    :param request: `CherryPy request <http://docs.cherrypy.org/en/latest/pkg/cherrypy.html#cherrypy._cprequest.Request>`_ instance representing incoming request
    :param validation_data: dict with validation data, e.g. ``owner``, ``repo``, ``branches``, extracted from the app config
    :returns: namedtuple(status, message, list of extracted params as dicts), e.g. ``Response(status=200, message='Payload validated. Branches: default', [{'branch': 'default'}])``
    '''

    from collections import namedtuple


    Response = namedtuple('Response', ('status', 'message', 'param_dicts'))

    return Response(200, 'Payload validated. Branches: default', [{'branch': 'default'}])

