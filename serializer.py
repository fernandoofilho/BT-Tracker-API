class Serializer: 
    
    @staticmethod
    def serialize_data(data):
        return data
    
    @staticmethod
    def serialize_many(data):
        data = {
            "items": data 
        }
        return data