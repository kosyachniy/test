import time
import json

import pytest

from api.errors import ErrorWrong
from api.models import Base, Attribute


class ObjectModel(Base):
    _db = 'tests'

    meta = Attribute(types=str)
    delta = Attribute(types=str, default='')
    extra = Attribute(types=str, default=lambda instance: f'u{instance.delta}o')
    multi = Attribute(types=list, default=[])

class SubObject(Base):
    _db = None

    id = Attribute(types=str)
    taiga = Attribute(types=int)
    tundra = Attribute(types=int, default=0)


def test_attr():
    now = time.time()
    instance = ObjectModel()

    assert instance.id == 0
    assert instance.name is None
    assert instance.user == 0
    assert instance.created < now + 1
    assert instance.updated is None
    assert instance.status is None
    assert instance.meta is None
    assert instance.delta == ''
    assert instance.extra == 'uo'

    with pytest.raises(AttributeError):
        assert instance.undefined_field

def test_item():
    now = time.time()
    instance = ObjectModel()

    assert instance['id'] == 0
    assert instance['name'] is None
    assert instance['user'] == 0
    assert instance['created'] < now + 1
    assert instance['updated'] is None
    assert instance['status'] is None
    assert instance['meta'] is None
    assert instance['delta'] == ''
    assert instance['extra'] == 'uo'

    with pytest.raises(AttributeError):
        assert instance['undefined_field']

def test_data():
    now = time.time()
    instance = ObjectModel({
        'id': 1,
        'name': 'test_data',
        'user': 2,
        'status': 3,
        'meta': 'onigiri',
        'delta': 'hinkali',
        'extra': 'ramen',
    })

    assert instance.id == 1
    assert instance.name == 'test_data'
    assert instance.created < now + 1
    assert instance.user == 2
    assert instance.status == 3
    assert instance.meta == 'onigiri'
    assert instance.delta == 'hinkali'
    assert instance.extra == 'ramen'

def test_kwargs():
    now = time.time()
    instance = ObjectModel(
        id=1,
        name='test_kwargs',
        user=2,
        status=3,
        meta='oNiGiRi',
        delta='HINKali',
        extra='RAMEN',
    )

    assert instance.id == 1
    assert instance.name == 'test_kwargs'
    assert instance.created < now + 1
    assert instance.user == 2
    assert instance.status == 3
    assert instance.meta == 'oNiGiRi'
    assert instance.delta == 'HINKali'
    assert instance.extra == 'RAMEN'

def test_create_empty():
    instance = ObjectModel()

    now = time.time()
    instance.save()

    assert instance.id > 0
    assert instance.updated < now + 1

def test_create():
    instance = ObjectModel(
        name='test_create',
        meta='onigiri',
    )

    now = time.time()
    instance.save()

    assert instance.id > 0
    assert instance.updated < now + 1

def test_load():
    now = time.time()
    instance = ObjectModel(
        name='test_load',
        user=2,
        status=3,
        meta='onigiri',
        delta='hinkali',
        extra='ramen',
    )
    instance.save()

    recieved = ObjectModel.get(ids=instance.id)

    assert isinstance(recieved, ObjectModel)
    assert recieved.id == instance.id
    assert recieved.name == 'test_load'
    assert instance.created < now + 1
    assert instance.updated < now + 1
    assert instance.user == 2
    assert instance.status == 3
    assert recieved.meta == 'onigiri'
    assert recieved.delta == 'hinkali'
    assert recieved.extra == 'ramen'

def test_list():
    now = time.time()

    instance1 = ObjectModel(
        name='test_list',
        user=2,
        status=3,
        meta='onigiri',
        delta='hinkali',
        extra='ramen',
    )
    instance1.save()

    instance2 = ObjectModel()
    instance2.save()

    recieved = ObjectModel.get(ids=(
        instance1.id,
        instance2.id,
    ))

    assert isinstance(recieved, list)

    with recieved[1] as recieved1:
        assert isinstance(recieved1, ObjectModel)
        assert recieved1.id == instance1.id
        assert recieved1.name == 'test_list'
        assert recieved1.created < now + 1
        assert recieved1.updated < now + 1
        assert recieved1.user == 2
        assert recieved1.status == 3
        assert recieved1.meta == 'onigiri'
        assert recieved1.delta == 'hinkali'
        assert recieved1.extra == 'ramen'

    with recieved[0] as recieved2:
        assert isinstance(recieved2, ObjectModel)
        assert recieved2.id == instance2.id
        assert recieved2.created < now + 1
        assert recieved2.updated < now + 1

