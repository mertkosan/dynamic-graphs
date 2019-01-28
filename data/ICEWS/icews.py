import pandas as pd
import os


class ICEWS():
    def __init__(self):
        self._data_folder = "./data"
        self._data_files = ["events.2018.tsv"]

    def get_statistics(self):
        for file in self._data_files:
            print("Statistics for file: %s\n" % file)
            path = os.path.join(self._data_folder, file)
            df = pd.read_csv(path, sep="\t", header=0)
            print("Number of nodes: %d" % self.number_of_nodes(df))
            print("Number of edges: %d" % self.number_of_edges(df))
            print("Number of nonnull:\n%s" % str(self.number_of_nonnull(df)))
            print("Number of unspecified target: %d" % self.number_of_unspecified_target(df))
            print("Number of event types: %d" % self.number_of_event_types(df))

    def number_of_nodes(self, df: pd.DataFrame):
        # based on "Source Name" and "Target Name"
        source = set(df["Source Name"])
        target = set(df["Target Name"])
        return len(source.union(target))

    def number_of_edges(self, df: pd.DataFrame):
        return len(df["Event ID"])

    def number_of_nonnull(self, df: pd.DataFrame):
        return df.count()

    def number_of_unspecified_target(self, df: pd.DataFrame):
        return len(df[df["Target Name"] == "Unspecified Actor"])

    def number_of_event_types(self, df: pd.DataFrame):
        return len(set(df["Event Text"]))


icews = ICEWS()
icews.get_statistics()
