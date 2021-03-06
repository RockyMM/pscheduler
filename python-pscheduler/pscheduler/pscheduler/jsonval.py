"""
Functions for validating JSON against the pScheduler JSON and standard
values dictionaries
"""

import copy
import jsonschema


# TODO: Consider adding tile/description and maybe "example" (not
# officially supported) as a way to generate the JSON dictionary.

# TODO: Need to go through and add "additionalProperties": False to
# all object entries.

#
# Types from the dictionary
#
__dictionary__ = {
    
    #
    # JSON Types
    #

    "AnyJSON": {
        "oneOf": [
            { "type": "array" },
            { "type": "boolean" },
            { "type": "integer" },
            { "type": "null" },
            { "type": "number" },
            { "type": "object" },
            { "type": "string" }
            ]
        },

    "Array": { "type": "array" },

    "AS": {
        "type": "object",
        "properties": {            
            "number": { "$ref": "#/pScheduler/Cardinal" },
            "owner": { "type": "string" },
            },
        "required": [ "number" ]
        },

    "Boolean": { "type": "boolean" },

    "Cardinal": {
        "type": "integer",
        "minimum": 1,
    },

    "CardinalList": {
        "type": "array",
        "items": { "$ref": "#/pScheduler/Cardinal" },
    },

    "CardinalRange": {
        "type": "object",
        "properties": {
            "lower": { "$ref": "#/pScheduler/Cardinal" },
            "upper": { "$ref": "#/pScheduler/Cardinal" }
        },
        "additionalProperties": False,
        "required": [ "lower", "upper" ]
    },

    "CardinalZero": {
        "type": "integer",
        "minimum": 0,
        },

    "CardinalZeroList": {
        "type": "array",
        "items": { "$ref": "#/pScheduler/CardinalZero" },
    },

    "CardinalZeroRange": {
        "type": "object",
        "properties": {
            "lower": { "$ref": "#/pScheduler/CardinalZero" },
            "upper": { "$ref": "#/pScheduler/CardinalZero" }
        },
        "additionalProperties": False,
        "required": [ "lower", "upper" ]
    },


    "Duration": {
        "type": "string",
        # ISO 8601.  Source: https://gist.github.com/philipashlock/8830168
        # Modified not to accept months or years, which are inexact.
        "pattern": r'^(R\d*\/)?P(?:\d+(?:\.\d+)?W)?(?:\d+(?:\.\d+)?D)?(?:T(?:\d+(?:\.\d+)?H)?(?:\d+(?:\.\d+)?M)?(?:\d+(?:\.\d+)?S)?)?$'
        },

    "DurationRange": {
        "type": "object",
        "properties": {
            "lower": { "$ref": "#/pScheduler/Duration" },
            "upper": { "$ref": "#/pScheduler/Duration" }
        },
        "additionalProperties": False,
        "required": [ "lower", "upper" ]
    },

    "Email": { "type": "string", "format": "email" },

    "Float": {
        "type": "number"
    },

    "GeographicPosition": {
        "type": "string",
        # ISO 6709
        # Source:  https://svn.apache.org/repos/asf/abdera/abdera2/common/src/main/java/org/apache/abdera2/common/geo/IsoPosition.java
        "pattern": r'^(([+-]\d{2})(\d{2})?(\d{2})?(\.\d+)?)(([+-]\d{3})(\d{2})?(\d{2})?(\.\d+)?)([+-]\d+(\.\d+)?)?$'
        },

    "Host": {
        "type": "string",
        "format": "host-name"
        },

    "Integer": { "type": "integer" },

    "IPAddress": {
        "oneOf": [
            { "type": "string", "format": "ipv4" },
            { "type": "string", "format": "ipv6" },
            ]
        },

    "IPv4": { "type": "string", "format": "ipv4" },

    "IPv6": { "type": "string", "format": "ipv6" },

    "IPv4CIDR": {
        "type": "string",
        # Source: http://blog.markhatton.co.uk/2011/03/15/regular-expressions-for-ip-addresses-cidr-ranges-and-hostnames
        "pattern":r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/([0-9]|[1-2][0-9]|3[0-2]))$'
        },

    "IPv6CIDR": {
        "type": "string",
        # Source: http://www.regexpal.com/93988
        "pattern": r'^s*((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3})|:))|(([0-9A-Fa-f]{1,4}:){5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1,5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:))|(:(((:[0-9A-Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]d|1dd|[1-9]?d)(.(25[0-5]|2[0-4]d|1dd|[1-9]?d)){3}))|:)))(%.+)?s*(\/([0-9]|[1-9][0-9]|1[0-1][0-9]|12[0-8]))?$'
    },

    "IPCIDR": {
        "oneOf": [
            { "$ref": "#/pScheduler/IPv4CIDR" },
            { "$ref": "#/pScheduler/IPv6CIDR" },
        ]
    },

    "IPPort": {
        "type": "integer",
        "minimum": 0,
        "maximum": 65535
        },
    
    "IPPortRange": {
        "type": "object",
        "properties": {
            "lower": { "$ref": "#/pScheduler/IPPort" },
            "upper": { "$ref": "#/pScheduler/IPPort" }
        },
        "additionalProperties": False,
        "required": [ "lower", "upper" ]
    },
    
    "IPTOS": {
        "type": "integer",
        "minimum": 0,
        "maximum": 63
        },
    
    "Number": { "type": "number" },

    "Numeric": {
        "oneOf": [
            { "$ref": "#/pScheduler/Number" },
            { "$ref": "#/pScheduler/SINumber" },
            ]
    },

    "NumericRange": {
        "type": "object",
        "properties": {
            "lower": { "$ref": "#/pScheduler/Numeric" },
            "upper": { "$ref": "#/pScheduler/Numeric" }
        },
        "additionalProperties": False,
        "required": [ "lower", "upper" ]
    },

    "Probability": {
        "type": "number",
        "minimum": 0.0,
        "maximum": 1.0
        },

    "ProbabilityRange": {
        "type": "object",
        "properties": {
            "lower": { "$ref": "#/pScheduler/Probability" },
            "upper": { "$ref": "#/pScheduler/Probability" }
        },
        "additionalProperties": False,
        "required": [ "lower", "upper" ]
    },


    "SINumber":  {
        "type": "string",
        "pattern": "^[0-9]+(\\.[0-9]+)?(\\s*[KkMmGgTtPpEeZzYy][Ii]?)?$"
        },

    # TODO: This should be subsumed by NumericRange,
    "SINumberRange": {
        "type": "object",
        "properties": {
            "lower": { "$ref": "#/pScheduler/SINumber" },
            "upper": { "$ref": "#/pScheduler/SINumber" }
        },
        "additionalProperties": False,
        "required": [ "lower", "upper" ]
    },

    "String": { "type": "string" },

    "StringList": {
        "type": "array",
        "items": { "$ref": "#/pScheduler/String" }
        },

    "StringMatch": {
        "type": "object",
        "properties": {
            "style": {
                "type": "string",
                "enum": [
                    "exact",
                    "contains",
                    "regex"
                    ],
            },
            "match": { "$ref": "#/pScheduler/String" },
            "case-insensitive": { "$ref": "#/pScheduler/Boolean" },
            "invert": { "$ref": "#/pScheduler/Boolean" },
        },
        "additionalProperties": False,
        "required": [ "style", "match" ]
    },

    "Timestamp": {
        "type": "string",
        # ISO 8601.  Source: https://gist.github.com/philipashlock/8830168
        "pattern": r'^([\+-]?\d{4}(?!\d{2}\b))((-?)((0[1-9]|1[0-2])(\3([12]\d|0[1-9]|3[01]))?|W([0-4]\d|5[0-2])(-?[1-7])?|(00[1-9]|0[1-9]\d|[12]\d{2}|3([0-5]\d|6[1-6])))([T\s]((([01]\d|2[0-3])((:?)[0-5]\d)?|24\:?00)([\.,]\d+(?!:))?)?(\17[0-5]\d([\.,]\d+)?)?([zZ]|([\+-])([01]\d|2[0-3]):?([0-5]\d)?)?)?)?$'
        },

    "TimestampAbsoluteRelative": {
        "oneOf" : [
            { "$ref": "#/pScheduler/Timestamp" },
            { "$ref": "#/pScheduler/Duration" },
            {
                "type": "string",
                # Same pattern as iso8601-duration, with '@' prepended
                "pattern": r'^@(R\d*/)?P(?:\d+(?:\.\d+)?Y)?(?:\d+(?:\.\d+)?M)?(?:\d+(?:\.\d+)?W)?(?:\d+(?:\.\d+)?D)?(?:T(?:\d+(?:\.\d+)?H)?(?:\d+(?:\.\d+)?M)?(?:\d+(?:\.\d+)?S)?)?$'
                }
            ]
        },

    "URL": { "type": "string", "format": "uri" },

    "UUID": {
        "type": "string",
        "pattern": r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}$'
        },

    "Version": {
        "type": "string",
        "pattern": r'^[0-9]+(\.[0-9]+(\.[0-9]+)?)$'
        },


    #
    # Compound Types
    #

    "ArchiveSpecification": {
        "type": "object",
        "properties": {
            "archiver": { "type": "string" },
            "data": { "$ref": "#/pScheduler/AnyJSON" },
            },
        "required": [
            "archiver",
            "data",
            ]
        },

    "Maintainer": {
        "type": "object",
        "properties": {
            "name":  { "type": "string" },
            "email": { "$ref": "#/pScheduler/Email" },
            "href":  { "$ref": "#/pScheduler/URL" },
            },
        "required": [
            "name",
            ]
        },

    "NameVersion": {
        "type": "object",
        "properties": {
            "name":    { "type": "string" },
            "version": { "$ref": "#/pScheduler/Version" },
            },
        "required": [
            "name",
            "version",
            ]
        },

    "ParticipantResult": {
        "type": "object",
        "properties": {
            "participant": { "$ref": "#/pScheduler/Host" },
            "result":      { "$ref": "#/pScheduler/AnyJSON" },
            },
        "required": [
            "participant",
            "result",
            ]
        },

    "RunResult": {
        "type": "object",
        "properties": {
            "id":           { "$ref": "#/pScheduler/UUID" },
            "schedule":     { "$ref": "#/pScheduler/TimeRange" },
            "test":         { "$ref": "#/pScheduler/TestSpecification" },
            "tool":         { "$ref": "#/pScheduler/NameVersion" },
            "participants": {
                "type": "array",
                "items": { "$ref": "#/pScheduler/ParticipantResult" },
                },
            "result":       { "$ref": "#/pScheduler/AnyJSON" }
            },
        "required": [
            "id",
            "schedule",
            "test",
            "tool",
            "participants",
            "result",
            ]
        },

    "ScheduleSpecification": {
        "type": "object",
        "properties": {
            "start":    { "$ref": "#/pScheduler/TimestampAbsoluteRelative" },
            "slip":     { "$ref": "#/pScheduler/Duration" },
            "randslip": { "$ref": "#/pScheduler/Probability" },
            "repeat":   { "$ref": "#/pScheduler/Duration" },
            "until":    { "$ref": "#/pScheduler/TimestampAbsoluteRelative" },
            "max-runs": { "$ref": "#/pScheduler/Cardinal" },
            },
        },

    "TaskSpecification": {
        "type": "object",
        "properties": {
            "schema":   { "$ref": "#/pScheduler/Cardinal" },
            "test":     { "$ref": "#/pScheduler/TestSpecification" },
            "tool":     {" $ref": "#/pScheduler/String" },
            "tools":    {"$ref": "#/pScheduler/StringList" },
            "schedule": { "$ref": "#/pScheduler/ScheduleSpecification" },
            "archives": {
                "type": "array",
                "items": { "$ref": "#/pScheduler/ArchiveSpecification" },
                },
            "reference": { "$ref": "#/pScheduler/AnyJSON" },
            "_key": { "$ref": "#/pScheduler/String" },
            },
        "required": [
            "schema",
            "test",
            ]
        },

    "TestSpecification": {
        "type": "object",
        "properties": {
            "test": { "type": "String" },
            "spec": { "$ref": "#/pScheduler/AnyJSON" },
            },
        "required": [
            "test",
            "spec",
            ],
        },

    "TimeRange": {
        "type": "object",
        "properties": {
            "start": { "$ref": "#/pScheduler/Timestamp" },
            "end":   { "$ref": "#/pScheduler/Timestamp" },
            },
        },




    #
    # Standard Values
    #
    # Note that these are lowercase with hyphens, matching the style
    # of the names used.
    #

    # TODO: Put this into the documentation
    "icmp-error": {
        "type": "string",
        "enum": [
            'net-unreachable',
            'host-unreachable',
            'protocol-unreachable',
            'port-unreachable',
            'fragmentation-needed-and-df-set',
            'source-route-failed',
            'destination-network-unknown',
            'destination-host-unknown',
            'source-host-isolated',
            'destination-network-administratively-prohibited',
            'destination-host-administratively-prohibited',
            'network-unreachable-for-type-of-service',
            'icmp-destination-host-unreachable-tos',
            'communication-administratively-prohibited',
            'host-precedence-violation',
            'precedence-cutoff-in-effect',
            ]
        },

    "ip-version": {
        "type": "integer",
        "enum": [ 4, 6 ]
        },


    #
    # Standard Limit Types
    #

    "Limit": {

        "Boolean": {
            "type": "object",
            "properties": {
                "description":  { "$ref": "#/pScheduler/String" },
                "match":        { "$ref": "#/pScheduler/Boolean" },
                "fail-message": { "$ref": "#/pScheduler/String" }
            },
            "additionalProperties": False,
            "required": [ "match" ]
        },

        "Cardinal": {
            "type": "object",
            "properties": {
                "description":  { "$ref": "#/pScheduler/String" },
                "range":        { "$ref": "#/pScheduler/CardinalRange" },
                "invert":       { "$ref": "#/pScheduler/Boolean" }
            },
            "additionalProperties": False,
            "required": [ "range" ]
        },

        "CardinalList": {
            "type": "object",
            "properties": {
                "description":  { "$ref": "#/pScheduler/String" },
                "match":        { "$ref": "#/pScheduler/CardinalList" },
                "invert":       { "$ref": "#/pScheduler/Boolean" }
            },
            "additionalProperties": False,
            "required": [ "match" ]

        },

        "CardinalZero": {
            "type": "object",
            "properties": {
                "description":  { "$ref": "#/pScheduler/String" },
                "range":        { "$ref": "#/pScheduler/CardinalZeroRange" },
                "invert":       { "$ref": "#/pScheduler/Boolean" }
            },
            "additionalProperties": False,
            "required": [ "range" ]
        },

        "CardinalZeroList": {
            "type": "object",
            "properties": {
                "description":  { "$ref": "#/pScheduler/String" },
                "match":        { "$ref": "#/pScheduler/CardinalZeroList" },
                "invert":       { "$ref": "#/pScheduler/Boolean" }
            },
            "additionalProperties": False,
            "required": [ "match" ]

        },

        "Duration": {
            "type": "object",
            "properties": {
                "description":  { "$ref": "#/pScheduler/String" },
                "range":        { "$ref": "#/pScheduler/DurationRange" },
                "invert":       { "$ref": "#/pScheduler/Boolean" }
            },
            "additionalProperties": False,
            "required": [ "range" ]
        },

        "SINumber": {
            "properties": {
                "description":  { "$ref": "#/pScheduler/String" },
                "range":        { "$ref": "#/pScheduler/SINumberRange" },
                "invert":       { "$ref": "#/pScheduler/Boolean" }
            },
            "additionalProperties": False,
            "required": [ "range" ]
        },

        "IPVersion": {
            "#": "TODO: Develop this."
        },

        "Probability": {
            "properties": {
                "description": { "$ref": "#/pScheduler/String" },
                "range":       { "$ref": "#/pScheduler/ProbabilityRange" },
                "invert":      { "$ref": "#/pScheduler/Boolean" }
            },
            "additionalProperties": False,
            "required": [ "range" ]
        },

        "String": {
            "type": "object",
            "properties": {
                "description":  { "$ref": "#/pScheduler/String" },
                "match":        { "$ref": "#/pScheduler/StringMatch" },
                "fail-message": { "$ref": "#/pScheduler/String" }
            },
            "additionalProperties": False,
            "required": [ "match" ]
        }

    }
}