def test_update():
    instance = ObjectModel(
        name='test_create',
        delta='hinkali',
    )
    instance.save()

    assert instance.name == 'test_create'
    assert instance.meta is None
    assert instance.delta == 'hinkali'

    instance_id = instance.id
    instance = ObjectModel.get(ids=instance_id)

    instance.name = 'test_update'
    instance.meta = 'onigiri'

    instance.save()

    assert instance_id == instance.id

    instance = ObjectModel.get(ids=instance.id)

    assert instance.name == 'test_update'
    assert instance.meta == 'onigiri'
    assert instance.delta == 'hinkali'

def test_update_empty():
    instance = ObjectModel(
        name='test_create',
        meta='onigiri',
    )
    instance.save()

    assert instance.name == 'test_create'
    assert instance.meta == 'onigiri'

    instance_id = instance.id
    instance = ObjectModel.get(ids=instance_id)

    instance.name = None

    instance.save()

    assert instance_id == instance.id

    instance = ObjectModel.get(ids=instance.id)

    assert instance.name == 'test_create'
    assert instance.meta == 'onigiri'

def test_update_resave():
    instance = ObjectModel(
        name='test_create',
        delta='hinkali'
    )
    instance.save()

    instance_id = instance.id

    instance.name = 'test_update'
    instance.meta = 'onigiri'
    instance.save()

    assert instance_id == instance.id

    instance = ObjectModel.get(ids=instance.id)

    assert instance.name == 'test_update'
    assert instance.meta == 'onigiri'
    assert instance.delta == 'hinkali'

def test_rm():
    instance = ObjectModel()
    instance.save()

    instance.rm()

    with pytest.raises(ErrorWrong):
        ObjectModel.get(ids=instance.id)

def test_rm_nondb():
    instance = ObjectModel()

    with pytest.raises(ErrorWrong):
        instance.rm()

def test_rm_attr():
    instance = ObjectModel(
        meta='onigiri',
        delta='hinkali',
    )
    instance.save()

    instance = ObjectModel.get(ids=instance.id)

    del instance.meta
    instance.delta = 'hacapuri'

    instance.save()
    instance = ObjectModel.get(ids=instance.id)

    assert instance.meta is None
    assert instance.delta == 'hacapuri'

def test_rm_attr_resave():
    instance = ObjectModel(
        name='test_attr_resave',
        meta='onigiri',
        delta='hinkali',
    )
    instance.save()

    del instance.meta
    instance.delta = 'hacapuri'

    instance.save()
    instance = ObjectModel.get(ids=instance.id)

    assert instance.name == 'test_attr_resave'
    assert instance.meta is None
    assert instance.delta == 'hacapuri'

def test_init_sub():
    sub = SubObject(
        taiga=0,
    )

    assert isinstance(sub.id, str)
    assert len(sub.id) == 32
    assert sub.taiga == 0
    assert sub.tundra == 0

def test_init_sub_with_id():
    sub = SubObject(
        id='1',
        tundra=1,
    )

    assert sub.id == '1'
    assert sub.taiga is None
    assert sub.tundra == 1

def test_init_with_sub():
    sub = SubObject(
        taiga=1,
    )
    instance = ObjectModel(
        multi=[sub.json(default=False)],
    )

    with SubObject(instance.multi[0]) as recieved:
        assert recieved.id == sub.id
        assert recieved.taiga == 1
        assert recieved.tundra == 0

