from jsonschema import validate

#次の４つのルールを持つスキーマ（期待するデータ構造）を定義する
schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "price": {
            "type": "string",
            "pattern": "^[0-9,]+$"
        }
    },
    "required": ["name", "price"]
}

validate({
    "name": "ぶどう",
    "price": "3,000"
}, schema)#スキーマに適合するので例外は発生しない

validate({
    "name": "みかん",
    "price": "無料"
}, schema)#スキーマに適合しないので例外発生