__default_schema__ = {

    # TODO: Find out if this is downloaded or just a placeholder
    "$schema": "http://json-schema.org/draft-04/schema#",
    "id": "http://perfsonar.net/pScheduler/json_generic.json",
    "title": "pScheduler Generic Validation Schema",

    "type": "object",
    "additionalProperties": False,

    "pScheduler": __dictionary__
}




def json_validate(json, skeleton):
    """
    Validate JSON against a jsonschema schema.

    The skeleton is a dictionary containing a partial,
    draft-04-compatible jsonschema schema, containing only the
    following:

        type         (array, boolean, integer, null, number, object, string)
        items        (Only when type is array)
        properties   (Only when type is object)
        additionalProperties  (Only when type is an object)
        required     Required items
        local        (Optional; see below.)

    The optional 'local' element is a dictionary which may be used for
    any local definitions to be referenced from the items or
    properties sections.

    The standard pScheduler types are available for reference as
    "#/pScheduler/TypeName", where TypeName is a standard pScheduler
    type as defined in the "pScheduler JSON Style Guide and Type
    Dictionary" document."

    The values returned are a tuple containing a boolean indicating
    whether or not the JSON was valid and a string containing any
    error messages if not.
    """

    # Validate what came in

    if type(json) != dict:
        raise ValueError("JSON provided must be a dictionary.")

    if type(skeleton) != dict:
        raise ValueError("Skeleton provided must be a dictionary.")


    # Build up the schema from the dictionaries and user input.

    # A shallow copy is sufficient for this since we don't clobber the
    # innards.
    schema = copy.copy(__default_schema__)

    for element in [ 'type', 'items', 'properties', 'additionalProperties',
                     'required', 'local' ]:
        if element in skeleton:
            schema[element] = skeleton[element]

    # Let this throw whatever it's going to throw, since schema errors
    # are problems wih the software, not the data.

    # TODO: This doesn't seem to validate references.
    jsonschema.Draft4Validator.check_schema(schema)


    try:
        jsonschema.validate(json, schema,
                            format_checker=jsonschema.FormatChecker())
    except jsonschema.exceptions.ValidationError as ex:
        return (False, "At %s: %s" % (
            '/' + ('/'.join([str(x) for x in ex.absolute_path])),
            ex.message
            ))


    return (True, 'OK')


