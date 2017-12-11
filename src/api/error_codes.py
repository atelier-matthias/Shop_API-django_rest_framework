from rest_framework.response import Response


def HTTP409Response(message):
    return Response({'message': message[0], 'code': message[1]}, status=409)

def HTTP404Response(message):
    return Response({'message': message[0], 'code': message[1]}, status=404)



class ErrorCodes(dict):

    RESULT_OK = ('success', 200)

    ORDER_NOT_FOUND = (1001, "order not found")

    EMAIL_ALREADY_REGISTERED = ('email already used', 2001)

    USER_OR_PASSWORD_NOT_MATCH = ('user or password not match', 3001)

    STOCK_ALREADY_CREATED = ('stocks with this product and shop already created', 4001)