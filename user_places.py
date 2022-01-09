import geopy.distance

class UserPlaces:
    def __init__(self, places, user):
        self.user = user
        self.sorted_places = self.__get_sorted_distances__(places)
        self.within_range = self.__places_within_range__()

    def __places_within_range__(self):
        within_range = []
        for distance, place in self.sorted_places:
            if distance <= self.user.range:
                within_range.append((distance, place))
        return within_range

    def __get_sorted_distances__(self, places):
        distances = []
        user_coords = (self.user.lat, self.user.lng)

        for place in places:
            if place.get('status') != "NO_STOCK":
                distances.append((self.__get_distance__(place, user_coords), place))

        return sorted(distances, key=lambda x: x[0])

    def __get_distance__(self, place, user_coords):
        coords = (place.get('lat'), place.get('lng'))
        return geopy.distance.distance((user_coords), coords).km