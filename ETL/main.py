from config import Config, Queries
from load import ElasticSearchLoader
from machine_states import Extract, Init, Load, SleepMode
from postgres_reader import PostgresReader


class ETL:
    def __init__(self, config: Config, queries: Queries):
        self.config = config
        self.queries = queries
        self.postgres = PostgresReader(connect_data=self.config.DSL,
                                       limit=self.config.LIMIT)
        self.elastic = ElasticSearchLoader(config.ELASTICSEARCH_URL,
                                           config.INDEX, config.INDEX_NAME)

        self.init = Init(self, self.postgres)
        self.extract = Extract(self, self.postgres)
        self.load = Load(self, self.elastic)
        self.sleep_mode = SleepMode(self)

        self.state = self.init

    def run_state(self):
        '''Запуск стартового состояния'''
        self.state.run()


if __name__ == '__main__':
    config = Config()
    queries = Queries()
    etl = ETL(config, queries)
    etl.run_state()