# Test program

if __name__ == "__main__":

    sample = {
        "schema": 1,
        "when": "2015-06-12T13:48:19.234",
        "howlong": "PT10M",
        "sendto": "bob@example.com",
        "x-factor": 3.14,
        "protocol": "udp",
        "ipv": 6,
        "ip": "fc80:dead:beef::",
        "archspec": { "name": "foo", "data": None },
        }

    schema = {
        "local": {
            "protocol": {
                "type": "string",
                "enum": ['icmp', 'udp', 'tcp']
                }
            },
        "type": "object",
        "properties": {
            "schema":   { "$ref": "#/pScheduler/Cardinal" },
            "when":     { "$ref": "#/pScheduler/Timestamp" },
            "howlong":  { "$ref": "#/pScheduler/Duration" },
            "sendto":   { "$ref": "#/pScheduler/Email" },
            "ipv":      { "$ref": "#/pScheduler/ip-version" },
            "ip":       { "$ref": "#/pScheduler/IPAddress" },
            "protocol": { "$ref": "#/local/protocol" },
            "x-factor": { "type": "number" },
            "archspec": { "$ref": "#/pScheduler/ArchiveSpecification" },

            },
        "required": [ "sendto", "x-factor" ]
        }

    valid, message = json_validate(sample, schema)

    print valid, message

