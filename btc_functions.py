from bitcoinrpc.authproxy import JSONRPCException
btc_unit = 100000000

def get_tx(tx_hash, rpc_connection):
    try:
        tx = rpc_connection.getrawtransaction(tx_hash, True)
    except JSONRPCException:
        return []
    
    tx_struct = {}
    tx_struct['hash'] = tx['txid']
    tx_struct['time'] = tx['time']
    tx_struct['out'] = get_out_addrs(tx)
    tx_struct['in'] = get_in_addrs(tx, rpc_connection)

    total_out = sum([y for x, y in tx_struct['out']])
    total_in = sum([y for x, y in tx_struct['in']])
    tx_fees = total_in - total_out

    tx_struct['value'] = total_out
    tx_struct['fees'] = tx_fees
    return tx_struct

def get_raw_tx(tx_hash, rpc_connection):
    try:
        return rpc_connection.getrawtransaction(tx_hash, True)
    except JSONRPCException:
        return None

def get_out_addrs(tx):
    out_info = [(x['scriptPubKey']['addresses'], (int) (x['value'] * btc_unit)) 
        for x in tx['vout'] if 'addresses' in x['scriptPubKey']]
    out_addrs = [(x[0], y) for x, y in out_info if len(x) >= 1]
    return out_addrs

def get_in_addrs(tx, rpc_connection):
    funding_txs = [(get_raw_tx(x['txid'], rpc_connection), x['vout'])for x in tx['vin']]
    return [get_out_addrs(tx)[out_inx] for tx, out_inx in funding_txs]

def coalesce_input_addrs(tx_input):
    """
    Function takes as argument a list of input addresses for a specific transaction and groups
    them together based on the wallet address, aggregating the amount of money spent by each
    address in transaction.

    For example,  the input [("addr1", 10), ("addr2", 5), ("addr1", 5)] is grouped to
    {"addr1": 15, "addr2": 5}

    Parameters:
        tx_inputs (lst): list of tuples where each tuple consists of a wallet address
                        along with the amount of bitcoin sent (i.e. tx linking)
    
    Returns:
        dct: a dictionary similar to example described above
    """

    dct_tmp = {x: [b for a, b in tx_input if a is x] for x, y in tx_input}
    return {x: sum(y) for x, y in dct_tmp.items()}
