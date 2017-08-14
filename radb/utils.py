import enum
import sys
import importlib
import json

def lreplace(s, prefix, sub):
    return s.replace(prefix, sub, 1)

def rreplace(s, suffix, sub):
    return sub.join(s.rsplit(suffix, 1))

def AutoNameEnum(enum_type_name, enum_fields):
    return enum.Enum(enum_type_name, [(field, field.lower()) for field in enum_fields])

class Tee:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.file = open(filename, 'w')

    def write(self, s):
        self.terminal.write(s)
        self.file.write(s)

    def flush(self):
        self.terminal.flush()
        self.file.flush()

def number_lines(s):
    lines = s.split('\n')
    lineno_max_width = len(str(len(lines)))
    for i, line in enumerate(lines):
        yield ('line {:>' + str(lineno_max_width) + '}: {}').format(i+1, line)

def dynamic_import(full_class_name):
    parts = full_class_name.split('.')
    mod = __import__('.'.join(parts[0:-1]), fromlist=[parts[-1]])
    return getattr(mod, parts[-1])

class CustomJSONSerializable:
    def to_json(self):
        return json.dumps(self, cls=CustomJSONEncoder, indent=2, sort_keys=True)
    def list_to_json(collection):
        return json.dumps(collection, cls=CustomJSONEncoder, indent=2, sort_keys=True)
    def from_json(object_json):
        if isinstance(object_json, str):
            return json.loads(object_json, cls=CustomJSCONDecoder)
        else:
            return json.load(object_json, cls=CustomJSCONDecoder)
    def list_from_json(list_json):
        if isinstance(list_json, str):
            return json.loads(list_json, cls=CustomJSCONDecoder)
        else:
            return json.load(list_json, cls=CustomJSCONDecoder)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, dict):
            return {k : self.default(v) for k, v in obj.items()}
        elif isinstance(obj, list) and not isinstance(obj, str):
            return [self.default(v) for v in obj]
        elif isinstance(obj, CustomJSONSerializable):
            outdict = {a : self.default(v) for a, v in obj.__dict__.items()}
            outdict['__type__'] = obj.__class__.__module__ + '.' + obj.__class__.__qualname__
            return outdict
        return obj

class CustomJSCONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
    def object_hook(self, o):
        try:
            if '__type__' in o:
                cls = dynamic_import(o['__type__'])
                obj = cls(**{key : o[key] for key in o if key != '__type__'})
                return obj
        except:
            pass
        return o