def test_create_with_sub():
    sub = SubObject(
        taiga=1,
    )
    instance = ObjectModel(
        multi=[sub.json(default=False)],
    )

    instance.save()

    assert instance.id > 0

    instance = ObjectModel.get(ids=instance.id)

    with SubObject(instance.multi[0]) as recieved:
        assert recieved.id == sub.id
        assert recieved.taiga == 1
        assert recieved.tundra == 0

def test_get_with_fields():
    instance = ObjectModel(
        meta='onigiri',
        delta='hinkali',
    )

    instance.save()
    recieved = ObjectModel.get(ids=instance.id, fields={'delta'})

    assert recieved.id == instance.id
    assert recieved.meta is None
    assert recieved.delta == 'hinkali'
    assert recieved.extra == 'uhinkalio'
    assert recieved.created is None
    assert recieved.updated is None

def test_save_none_with_fields():
    instance = ObjectModel(
        meta='onigiri',
        delta='hinkali',
    )

    instance.save()
    recieved1 = ObjectModel.get(ids=instance.id, fields={'delta'})

    recieved1.extra = 'ramen'

    recieved1.save()
    recieved2 = ObjectModel.get(ids=instance.id)

    assert recieved2.id == instance.id
    assert recieved2.meta == 'onigiri'
    assert recieved2.delta == 'hinkali'
    assert recieved2.extra == 'ramen'
    assert recieved2.created == instance.created
    assert recieved2.updated != instance.updated

def test_save_data_with_fields():
    instance = ObjectModel(
        name='test_save_fields',
        meta='onigiri',
        delta='hinkali',
    )

    instance.save()
    recieved1 = ObjectModel.get(ids=instance.id, fields={'name', 'delta'})

    recieved1.name = None
    recieved1.delta = 'hacapuri'

    recieved1.save()
    recieved2 = ObjectModel.get(ids=instance.id)

    assert recieved2.id == instance.id
    assert recieved2.name == 'test_save_fields'
    assert recieved2.meta == 'onigiri'
    assert recieved2.delta == 'hacapuri'
    assert recieved2.extra == 'uhacapurio'
    assert recieved2.created == instance.created
    assert recieved2.updated != instance.updated

def test_save_sub_partially():
    sub1 = SubObject(
        taiga=1,
    )
    instance = ObjectModel(
        multi=[sub1.json(default=False)],
    )

    instance.save()
    recieved1 = ObjectModel.get(ids=instance.id, fields={'delta'})

    assert recieved1.multi == []


    sub2 = SubObject()
    recieved1.multi += [sub2.json(default=False)]

    recieved1.save()
    recieved2 = ObjectModel.get(ids=instance.id, fields={'multi'})

    assert recieved2.id == instance.id

    with SubObject(recieved2.multi[1]) as recieved:
        assert recieved.id == sub2.id
        assert recieved.taiga is None

    with SubObject(recieved2.multi[0]) as recieved:
        assert recieved.id == sub1.id
        assert recieved.taiga == 1

def test_reload():
    instance = ObjectModel(
        delta='hinkali',
    )
    instance.save()

    recieved1 = ObjectModel.get(ids=instance.id)
    recieved2 = ObjectModel.get(ids=instance.id)

    assert recieved1._specified_fields is None
    assert recieved2._specified_fields is None

    recieved1.delta = 'hacapuri'
    recieved1.save()

    assert recieved1.delta == 'hacapuri'
    assert recieved2.delta == 'hinkali'

    recieved2.reload()

    assert recieved2._specified_fields is None
    assert recieved2.id == recieved1.id == instance.id
    assert recieved2.delta == 'hacapuri'

    recieved1.reload()

    assert recieved1._specified_fields is None
    assert recieved1.id == recieved1.id == instance.id
    assert recieved1.delta == 'hacapuri'

