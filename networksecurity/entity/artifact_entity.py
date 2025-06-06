## We created this .py file becoz after data ingestion we  need to the data ingestion artifacts 
from dataclasses import dataclass
# it is done to import dataclass decorator from the dataclasses library 
#dataclasses simplify the creation of classes that are primarily used to store data.

@dataclass 
class DataIngestionArtifact:
    trained_file_path:str 
    test_file_path:str