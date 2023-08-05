import grpc
import cbor2

# Generated from dapi-grpc
import dapiclient.rpc.grpc.core_pb2 as core_pb2
import dapiclient.rpc.grpc.core_pb2_grpc as core_pb2_grpc
import dapiclient.rpc.grpc.platform_pb2 as platform_pb2
import dapiclient.rpc.grpc.platform_pb2_grpc as platform_pb2_grpc
import dapiclient.rpc.grpc.transactions_filter_stream_pb2 as transactions_filter_stream_pb2
import dapiclient.rpc.grpc.transactions_filter_stream_pb2_grpc as transactions_filter_stream_pb2_grpc


class GRpcClient:

    def __init__(self):
        pass

    def request(socket, method, params = {}, options = {'timeout': 5}):
        channel = grpc.insecure_channel(socket)
        #print(socket)

        stub = platform_pb2_grpc.PlatformStub(channel)
        stubCore = core_pb2_grpc.CoreStub(channel)
        stubTransactions = transactions_filter_stream_pb2_grpc.TransactionsFilterStreamStub(channel)

        if method == 'getIdentity':
            return GRpcClient.getIdentity(stub, params, options)

        elif method == 'getDataContract':
            return GRpcClient.getDataContract(stub, params, options)

        elif method == 'getDocuments':
            return GRpcClient.getDocuments(stub, params, options)

        elif method == 'applyStateTransition':
            return GRpcClient.applyStateTransition(stub, params, options)

        elif method == 'getIdentityByFirstPublicKey':
            return GRpcClient.getIdentityByFirstPublicKey(stub, params, options)

        elif method == 'getIdentityIdByFirstPublicKey':
            return GRpcClient.getIdentityIdByFirstPublicKey(stub, params, options)

        elif method == 'getBlock':
            return GRpcClient.getBlock(stubCore, params, options)

        elif method == 'getStatus':
            return GRpcClient.getStatus(stubCore, params, options)

        elif method == 'getTransaction':
            return GRpcClient.getTransaction(stubCore, params, options)

        elif method == 'sendTransaction':
            return GRpcClient.sendTransaction(stubCore, params, options)

        elif method == 'subscribeToTransactionsWithProofs':
            return GRpcClient.subscribeToTransactionsWithProofs(stubTransactions, params, options)

        else:
            raise ValueError('Unknown gRPC endpoint: {}'.format(method))


    def getIdentity(stub, params, options):
        # Create Identity request
        identity_request = platform_pb2.GetIdentityRequest()
        # Set identity parameter of request
        identity_request.id = params['id']

        response = stub.getIdentity(identity_request, options['timeout'])
        return cbor2.loads(response.identity)


    def getDataContract(stub, params, options):
        contract_request = platform_pb2.GetDataContractRequest()
        contract_request.id = params['id']

        response = stub.getDataContract(contract_request, options['timeout'])
        #print('Data Contract: {}\n'.format(cbor2.loads(response.data_contract)))

        return cbor2.loads(response.data_contract)


    def getDocuments(stub, params, options):
        #print(params)

        document_request = platform_pb2.GetDocumentsRequest()
        document_request.data_contract_id = params['data_contract_id']
        document_request.document_type =  params['document_type']
        document_request.where = params['where']
        document_request.order_by = params['order_by']
        document_request.limit =  params['limit']
        document_request.start_at =  params['start_at']
        document_request.start_after = params['start_after']

        response = stub.getDocuments(document_request, options['timeout'])

        #for d in response.documents:
        #    print('Document cbor: {}\n'.format(cbor2.loads(d)))

        return response.documents

    def getBlock(stubCore, params, options):
        block_request = core_pb2.GetBlockRequest()
        block_request.hash = params['hash']
        block_request.height = params['height']

        response = stubCore.getBlock(block_request, options['timeout'])
        return cbor2.loads(response.block)

    def getStatus(stubCore, params, options):
        status_request = core_pb2.GetStatusRequest()

        response = stubCore.getStatus(status_request, options['timeout'])

        return response

    def getTransaction(stubCore, params, options):
        transaction_request = core_pb2.GetTransactionRequest()
        transaction_request.id = params['id']

        response = stubCore.getTransaction(transaction_request, options['timeout'])

        return response.transaction

    def sendTransaction(stubCore, params, options):
        transaction_request = core_pb2.SendTransactionRequest()
        transaction_request.transaction = params['transaction']
        transaction_request.allow_high_fees = params['allow_high_fees']
        transaction_request.bypass_limits = params['bypass_limits']

        response = stubCore.sendTransaction(transaction_request, options['timeout'])

        return response

    def subscribeToTransactionsWithProofs(stubTransactions, params, options):
        subscribe_request = transactions_filter_stream_pb2.TransactionsWithProofsRequest()
        subscribe_request.from_block_hash = params['from_block_hash']
        subscribe_request.from_block_height = params['from_block_height']
        subscribe_request.count = params['count']
        subscribe_request.send_transaction_hashes = params['send_transaction_hashes']
        setattr(subscribe_request.bloom_filter, 'n_hash_funcs', params['bloom_filter']['n_hash_funcs'])
        setattr(subscribe_request.bloom_filter, 'v_data', params['bloom_filter']['v_data'])
        setattr(subscribe_request.bloom_filter, 'n_tweak', params['bloom_filter']['n_tweak'])
        setattr(subscribe_request.bloom_filter, 'n_flags', params['bloom_filter']['n_flags'])

        response = stubTransactions.transactionWithProof(subscribe_request, options['timeout'])

        return response

    def applyStateTransition(stub, params, options):
        apply_request = platform_pb2.ApplyStateTransitionRequest()
        apply_request.state_transition = params['state_transition']

        response = stub.applyStateTransition(apply_request, options['timeout'])

        return response

    def getIdentityByFirstPublicKey(stub, params, options):
        request = platform_pb2.GetIdentityByFirstPublicKeyRequest()
        request.public_key_hash = params['public_key_hash']

        response = stub.getIdentityByFirstPublicKey(request, options['timeout'])

        return response

    def getIdentityIdByFirstPublicKey(stub, params, options):
        request = platform_pb2.GetIdentityIdByFirstPublicKeyRequest()
        request.public_key_hash = params['public_key_hash']

        response = stub.getIdentityIdByFirstPublicKey(request, options['timeout'])

        return response
