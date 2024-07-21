

def get_datev_example_data():
    return [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "file_number_short": "000001-05",
                    "file_number": "000001-2005/001:00",
                    "file_name": "Insolvenzverfahren Mustermann",
                    "project_number": "123/331-12",
                    "short_reason": "Beratung",
                    "long_reason": "vacnatocbosa",
                    "department": {
                    "id": "ebd93cfc-1c2e-4927-aee5-24b448b050fd",
                    "link": "https://localhost:58452/datev/api/law/v1/departments/ebd93cfc-1c2e-4927-aee5-24b448b050fd"
                    },
                    "causes": [
                    {
                        "id": "051534f8-7b78-441a-aa9e-6f708b49d855",
                        "number": 3,
                        "name": "Forderung aus Warenlieferung",
                        "department_id": "ebd93cfc-1c2e-4927-aee5-24b448b050fd",
                        "department_link": "https://localhost:58452/datev/api/law/v1/departments/ebd93cfc-1c2e-4927-aee5-24b448b050fd"
                    },
                    {
                        "id": "051534f8-7b78-441a-aa9e-6f708b49d855",
                        "number": 15,
                        "name": "sonstige zivilrechtliche Ansprüche",
                        "department_id": "e5a91019-af4d-4373-a18c-36e64e4ec478",
                        "department_link": "https://localhost:58452/datev/api/law/v1/departments/e5a91019-af4d-4373-a18c-36e64e4ec478"
                    }
                    ],
                    "partner": {
                    "id": "c015c071-43c4-432f-be80-508d54c720e7",
                    "number": 62,
                    "display_name": "Ernst Exempeladvokat",
                    "link": "https://localhost:58452/datev/api/law/v1/employees/c015c071-43c4-432f-be80-508d54c720e7"
                    },
                    "case_handlers": [
                    {
                        "id": "c015c071-43c4-432f-be80-508d54c720e7",
                        "number": 62,
                        "display_name": "Ernst Exempeladvokat",
                        "primary_case_handler": true,
                        "commission": 100,
                        "employee_id": "f8586db2-4f22-44af-8cec-16f426bd5440",
                        "employee_link": "http://localhost:58454/datev/api/master-data/v1/employees/f8586db2-4f22-44af-8cec-16f426bd5440"
                    }
                    ],
                    "security_zone": {
                    "id": "174ddc49-e8c4-466b-8c35-d8eef5d655b6",
                    "short_name": "SB-0",
                    "name": "Öffentliche Akten"
                    },
                    "establishment": {
                    "number": 1,
                    "name": "Musterniederlassung",
                    "link": "http://localhost:58454/datev/api/master-data/v1/corporate-structures/3fa85f64-5717-4562-b3fc-2c963f66afa6/establishments/59bb1870-5e0a-4ce9-bb7d-42e95f5cdb4e",
                    "organization": {
                        "id": "2da7f880-6c24-44cd-be38-32746a268b0f",
                        "number": 1,
                        "name": "Musterkanzlei",
                        "link": "http://localhost:58454/datev/api/master-data/v1/corporate-structures/3fa85f64-5717-4562-b3fc-2c963f66afa6"
                    }
                    },
                    "economic_data": {
                    "cause_value": {
                        "amount": 20000,
                        "currency": "EUR"
                    },
                    "budget": {
                        "amount": 10000,
                        "currency": "EUR"
                    },
                    "budget_timespan": "total",
                    "base_currency": "EUR"
                    },
                    "accounting_area": {
                    "id": "7447f931-b42e-4e71-84f3-1319a49fb076",
                    "number": 1,
                    "name": "Standardbuchungskreis",
                    "link": "https://localhost:58452/datev/api/law/v1/accounting-areas/7447f931-b42e-4e71-84f3-1319a49fb076"
                    },
                    "reactivated": false,
                    "filing": {
                    "date": "2019-08-12",
                    "number": "000001-2005",
                    "retention_period_end": "2029-08-12",
                    "location": "Keller"
                    },
                    "note": "umamonabp",
                    "created": {
                    "date": "2018-09-27",
                    "creator": "Ernst Exempeladvokat"
                    },
                    "modified": {
                    "date": "2019-08-11",
                    "creator": "Ernst Exempeladvokat"
                    }
                },
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "file_number_short": "000001-05",
                    "file_number": "000001-2005/001:00",
                    "file_name": "Insolvenzverfahren Mustermann",
                    "project_number": "123/331-12",
                    "short_reason": "Beratung",
                    "long_reason": "morigejofo",
                    "department": {
                    "id": "ebd93cfc-1c2e-4927-aee5-24b448b050fd",
                    "link": "https://localhost:58452/datev/api/law/v1/departments/ebd93cfc-1c2e-4927-aee5-24b448b050fd"
                    },
                    "causes": [
                    {
                        "id": "051534f8-7b78-441a-aa9e-6f708b49d855",
                        "number": 3,
                        "name": "Forderung aus Warenlieferung",
                        "department_id": "ebd93cfc-1c2e-4927-aee5-24b448b050fd",
                        "department_link": "https://localhost:58452/datev/api/law/v1/departments/ebd93cfc-1c2e-4927-aee5-24b448b050fd"
                    },
                    {
                        "id": "051534f8-7b78-441a-aa9e-6f708b49d855",
                        "number": 15,
                        "name": "sonstige zivilrechtliche Ansprüche",
                        "department_id": "e5a91019-af4d-4373-a18c-36e64e4ec478",
                        "department_link": "https://localhost:58452/datev/api/law/v1/departments/e5a91019-af4d-4373-a18c-36e64e4ec478"
                    }
                    ],
                    "partner": {
                    "id": "c015c071-43c4-432f-be80-508d54c720e7",
                    "number": 62,
                    "display_name": "Ernst Exempeladvokat",
                    "link": "https://localhost:58452/datev/api/law/v1/employees/c015c071-43c4-432f-be80-508d54c720e7"
                    },
                    "case_handlers": [
                    {
                        "id": "c015c071-43c4-432f-be80-508d54c720e7",
                        "number": 62,
                        "display_name": "Ernst Exempeladvokat",
                        "primary_case_handler": true,
                        "commission": 100,
                        "employee_id": "f8586db2-4f22-44af-8cec-16f426bd5440",
                        "employee_link": "http://localhost:58454/datev/api/master-data/v1/employees/f8586db2-4f22-44af-8cec-16f426bd5440"
                    }
                    ],
                    "security_zone": {
                    "id": "174ddc49-e8c4-466b-8c35-d8eef5d655b6",
                    "short_name": "SB-0",
                    "name": "Öffentliche Akten"
                    },
                    "establishment": {
                    "number": 1,
                    "name": "Musterniederlassung",
                    "link": "http://localhost:58454/datev/api/master-data/v1/corporate-structures/3fa85f64-5717-4562-b3fc-2c963f66afa6/establishments/59bb1870-5e0a-4ce9-bb7d-42e95f5cdb4e",
                    "organization": {
                        "id": "2da7f880-6c24-44cd-be38-32746a268b0f",
                        "number": 1,
                        "name": "Musterkanzlei",
                        "link": "http://localhost:58454/datev/api/master-data/v1/corporate-structures/3fa85f64-5717-4562-b3fc-2c963f66afa6"
                    }
                    },
                    "economic_data": {
                    "cause_value": {
                        "amount": 20000,
                        "currency": "EUR"
                    },
                    "budget": {
                        "amount": 10000,
                        "currency": "EUR"
                    },
                    "budget_timespan": "total",
                    "base_currency": "EUR"
                    },
                    "accounting_area": {
                    "id": "7447f931-b42e-4e71-84f3-1319a49fb076",
                    "number": 1,
                    "name": "Standardbuchungskreis",
                    "link": "https://localhost:58452/datev/api/law/v1/accounting-areas/7447f931-b42e-4e71-84f3-1319a49fb076"
                    },
                    "reactivated": false,
                    "filing": {
                    "date": "2019-08-12",
                    "number": "000001-2005",
                    "retention_period_end": "2029-08-12",
                    "location": "Keller"
                    },
                    "note": "supvujsekdiras",
                    "created": {
                    "date": "2018-09-27",
                    "creator": "Ernst Exempeladvokat"
                    },
                    "modified": {
                    "date": "2019-08-11",
                    "creator": "Ernst Exempeladvokat"
                    }
                },
                {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "file_number_short": "000001-05",
                "file_number": "000001-2005/001:00",
                "file_name": "Insolvenzverfahren Mustermann",
                "project_number": "123/331-12",
                "short_reason": "Beratung",
                "long_reason": "tanejomeve",
                "department": {
                "id": "ebd93cfc-1c2e-4927-aee5-24b448b050fd",
                "link": "https://localhost:58452/datev/api/law/v1/departments/ebd93cfc-1c2e-4927-aee5-24b448b050fd"
                },
                "causes": [
                {
                    "id": "051534f8-7b78-441a-aa9e-6f708b49d855",
                    "number": 3,
                    "name": "Forderung aus Warenlieferung",
                    "department_id": "ebd93cfc-1c2e-4927-aee5-24b448b050fd",
                    "department_link": "https://localhost:58452/datev/api/law/v1/departments/ebd93cfc-1c2e-4927-aee5-24b448b050fd"
                },
                {
                    "id": "051534f8-7b78-441a-aa9e-6f708b49d855",
                    "number": 15,
                    "name": "sonstige zivilrechtliche Ansprüche",
                    "department_id": "e5a91019-af4d-4373-a18c-36e64e4ec478",
                    "department_link": "https://localhost:58452/datev/api/law/v1/departments/e5a91019-af4d-4373-a18c-36e64e4ec478"
                }
                ],
                "partner": {
                "id": "c015c071-43c4-432f-be80-508d54c720e7",
                "number": 62,
                "display_name": "Ernst Exempeladvokat",
                "link": "https://localhost:58452/datev/api/law/v1/employees/c015c071-43c4-432f-be80-508d54c720e7"
                },
                "case_handlers": [
                {
                    "id": "c015c071-43c4-432f-be80-508d54c720e7",
                    "number": 62,
                    "display_name": "Ernst Exempeladvokat",
                    "primary_case_handler": true,
                    "commission": 100,
                    "employee_id": "f8586db2-4f22-44af-8cec-16f426bd5440",
                    "employee_link": "http://localhost:58454/datev/api/master-data/v1/employees/f8586db2-4f22-44af-8cec-16f426bd5440"
                }
                ],
                "security_zone": {
                "id": "174ddc49-e8c4-466b-8c35-d8eef5d655b6",
                "short_name": "SB-0",
                "name": "Öffentliche Akten"
                },
                "establishment": {
                "number": 1,
                "name": "Musterniederlassung",
                "link": "http://localhost:58454/datev/api/master-data/v1/corporate-structures/3fa85f64-5717-4562-b3fc-2c963f66afa6/establishments/59bb1870-5e0a-4ce9-bb7d-42e95f5cdb4e",
                "organization": {
                    "id": "2da7f880-6c24-44cd-be38-32746a268b0f",
                    "number": 1,
                    "name": "Musterkanzlei",
                    "link": "http://localhost:58454/datev/api/master-data/v1/corporate-structures/3fa85f64-5717-4562-b3fc-2c963f66afa6"
                }
                },
                "economic_data": {
                "cause_value": {
                    "amount": 20000,
                    "currency": "EUR"
                },
                "budget": {
                    "amount": 10000,
                    "currency": "EUR"
                },
                "budget_timespan": "total",
                "base_currency": "EUR"
                },
                "accounting_area": {
                "id": "7447f931-b42e-4e71-84f3-1319a49fb076",
                "number": 1,
                "name": "Standardbuchungskreis",
                "link": "https://localhost:58452/datev/api/law/v1/accounting-areas/7447f931-b42e-4e71-84f3-1319a49fb076"
                },
                "reactivated": false,
                "filing": {
                "date": "2019-08-12",
                "number": "000001-2005",
                "retention_period_end": "2029-08-12",
                "location": "Keller"
                },
                "note": "tuhoweswurisa",
                "created": {
                "date": "2018-09-27",
                "creator": "Ernst Exempeladvokat"
                },
                "modified": {
                "date": "2019-08-11",
                "creator": "Ernst Exempeladvokat"
                }
            }
    ]