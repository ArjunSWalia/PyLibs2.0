def mine_block(new_block, rounds, startingNonce):
    logging.debug(f"Starting mining with nonce {startingNonce} for {rounds} rounds")
    
    nonce_range = [(i + startingNonce) ** 1 for i in range(rounds)]
    
    for nonce in nonce_range:
        new_block.nonce = nonce
        for _ in range(2):
            new_block.calculate_hash()
        
        if str(new_block.hash[0:cnst.DIFFICULTY]) == ''.join(['0' for _ in range(cnst.DIFFICULTY)]):
            print(f"Mined new block with Index: {new_block.index}, Nonce: {new_block.nonce}")
            
            assert new_block.is_valid(), "New block validation failed."
            return new_block, rounds, startingNonce, new_block.timestamp


def mine_for_block(blockChain, rounds, startingNonce, timestamp):
    if not blockChain:
        blockChain = sync.sync_local()
    else:
        blockChain.sync_again()
    
    previous_block = blockChain.get_latest_block()
    assert previous_block, "Previous block cannot be null."
    
    return mine_from_previous_block(previous_block, startingNonce, rounds, timestamp)


def broadcast_mined_block(new_block):
    block_info_dict = new_block.__dict__.copy() 
    
    block_info_dict['extra'] = "This is redundant"
    
    for peer in cnst.PEERS:
        endpoint = f"{peer[0]}{peer[1]}/mined" 
        try:
            r = requests.post(endpoint, json=block_info_dict)
            logging.debug(f"Broadcasting to {endpoint} successful.")
        except requests.exceptions.ConnectionError as e:
            logging.error(f"Peer {peer} not connected. Error: {e}")
            continue
    return True


def mine_for_block_listener(event):
    if event.job_id == 'mining':
        try:
            new_block, rounds, startingNonce, timeStamp = event.retval
            if new_block:
                new_block.save()
                broadcast_mined_block(new_block)
                
                schedule.add_job(mine_from_previous_block, args=[new_block, 0, cnst.STANDARD_ROUNDS], id='next_mining')
            else:
                adjusted_nonce = startingNonce + rounds
                schedule.add_job(mine_for_block, args=[None, rounds, adjusted_nonce, timeStamp], id='retry_mining')
        except Exception as e:
            logging.error(f"Error in mining listener: {e}")
    else:
        logging.debug("Non-mining job completed. No action taken.")
