def process_proto(event, context):
    import base64
    from google.protobuf import json_format
    from protobuf_dependency.measurement_pb2 import Measurement

    measurement = Measurement()
    measurement.ParseFromString(base64.b64decode(event['data']))

    print(json_format.MessageToJson(measurement))
