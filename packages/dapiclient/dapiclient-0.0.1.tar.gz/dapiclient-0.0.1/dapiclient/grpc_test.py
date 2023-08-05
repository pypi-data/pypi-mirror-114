import grpc

import dapiclient.rpc.grpc.core_pb2 as core_pb2
import dapiclient.rpc.grpc.core_pb2_grpc as core_pb2_grpc
import dapiclient.rpc.grpc.platform_pb2 as platform_pb2
import dapiclient.rpc.grpc.platform_pb2_grpc as platform_pb2_grpc
import dapiclient.rpc.grpc.transactions_filter_stream_pb2 as transactions_filter_stream_pb2
import dapiclient.rpc.grpc.transactions_filter_stream_pb2_grpc as transactions_filter_stream_pb2_grpc

import cbor2
import base58

GRPC_REQUEST_TIMEOUT = 5

# Set up connection
channel = grpc.insecure_channel('seed-1.testnet.networks.dash.org:3010')
stub = platform_pb2_grpc.PlatformStub(channel)
stubCore = core_pb2_grpc.CoreStub(channel)
stubTransactions = transactions_filter_stream_pb2_grpc.TransactionsFilterStreamStub(channel)


def get_identity(id):
    # Get Identity
    # identity_id = 'Bb2p582MFR1tQhVQHKrScsAJH6Erqsb6SoroD9dQhJ5e'
    # Create Identity request
    get_identity_request = platform_pb2.GetIdentityRequest()
    # Set identity parameter of request
    get_identity_request.id = id

    # get_identity_response = platform_pb2.GetIdentityResponse()
    get_identity_response = stub.getIdentity(get_identity_request, GRPC_REQUEST_TIMEOUT)
    # print(get_identity_response)
    print('Identity Response: {}\n'.format(cbor2.loads(get_identity_response.identity)))

    # print(dir(identity_response))


def get_data_contract(contract_id):
    # Get Data Contract
    # dpns_contract_id = '2KfMcMxktKimJxAZUeZwYkFUsEcAZhDKEpQs8GMnpUse'
    contract_request = platform_pb2.GetDataContractRequest()
    contract_request.id = contract_id

    data_contract = stub.getDataContract(contract_request, GRPC_REQUEST_TIMEOUT)
    print(data_contract)
    print('Data Contract: {}\n'.format(cbor2.loads(data_contract.data_contract)))


def get_documents(contract_id, type, options):
    # Get Document
    # contract_id = dpns_contract_id

    document_request = platform_pb2.GetDocumentsRequest()
    document_request.data_contract_id = contract_id
    document_request.document_type = type
    document_request.limit = 2
    # document_request.where = # Requires cbor (found in dapi-client)

    docs = stub.getDocuments(document_request, GRPC_REQUEST_TIMEOUT)
    # print(docs)
    for d in docs.documents:
        print('Document cbor: {}\n'.format(cbor2.loads(d)))


def get_block(hash=0, height=0):
    # Get Block
    block_request = core_pb2.GetBlockRequest()
    block_request.hash = hash
    block_request.height = height

    block_response = stubCore.getBlock(block_request, GRPC_REQUEST_TIMEOUT)
    print('Block: {}\n'.format(block_response.block))


def get_status():
    status_request = core_pb2.GetStatusRequest()

    status_response = stubCore.getStatus(status_request, GRPC_REQUEST_TIMEOUT)
    print('Status: {}\n'.format(status_response))


def get_transaction(id):
    transaction_request = core_pb2.GetTransactionRequest()
    transaction_request.id = id

    transaction_response = stubCore.getTransaction(transaction_request, GRPC_REQUEST_TIMEOUT)
    print('Transaction: {}\n'.format(transaction_response.transaction))


def send_transaction(transaction, allow_high_fees=0, bypass_limits=0):
    transaction_request = core_pb2.SendTransactionRequest()
    transaction_request.transaction = transaction
    transaction_request.allow_high_fees = allow_high_fees
    transaction_request.bypass_limits = bypass_limits

    transaction_response = stubCore.sendTransaction(transaction_request, GRPC_REQUEST_TIMEOUT)
    print('Transaction: {}\n'.format(transaction_response))


def getIdentityByFirstPublicKey(public_key_hash):
    request = platform_pb2.GetIdentityByFirstPublicKeyRequest()
    request.public_key_hash = public_key_hash

    response = stub.getIdentityByFirstPublicKey(request, GRPC_REQUEST_TIMEOUT)
    print('getIdentityByFirstPublicKey: {}\n'.format(response))


def getIdentityIdByFirstPublicKey(public_key_hash):
    request = platform_pb2.GetIdentityIdByFirstPublicKeyRequest()
    request.public_key_hash = public_key_hash

    response = stub.getIdentityIdByFirstPublicKey(request, GRPC_REQUEST_TIMEOUT)
    print('getIdentityIdByFirstPublicKey: {}\n'.format(response))


