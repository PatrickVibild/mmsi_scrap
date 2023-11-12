class ShipData:
    def __init__(self, mmsi, type_g, build_year, length, breath, tonnage):
        self.mmsi = str(mmsi)
        self.generic_type = type_g
        self.build_year = build_year
        self.length = length
        self.breath = breath
        self.tonnage = tonnage

    def to_dict(self):
        return {
            '_id': self.mmsi,
            'mmsi': self.mmsi,
            'generic_type': self.generic_type,
            'build_year': self.build_year,
            'length': self.length,
            'breath': self.breath,
            'gross_tonnage': self.tonnage
        }