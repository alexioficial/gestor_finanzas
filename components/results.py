from typing import List, Dict, Optional

class InsertOneResult:
    def __init__(self, inserted_id: int):
        self.inserted_id = inserted_id

    def __repr__(self):
        return f"<InsertOneResult inserted_id={self.inserted_id}>"

class DeleteResult:
    def __init__(self, deleted_count: int):
        self.deleted_count = deleted_count

    def __repr__(self):
        return f"<DeleteResult deleted_count={self.deleted_count}>"

class UpdateResult:
    def __init__(self, matched_count: int, modified_count: int):
        self.matched_count = matched_count
        self.modified_count = modified_count

    def __repr__(self):
        return f"<UpdateResult matched_count={self.matched_count}, modified_count={self.modified_count}>"

class SelectResult:
    def __init__(self, documents: list[dict], count: int, limit: int = None):
        self.documents = documents
        self.count = count
        self.limit = limit

    def __iter__(self):
        return iter(self.documents)

    def __len__(self):
        return len(self.documents)

    def __getitem__(self, index):
        return self.documents[index]

    def __repr__(self):
        return f"SelectResult(count={self.count}, limit={self.limit}, documents={self.documents})"