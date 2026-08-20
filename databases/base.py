from abc import ABC, abstractmethod


class DatabaseAdapter(ABC):

    @abstractmethod
    def connect(self):
        """Establish database connection."""
        pass

    @abstractmethod
    def close(self):
        """Close database connection."""
        pass

    @abstractmethod
    def load_dataset(self, dataset_path):
        """Load the benchmark dataset."""
        pass

    @abstractmethod
    def point_lookup(self, node_id):
        """Find a single node."""
        pass

    @abstractmethod
    def traversal_1_hop(self, node_id):
        """Traverse one relationship from a node."""
        pass

    @abstractmethod
    def traversal_2_hop(self, node_id):
        """Traverse two relationships from a node."""
        pass

    @abstractmethod
    def traversal_3_hop(self, node_id):
        """Traverse three relationships from a node."""
        pass

    @abstractmethod
    def aggregation(self):
        """Execute the benchmark aggregation query."""
        pass