import random

from src.Client.Implementation.client import Client

if __name__ == '__main__':
    client = Client(f'client{random.randint(1, 100)}')
    client.run()
