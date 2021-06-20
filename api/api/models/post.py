"""
Post model of DB object
"""

from . import Base, Attribute


class Post(Base):
    """ Post """

    _db = 'posts'
    reactions = Attribute(dict, {
        'views': [], # TODO: + UTM
        'likes': [],
        'reposts': [],
        'comments': [],
    }) # TODO: attributes
    cont = Attribute(str, '')
    cover = Attribute(str)
    # TODO: language
    # TODO: category
    # TODO: tags
    # TODO: source
    # TODO: actions