def test_reload_with_fields():
    # now = time.time()

    instance = ObjectModel(
        name='test_reload_fields',
        meta='onigiri',
        delta='hinkali',
        multi=[1, 2, 3],
    )
    instance.save()

    recieved = ObjectModel.get(ids=instance.id, fields={'meta'})

    assert set(recieved._loaded_values) == {'id', 'meta'}
    assert recieved._specified_fields == {'id', 'meta'}

    recieved.delta = 'hacapuri'
    recieved.multi = [4, 5, 6]
    recieved.save()

    recieved.reload(fields={'meta', 'extra', 'multi'})

    assert set(recieved._loaded_values) == {
        'id', # Default
        'meta', # Specified
        'multi', # Specified
        # 'delta', # Changed
        # 'updated', # Auto changed
    }
    assert recieved._specified_fields == {
        'id',
        'meta',
        'extra',
        'multi',
    }
    assert recieved.id == instance.id
    assert recieved.name is None
    assert recieved.meta == 'onigiri'
    assert recieved.delta == '' # default
    assert recieved.extra == 'uo' # default
    assert recieved.multi == [4, 5, 6] # new
    assert recieved.created is None
    assert recieved.updated is None

def test_init_print():
    instance = ObjectModel(
        meta='onigiri',
        multi=[1, 2, 3],
    )

    text = str(instance)
    assert text[:19] == 'Object ObjectModel('
    assert text[-1] == ')'
    assert json.loads(text[19:-1]) == {
        'id': 0,
        'name': None,
        'meta': 'onigiri',
        'delta': '',
        'extra': 'uo',
        'multi': [1, 2, 3],
        'status': None,
        'user': 0,
        'created': instance.created,
        'updated': None,
    }

def test_pull():
    sub1 = SubObject(
        taiga=1,
    )
    sub2 = SubObject(
        taiga=2,
    )
    sub3 = SubObject(
        taiga=3,
    )
    instance = ObjectModel(
        multi=[
            sub1.json(default=False),
            sub2.json(default=False),
            sub3.json(default=False),
        ],
    )

    instance.save()
    instance = ObjectModel.get(ids=instance.id)

    assert len(instance.multi) == 3

    instance.multi[2]['taiga'] = 0
    del instance.multi[0]

    instance.save()
    instance = ObjectModel.get(ids=instance.id)

    assert len(instance.multi) == 2
    assert instance.multi[0]['id'] == sub2.id
    assert instance.multi[0]['taiga'] == sub2.taiga
    assert instance.multi[1]['id'] == sub3.id

def test_update_replace():
    sub1 = SubObject(
        taiga=1,
    )
    sub2 = SubObject(
        taiga=1,
    )
    sub3 = SubObject(
        taiga=3,
    )
    sub4 = SubObject(
        taiga=4,
        tundra=1,
    )
    sub5 = SubObject(
        taiga=5,
    )
    sub6 = SubObject(
        taiga=6,
        tundra=1,
    )
    instance = ObjectModel(
        multi=[
            sub1.json(default=False),
            sub2.json(default=False),
            sub3.json(default=False),
            sub4.json(default=False),
            sub5.json(default=False),
            sub6.json(default=False),
        ],
    )

    instance.save()
    instance = ObjectModel.get(ids=instance.id)

    assert len(instance.multi) == 6

    instance.multi[1]['taiga'] = 2
    del instance.multi[3]['tundra']
    instance.multi[4]['taiga'] = 5
    instance.multi[5]['tundra'] = 0

    instance.save()
    instance = ObjectModel.get(ids=instance.id)

    assert len(instance.multi) == 6
    assert instance.multi[0]['id'] == sub1.id
    assert instance.multi[0]['taiga'] == 1
    assert instance.multi[1]['id'] == sub2.id
    assert instance.multi[1]['taiga'] == 2
    assert instance.multi[2]['id'] == sub3.id
    assert instance.multi[2]['taiga'] == 3
    assert instance.multi[3]['id'] == sub4.id
    assert instance.multi[3]['taiga'] == 4
    assert 'tundra' not in instance.multi[3]
    assert instance.multi[4]['id'] == sub5.id
    assert instance.multi[4]['taiga'] == 5
    assert instance.multi[5]['id'] == sub6.id
    assert instance.multi[5]['taiga'] == 6
    assert instance.multi[5]['tundra'] == 1
