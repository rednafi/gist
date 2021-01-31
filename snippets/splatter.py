import json
from pprint import pprint
import argparse


json_str = """


{
    "uuid": "3934de86-e308-4407-b411-e57b23b9f1e5",
    "alternate_id": "123123",
    "account": "AnyTestNow",
    "provider": {
        "user": {
            "first_name": "Lisa",
            "last_name": "Leslie",
            "email": "leslie@clinic.com"
        },
        "uuid": "432b3eda-909c-4500-b5bd-9de2819ab1c1",
        "npi": "5555555555"
    },
    "patient": {
        "uuid": "b2ccecc7-58b9-4836-b64d-5372bcf82788",
        "id": "5",
        "alternate_id": "",
        "user": {
            "first_name": "Dell",
            "last_name": "Curry",
            "email": "dcurry@mailinator.com"
        },
        "middle_initial": "D",
        "gender": "M",
        "birth_date": "1980-01-05",
        "suffix": "",
        "address1": "23 jump st",
        "address2": "suite 3",
        "city": "12city",
        "state": "",
        "country": "Armenia",
        "zip_code": "123423",
        "social_security": "555-55-5555",
        "phone_number": "(744) 555-4342",
        "drivers_license": "",
        "ethnicity": "U",
        "race": "U",
        "reference_integration": null,
        "bill_to": "Insurance",
        "accounts": [
            "f16693a2-c70a-4056-bbc1-e48dda71474a",
            "3c49f9db-b900-43a8-a5e1-47dbec8f7fd0",
            "e1e9a0d1-52ba-4904-bbdc-eaaebf05733b"
        ],
        "providers": [
            "a962ed42-c824-499d-bedf-f0da7efed3fe",
            "432b3eda-909c-4500-b5bd-9de2819ab1c1",
            "a47ba996-2095-497c-8870-787a70faa6e6"
        ]
    },
    "code": "2021-0000071",
    "status": "Unreceived",
    "accession_number": null,
    "is_acknowledged_by_external_user": false,
    "in_house_lab_locations": [],
    "bill_to": "Insurance",
    "test_panels": [
        {
            "uuid": "51f5f9c6-fb43-4ae1-804a-c8c2fc541de6",
            "test_panel_type": {
                "uuid": "60a30ac0-a6b3-4774-9686-39e0f37cbdba",
                "alternate_id": "",
                "name": "Anticonvulsants"
            },
            "samples": [
                {
                    "uuid": "ad543d1c-bf7e-4ada-a628-19d737d84edb",
                    "code": "2021-0000071-U-1",
                    "alternate_id": "",
                    "collection_date": null,
                    "barcode": "20210000071U1",
                    "clia_sample_type": {
                        "uuid": "18fc0c28-5e89-4855-9ea2-568590737aa4",
                        "name": "Urine"
                    },
                    "collection_temperature": "",
                    "comments": ["00"]
                }
            ]
        }
    ],
    "origin_entity": "Dendi API",
    "submitted_date": "2021-01-20T14:17:41.122094",
    "reference_lab_received_date": null,
    "origin": "Reference Lab",
    "icd10_codes": [
        {
            "uuid": "b473220f-2abc-45f5-8355-9374c263627f",
            "full_code": "A00.0"
        }
    ],
    "reference_id": "2020-0021920",
    "reference_integration": null,
    "notes_by_provider": "Testing an API call.",
    "bulk_order_uuid": null
}

"""


class Splatter:
    def __init__(
        self,
        dct,
        prefix="",
        delimiter=".",
        show_value=False,
        show_markdown=False,
        export_path=None,
    ):
        self.dct = dct
        self.prefix = prefix
        self.delimiter = delimiter
        self.show_value = show_value
        self.show_markdown = show_markdown
        self.export_path = export_path
        self._rows = []

    @staticmethod
    def _get_type(o):
        return type(o).__name__

    def _path_finder(self, path, dct):
        if isinstance(dct, dict):
            for k, v in dct.items():
                if isinstance(v, list):
                    for i, item in enumerate(v):
                        self._path_finder(
                            path + self.delimiter + k + self.delimiter + str(i),
                            item,
                        )
                elif isinstance(v, dict):
                    self._path_finder(path + self.delimiter + k, v)

                else:
                    if self.show_markdown:
                        if self.show_value:
                            row = f"* `{path}{self.delimiter}{k}` : `{self._get_type(v)}` => `{v}`"
                        else:
                            row = f"* `{path}{self.delimiter}{k}` : `{self._get_type(v)}`"
                    else:
                        if self.show_value:
                            row = f"{path}{self.delimiter}{k} : {self._get_type(v)} => {v}"
                        else:
                            row = f"{path}{self.delimiter}{k} : {self._get_type(v)} => {v}"
                    self._rows.append(row)

            return self._rows

    def splat(self):
        rows = self._path_finder(self.prefix, self.dct)
        export_path = self.export_path
        if not export_path:
            for row in rows:
                print(row)
                if self.show_markdown:
                    print(f"    * ")
                    print()
        else:
            with open(export_path, 'w+') as f:
                for row in rows:
                    print(row)
                    if self.show_markdown:
                        print(f"    * ")
                        print()
                    f.writelines(f"{row}\n")


class CLI:
    def __init__(self, splatter_cls):
        self.splatter_cls = splatter_cls

    @staticmethod
    def _load_json(json_str, json_path=None):
        if json_str:
            return json.loads(json_str)

        with open(json_path) as f:
            return json.load(f)

    @staticmethod
    def _parse_args():
        parser = argparse.ArgumentParser(description="Splatter a json string.")
        parser.add_argument(
            "--json",
            help="provide the target json string",
        )
        parser.add_argument(
            "--json_path",
            help="provide the target json file path",
        )
        parser.add_argument("--prefix", default="", help="append a prefix before path")
        parser.add_argument(
            "--delimiter",
            default=".",
            help="provide preferred delimiter",
        )
        parser.add_argument(
            "--show_markdown",
            action="store_true",
            help="print in markdown format",
        )
        parser.add_argument(
            "--hide_value",
            action="store_false",
            help="show or hide attr values",
        )
        parser.add_argument(
            "--export_path",
            help="export result to `.md` file",
        )

        args = parser.parse_args()

        return args

    def entrypoint(self):
        args = self._parse_args()
        dct = self._load_json(args.json, args.json_path)
        sp = self.splatter_cls(
            dct,
            prefix=args.prefix,
            delimiter=args.delimiter,
            show_markdown=args.show_markdown,
            show_value=args.hide_value,
            export_path = args.export_path
        )

        sp.splat()

if __name__ == "__main__":

    cli = CLI(Splatter)
    cli.entrypoint()
