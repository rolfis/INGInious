import web


session = None

def init(app):
    """ Init the session. Should be call before starting the web.py server """
    global session
    if web.config.get('_session') is None:
        session = web.session.Session(app, web.session.DiskStore('sessions'), {'count': 0})
        web.config._session = session
    else:
        session = web.config._session