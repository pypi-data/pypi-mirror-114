from pycspr.serialisation.byte_array import encode as byte_array_encoder
from pycspr.types import CLValue
from pycspr.types import CLType
from pycspr.types import CLType_ByteArray
from pycspr.types import CLType_List
from pycspr.types import CLType_Map
from pycspr.types import CLType_Option
from pycspr.types import CLType_Simple
from pycspr.types import CLType_Tuple1
from pycspr.types import CLType_Tuple2
from pycspr.types import CLType_Tuple3
from pycspr.types import CLTypeKey
from pycspr.types import TYPES_NUMERIC



# Map: simple internal enum to external type key.
_TYPE_KEYS = {
    CLTypeKey.BOOL: "Bool",
    CLTypeKey.UNIT: "Unit",
    CLTypeKey.STRING: "String",
    CLTypeKey.KEY: "Key",
    CLTypeKey.UREF: "URef",
    CLTypeKey.PUBLIC_KEY: "PublicKey",
}


def encode_cl_type(entity: CLType) -> dict:
    """Encodes a CL type.
    
    """
    _ENCODERS = {
        # Byte array.
        CLType_ByteArray: lambda: {
            "ByteArray": entity.size
        },

        # List.
        CLType_List: lambda: {
            "List": encode_cl_type(entity.inner_type)
        },

        # Map.
        CLType_Map: lambda: {
            "Map": encode_cl_type(entity.inner_type)
        },

        # Optional.
        CLType_Option: lambda: {
            "Option": encode_cl_type(entity.inner_type)
        },

        # Simple type.
        CLType_Simple: lambda: encode_cl_type_key(entity.typeof),

        # 1-ary tuple.
        CLType_Tuple1: lambda: {
            "Tuple1": encode_cl_type(entity.t0_type)
        },

        # 2-ary tuple.
        CLType_Tuple2: lambda: {
            "Tuple2": [encode_cl_type(entity.t0_type), encode_cl_type(entity.t1_type)]
        },

        # 3-ary tuple.
        CLType_Tuple3: lambda: {
            "Tuple3": [encode_cl_type(entity.t0_type), encode_cl_type(entity.t1_type), encode_cl_type(entity.t2_type)]
        },
    }

    return _ENCODERS[type(entity)]()


def encode_cl_type_key(entity: CLTypeKey) -> str:
    """Encodes a CL type key.
    
    """    
    try:
        return _TYPE_KEYS[entity]
    except KeyError:
        return entity.name


def encode_cl_value(entity: CLValue) -> dict:
    """Encodes a CL value.

    """
    return {
        "bytes": byte_array_encoder(entity).hex(),
        "cl_type": encode_cl_type(entity.cl_type),
        "parsed": encode_cl_value_parsed(entity.cl_type, entity.parsed),
    }


def encode_cl_value_parsed(type_info: CLType, parsed: object) -> str:
    """Encodes a parsed CL value.

    """
    if type_info.typeof in TYPES_NUMERIC:
        return str(int(parsed))
    elif type_info.typeof == CLTypeKey.BYTE_ARRAY:
        return parsed.hex()
    elif type_info.typeof == CLTypeKey.PUBLIC_KEY:
        return parsed.account_key.hex()
    elif type_info.typeof == CLTypeKey.OPTION:
        return encode_cl_value_parsed(type_info.inner_type, parsed)
    else:
        return str(parsed)
    