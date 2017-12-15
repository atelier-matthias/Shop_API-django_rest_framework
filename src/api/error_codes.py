from rest_framework.response import Response


def HTTP409Response(message):
    return Response({'message': message[0], 'code': message[1]}, status=409)


def HTTP404Response(message):
    return Response({'message': message[0], 'code': message[1]}, status=404)


def HTTP500Response(message):
    return Response({'message': message[0], 'code': message[1]}, status=500)


class ErrorCodes(dict):

    RESULT_OK = ('success', 200)

    ORDER_NOT_FOUND = ("order not found", 1001)
    ORDER_NOT_CREATED = ("order not created", 1002)

    PRODUCT_ALREADY_IN_BUCKET = ("Product already in bucket", 1041)
    PRODUCT_NOT_AVALIABLE = ('Product not avaliable', 1042)
    NOT_ENOUGH_PRODUCTS_IN_MAGAZINES = ('not enough products in magazines', 1043)

    BUCKET_IS_EMPTY = ("bucket is empty", 1083)
    ADD_PRODUCT_TO_BUCKET_ERROR = ('product not added to bucker', 1084)

    EMAIL_ALREADY_REGISTERED = ('email already used', 2001)

    USER_OR_PASSWORD_NOT_MATCH = ('user or password not match', 3001)

    STOCK_ALREADY_CREATED = ('stocks with this product and shop already created', 4001)