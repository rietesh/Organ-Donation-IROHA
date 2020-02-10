import os
import binascii
from iroha import IrohaCrypto
from iroha import Iroha, IrohaGrpc
from iroha.primitive_pb2 import can_set_my_account_detail
import sys

if sys.version_info[0] < 3:
    raise Exception('Python 3 or a more recent version is required.')


IROHA_HOST_ADDR = os.getenv('IROHA_HOST_ADDR', '127.0.0.1')
IROHA_PORT = os.getenv('IROHA_PORT', '50051')
ADMIN_ACCOUNT_ID = os.getenv('ADMIN_ACCOUNT_ID', 'admin@odwa')
ADMIN_PRIVATE_KEY = os.getenv(
    'ADMIN_PRIVATE_KEY', 'f101537e319568c765b2cc89698325604991dca57b9716b58016b253506cab70')

user_private_key = IrohaCrypto.private_key()
user_public_key = IrohaCrypto.derive_public_key(user_private_key)
iroha = Iroha(ADMIN_ACCOUNT_ID)
net = IrohaGrpc('{}:{}'.format(IROHA_HOST_ADDR, IROHA_PORT))

def user_pub_priv_key():
    user_private_key = IrohaCrypto.private_key()
    user_public_key = IrohaCrypto.derive_public_key(user_private_key)
    return user_private_key, user_public_key

def send_transaction_and_print_status(transaction):
    hex_hash = binascii.hexlify(IrohaCrypto.hash(transaction))
    print('Transaction hash = {}, creator = {}'.format(
        hex_hash, transaction.payload.reduced_payload.creator_account_id))
    net.send_tx(transaction)
    to_send_back = []
    to_send_back.append(hex_hash)
    for status in net.tx_status_stream(transaction):
        to_send_back.append(status)
    return to_send_back

################################  Donors.html  ##############################################
def create_asset(assetss):
    """
    Creates domain 'domain' and asset 'coin#domain' with precision 2
    iroha.command('CreateDomain', domain_id='donor', default_role='user'),
    """
    commands = [
        iroha.command('CreateAsset', asset_name=assetss,
                      domain_id='organ', precision=0)
    ]
    tx = IrohaCrypto.sign_transaction(
        iroha.transaction(commands), ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


def add_coin_to_admin(assetss):
    """
    Add 1000.00 units of 'coin#domain' to 'admin@odwa'
    """
    assetid = assetss+'#'+'organ'
    tx = iroha.transaction([
        iroha.command('AddAssetQuantity',
                      asset_id=assetid, amount='10')
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    send_transaction_and_print_status(tx)


def create_account_donor(name,ass):
    """
    Create account
    """
    accid = name+'@'+'patient'
    assetid = ass+'#'+'organ'
    priv,pub = user_pub_priv_key()
    tx = iroha.transaction([
        iroha.command('CreateAccount', account_name=name, domain_id='patient',
                      public_key=pub),
        iroha.command('TransferAsset', src_account_id='admin@odwa', dest_account_id=accid,
                      asset_id=assetid, description='init top up', amount='1')
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    res = send_transaction_and_print_status(tx)
    return res

def transfer_coin_from_src_to_dest(src,dest,ass):
    """
    Transfer 1 'organ' from 'donor' to 'patient'
    """
    srcaccid = src+'@'+'patient'
    destaccid = dest+'@'+'patient'
    assetid = ass+'#'+'organ'
    tx = iroha.transaction([
        iroha.command('TransferAsset', src_account_id='admin@odwa', dest_account_id=destaccid,
                      asset_id=assetid, description='Transferred', amount='1')
    ])
    IrohaCrypto.sign_transaction(tx, ADMIN_PRIVATE_KEY)
    result = send_transaction_and_print_status(tx)
    return result

##########################################################################


############################  Query.html #################################
def get_account_assets(name):
    """
    List all the assets of an account
    """
    accid = name+'@'+'patient'
    query = iroha.query('GetAccountAssets', account_id=accid)
    IrohaCrypto.sign_query(query, ADMIN_PRIVATE_KEY)

    response = net.send_query(query)
    data = response.account_assets_response.account_assets
    res = []
    for asset in data:
        res.append(asset)
    return res

#########################################################################


print('done')
