import json
from copy import Error
from typing import Dict, Optional

from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from graphql.language import (ArgumentNode, DocumentNode, FieldNode, NameNode,
                              OperationDefinitionNode, OperationType,
                              SelectionSetNode, StringValueNode, parse,
                              print_ast)


def mantle(
        mantle_endpoint: Optional[str] = 'https://tequila-mantle.anchorprotocol.com',
        http_headers: Optional[Dict] = {
            "Content-type": "application/json",
        },
        query: Optional[str] = None,
        query_variables: Optional[Dict] = None,
        wasm_query: Optional[Dict] = {}
) -> Dict:
    if (query == None and wasm_query == None):
        raise Error('Either query or wasm_query must be entered')

    selections = []

    for key in wasm_query.keys():
        selections.append(
            FieldNode(
                alias=NameNode(value=key),
                name=NameNode(value='WasmContractsContractAddressStore'),
                arguments=[
                    ArgumentNode(
                        name=NameNode(value='ContractAddress'),
                        value=StringValueNode(
                            value=wasm_query[key]['contractAddress'])
                    ),
                    ArgumentNode(
                        name=NameNode(value='QueryMsg'),
                        value=StringValueNode(
                            value=json.dumps(wasm_query[key]['query']))
                    )
                ],
                selection_set=SelectionSetNode(
                    selections=[
                        FieldNode(
                            name=NameNode(value='Result')
                        )
                    ]
                )
            )
        )

    if (query != None):
        document = parse(query)
        document.definitions[0].selection_set.selections = document.definitions[0].selection_set.selections + selections
    else:
        document = DocumentNode(definitions=[
            OperationDefinitionNode(
                operation=OperationType.QUERY,
                directives=[],
                variables_definitions=[],
                selection_set=SelectionSetNode(selections=selections),
            )
        ])

    execute_query = print_ast(document)

    transport = RequestsHTTPTransport(
        url=mantle_endpoint,
        use_json=True,
        headers=http_headers,
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )

    result = client.execute(
        gql(execute_query), variable_values=query_variables)

    for key in wasm_query.keys():
        result[key] = json.loads(result[key]['Result'])

    return result
