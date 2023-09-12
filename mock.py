class MockScalarResult:
    @staticmethod
    def first():
        return {
            "id": 0,
            "name": "string",
            "cost": 0,
            "brand": "string",
            "size": "string",
            "added_at": "2023-09-12T09:09:47.756000",
            "description": "string",
            "rating": 0,
            "amount": 0,
            "type": "string"
        }


class MockResult:
    def scalars(self):
        return MockScalarResult()

class MockAsyncSession:
    def execute(self, statement):
        return MockResult()

session = MockAsyncSession()
query = "fdasfkjsd"
result = session.execute(query)
print(result)
res = result.scalars().first()
print(res)