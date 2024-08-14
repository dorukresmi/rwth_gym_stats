from gym_stats.data_store import DataStore

class VisitorStatistics:
    def __init__(self, db_name, table_name):
        self.data_store = DataStore(db_name, table_name)

    def get_statistics(self):
        return self.data_store.get_only_numbers_and_timestamps()
    
    def get_all_data(self):
        return self.data_store.get_data()
    
    def run_query(self, query):
        return self.data_store.get_custom_query(query)

    def close(self):
        self.data_store.close()