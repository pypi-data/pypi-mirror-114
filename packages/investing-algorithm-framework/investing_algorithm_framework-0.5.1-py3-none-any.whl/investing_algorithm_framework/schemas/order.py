from marshmallow import Schema, fields


class OrderSerializer(Schema):
    id = fields.Int(dump_only=True)
    target_symbol = fields.String(dump_only=True)
    trading_symbol = fields.String(dump_only=True)
    price = fields.Float(dump_only=True)
    amount = fields.Float(dump_only=True)
    executed = fields.Bool(dump_only=True)
    terminated = fields.Bool(dump_only=True)

    # Optional fields
    broker = fields.Method("get_broker")
    position_id = fields.Int(dump_only=True)

    @staticmethod
    def get_broker(obj):
        return obj.position.portfolio.broker
