def pretty_print(distance, place):
    price = "??.?" if place.get('priceInCents') is None else str(place.get('priceInCents')/100)

    msg = str(round(distance)) + "km: " \
            + place.get('status') \
            + " $" + price \
            + " for " + str(place.get('pricePerN')) \
            + " : " + place.get('address')
    print(msg)
    return msg