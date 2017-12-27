import ast


class DefaultCommands(object):

    def str2dict(self, text):
        return ast.literal_eval(text)
