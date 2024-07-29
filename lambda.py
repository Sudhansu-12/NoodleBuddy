import json

# Updated values
sizes = ['small', 'medium', 'large']
broth = ['light', 'medium', 'thick']
types = ['chicken', 'vegetable', 'beef', 'crab', 'shrimp']
spices = ['no-spicy', 'spicy', 'super-spicy']

def validate_order(slots):
    # Validate Size
    if not slots['Size']:
        print('Validating Size Slot')
        return {
            'isValid': False,
            'invalidSlot': 'Size'
        }
    if slots['Size']['value']['originalValue'].lower() not in sizes:
        print('Invalid Size')
        return {
            'isValid': False,
            'invalidSlot': 'Size',
            'message': 'Please select a {} size.'.format(", ".join(sizes))
        }

    # Validate Broth
    if not slots['Broth']:
        print('Validating Broth Slot')
        return {
            'isValid': False,
            'invalidSlot': 'Broth'
        }
    if slots['Broth']['value']['originalValue'].lower() not in broth:
        print('Invalid Broth')
        return {
            'isValid': False,
            'invalidSlot': 'Broth',
            'message': 'Please select from {} broth types.'.format(", ".join(broth))
        }

    # Validate Type
    if not slots['Type']:
        print('Validating Type Slot')
        return {
            'isValid': False,
            'invalidSlot': 'Type'
        }
    if slots['Type']['value']['originalValue'].lower() not in types:
        print('Invalid Type')
        return {
            'isValid': False,
            'invalidSlot': 'Type',
            'message': 'Please select a noodle type from {}.'.format(", ".join(types))
        }

    # Validate Spice
    if not slots['spice']:
        print('Validating Spice Slot')
        return {
            'isValid': False,
            'invalidSlot': 'spice'
        }
    if slots['spice']['value']['originalValue'].lower() not in spices:
        print('Invalid spice')
        return {
            'isValid': False,
            'invalidSlot': 'spice',
            'message': 'Please select a spice level from {}.'.format(", ".join(spices))
        }

    # Valid Order
    return {'isValid': True}


def lambda_handler(event, context):
    print(event)

    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    order_validation_result = validate_order(slots)

    if event['invocationSource'] == 'DialogCodeHook':
        if not order_validation_result['isValid']:
            if 'message' in order_validation_result:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": order_validation_result['message']
                        }
                    ]
                }
            else:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    }
                }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }

    if event['invocationSource'] == 'FulfillmentCodeHook':
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": slots,
                    "state": "Fulfilled"
                }

            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "I've placed your order."
                }
            ]
        }

    print(response)
    return response
