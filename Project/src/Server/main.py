from src.Business.log.logger import MyLogger
from src.Server.Implementation.server import Server

if __name__ == '__main__':
    server = Server()
    logger = MyLogger('project.main')
    try:
        logger.info('Starting server')
        server.run()
    except Exception as e:
        logger.error(f'Main error: {e}')
    finally:
        logger.info('Server stopped')