def subscribeToTransactionsWithProofs(bloom_filter, from_block_hash=b'', from_block_height=0, count=0, send_transaction_hashes=0):
    subscribe_request = transactions_filter_stream_pb2.TransactionsWithProofsRequest()
    subscribe_request.from_block_hash = from_block_hash
    subscribe_request.from_block_height = from_block_height
    subscribe_request.count = count
    subscribe_request.send_transaction_hashes = send_transaction_hashes
    setattr(subscribe_request.bloom_filter, 'n_hash_funcs', bloom_filter['n_hash_funcs'])
    setattr(subscribe_request.bloom_filter, 'v_data', bloom_filter['v_data'])
    setattr(subscribe_request.bloom_filter, 'n_tweak', bloom_filter['n_tweak'])
    setattr(subscribe_request.bloom_filter, 'n_flags', bloom_filter['n_flags'])

    response = stubTransactions.subscribeToTransactionsWithProofs(subscribe_request, GRPC_REQUEST_TIMEOUT)

    return response


def applyStateTransition(state_transition):
    apply_request = platform_pb2.ApplyStateTransitionRequest()
    apply_request.state_transition = state_transition

    response = stub.applyStateTransition(apply_request, GRPC_REQUEST_TIMEOUT)

    return response


def main():
    identity_id =  base58.b58decode('GCAFKUdw7PtUcDEG8j3sicMJ4ngx1aTqCdb4HD5n5WZ7')
    contract_id = base58.b58decode('En3GRoMNAnt69firp32h3NEBxyveLcHQMUbwhDW2UqoX')
    transaction_id = '0f8409a5239150bc9a12c2d3b9a430dcc515ef562906a46e2bfb3ba418d8c9e3'

    bloom_filter = {
        "n_hash_funcs": 11,
        "v_data": b'',
        "n_tweak": 0,
        "n_flags": 0
    }

    get_identity(identity_id)
    get_data_contract(contract_id)
    get_documents(contract_id, 'thumbnailField', 'limit = 2')
    get_block('000000079cac3c9e8f40d200589d3935df984fcb89bbbe46f24653b7ccfb5e9c', 1)
    get_transaction(transaction_id)
    subscribeToTransactionsWithProofs(bloom_filter, from_block_height=1, count=1, send_transaction_hashes=0)
    getIdentityByFirstPublicKey(b'4e2736d0eecca645821089eb4b2422544e045655')
    getIdentityIdByFirstPublicKey(b'4e2736d0eecca645821089eb4b2422544e045655')
    send_transaction(b'03000000014f83880b387e1d4a639f8dd59083ab68f464516a060e4725cc1530a0ee2c3d41000000006b483045022100e7ea589971130f6221ec129b66696ecdd359576b7421e8ee5ab0c7e8c4dc3c460220075c25bd0384148de5636af8bc16f4cc271156d20a3eae26e6b590bfc84033d2012103a65caff6ca4c0415a3ac182dfc2a6d3a4dceb98e8b831e71501df38aa156f2c1ffffffff02204e0000000000001976a91409cf4b155dd5ca22979c1390df14aaaa1009bbee88ac44701a3d050000001976a91416b93a3b9168a20605cc3cda62f6135a3baa531a88ac00000000')
    applyStateTransition(b'pmR0eXBlAmdhY3Rpb25zgQFpZG9jdW1lbnRzgaZkJHJldgFlJHR5cGVocHJlb3JkZXJnJHVzZXJJZHgsR0pNVm51UzdYVFhkaWtnalFyRDR0TjVaSkNYem02eE12R0dyNVNkdGVjcDFoJGVudHJvcHl4InlVOXVta1Q0QnZjQWpQSmpGRVRGNW9CbUgzdEEyU3FKS2drJGNvbnRyYWN0SWR4LDJLZk1jTXhrdEtpbUp4QVpVZVp3WWtGVXNFY0FaaERLRXBRczhHTW5wVXNlcHNhbHRlZERvbWFpbkhhc2h4XjU2MmQ4Y2Q1YTQ1Nzg4ZWU0MWM3YzNiYWNhZGU5ODMwNGY0MTk0MzkyOTA4NDgxMzljOWZiZDU2MTI3NDY1NzM3NDJlNzQ2ODY1NzA2ODY1N2EzMzJlNjQ2MTczNjhpc2lnbmF0dXJleFhIMkxxMW5pM1cyR0Q0TXlqK3lzSHdOMExKRXdHSjExMTRaTHExL0dTalJxakliY2Z0VzcvUkpZVFozeFhnOW0wTTJ4SnVJSEwvMzVGUFVUdUkxUUFBSTg9b3Byb3RvY29sVmVyc2lvbgB0c2lnbmF0dXJlUHVibGljS2V5SWQB')


if __name__ == "__main__":
    main()
