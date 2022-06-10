from time import sleep

from src.Business.log.logger import MyLogger
from src.Server.Implementation.server import Server

if __name__ == '__main__':
    server = Server()
    logger = MyLogger('project.main')
    logger.info('Starting server')
    server.run()
    logger.info('Server stopped')