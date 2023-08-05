
import json
from .miioservice import MiIOService


def twins_split(string, sep, default=None):
    pos = string.find(sep)
    return (string, default) if pos == -1 else (string[0:pos], string[pos+1:])


def string_to_value(string):
    if string == 'null' or string == 'none':
        return None
    elif string == 'false':
        return False
    elif string == 'true':
        return True
    else:
        return int(string)


def string_or_value(string):
    return string_to_value(string[1:]) if string[0] == '#' else string


def miio_command_help(did=None, prefix='?'):
    quote = '' if prefix == '?' else "'"
    return f'\
Get Props: {prefix}<siid[-piid]>[,...]\n\
           {prefix}1,1-2,1-3,1-4,2-1,2-2,3\n\
Set Props: {prefix}<siid[-piid]=[#]value>[,...]\n\
           {prefix}2=#60,2-2=#false,3=test\n\
Do Action: {prefix}<siid[-piid]> <arg1|#NA> [...] \n\
           {prefix}2 #NA\n\
           {prefix}5 Hello\n\
           {prefix}5-4 Hello #1\n\n\
Call MIoT: {prefix}<cmd=prop/get|/prop/set|action> <params>\n\
           {prefix}action {quote}{{"did":"{did or "267090026"}","siid":5,"aiid":1,"in":["Hello"]}}{quote}\n\n\
Call MiIO: {prefix}/<uri> <data>\n\
           {prefix}/home/device_list {quote}{{"getVirtualModel":false,"getHuamiDevices":1}}{quote}\n\n\
Devs List: {prefix}list [name=full|name_keyword] [getVirtualModel=false|true] [getHuamiDevices=0|1]\n\
           {prefix}list Light true 0\n\n\
MiIO Spec: {prefix}spec [model_keyword|type_urn] [format=text|python|json]\n\
           {prefix}spec\n\
           {prefix}spec speaker\n\
           {prefix}spec xiaomi.wifispeaker.lx04\n\
           {prefix}spec urn:miot-spec-v2:device:speaker:0000A015:xiaomi-lx04:1\n\
'


async def miio_command(service: MiIOService, did, text, prefix='?'):

    cmd, arg = twins_split(text, ' ')

    if cmd.startswith('/'):
        return await service.miio_request(cmd, arg)

    if cmd.startswith('prop') or cmd == 'action':
        return await service.miot_request(cmd, json.loads(arg) if arg else None)

    argv = arg.split(' ') if arg else []
    argc = len(argv)
    if cmd == 'list':
        return await service.device_list(argc > 0 and argv[0], argc > 1 and string_to_value(argv[1]), argc > 2 and argv[2])

    if cmd == 'spec':
        return await service.miot_spec(argc > 0 and argv[0], argc > 1 and argv[1])

    if not did or not cmd or cmd == '?' or cmd == '？' or cmd == 'help' or cmd == '-h' or cmd == '--help':
        return miio_command_help(did, prefix)

    props = []
    isget = False
    for item in cmd.split(','):
        iid, value = twins_split(item, '=')
        siid, apiid = twins_split(iid, '-', '1')
        if not siid.isdigit() or not apiid.isdigit():
            return 'ERROR: siid/piid/aiid must be integer'
        prop = [int(siid), int(apiid)]
        if not isget:
            if value is None:
                isget = True
            else:
                prop.append(string_or_value(value))
        props.append(prop)

    if argc > 0:
        args = [string_or_value(a) for a in argv] if arg != '#NA' else []
        return await service.miot_action(did, props[0][0], props[0][1], args)

    return await (service.miot_get_props if isget else service.miot_set_props)(did, props)
