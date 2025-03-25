import hashlib
import time
import json
from datetime import datetime


class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0):
        """
        Initialize a new block in the blockchain.

        Args:
            index (int): The block number/index
            transactions (list): List of transactions in the block
            previous_hash (str): Hash of the previous block in the chain
            nonce (int): The nonce used for proof-of-work
        """
        self.index = index
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        Calculate the SHA-256 hash of the block's contents.

        Returns:
            str: The hexadecimal digest of the block's hash
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def __str__(self):
        """
        String representation of the block for printing.
        """
        return (f"Block {self.index}:\n"
                f"Timestamp: {self.timestamp}\n"
                f"Transactions: {self.transactions}\n"
                f"Previous Hash: {self.previous_hash}\n"
                f"Nonce: {self.nonce}\n"
                f"Hash: {self.hash}\n")


class Blockchain:
    def __init__(self):
        """
        Initialize the blockchain with a genesis block.
        """
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 4  # Number of leading zeros required for proof-of-work
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        Create the first block in the blockchain (genesis block).
        """
        genesis_block = Block(0, ["Genesis Transaction"], "0")
        self.chain.append(genesis_block)

    def get_last_block(self):
        """
        Get the most recent block in the blockchain.

        Returns:
            Block: The last block in the chain
        """
        return self.chain[-1]

    def add_transaction(self, transaction):
        """
        Add a new transaction to the list of pending transactions.

        Args:
            transaction (str): The transaction to add
        """
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self):
        """
        Mine all pending transactions into a new block.
        """
        if not self.pending_transactions:
            print("No transactions to mine!")
            return

        last_block = self.get_last_block()
        new_block = Block(
            index=last_block.index + 1,
            transactions=self.pending_transactions,
            previous_hash=last_block.hash
        )

        # Proof of work
        new_block = self.proof_of_work(new_block)

        self.chain.append(new_block)
        self.pending_transactions = []  # Reset pending transactions

    def proof_of_work(self, block):
        """
        Simple proof-of-work algorithm that finds a nonce that makes the hash 
        meet the difficulty criteria.

        Args:
            block (Block): The block to perform proof-of-work on

        Returns:
            Block: The block with the valid nonce
        """
        print(f"Mining block {block.index}...")
        start_time = time.time()

        while not self.is_valid_nonce(block):
            block.nonce += 1
            block.hash = block.calculate_hash()

        end_time = time.time()
        print(
            f"Block mined in {end_time - start_time:.2f} seconds. Nonce: {block.nonce}")
        return block

    def is_valid_nonce(self, block):
        """
        Check if the block's hash meets the difficulty criteria.

        Args:
            block (Block): The block to check

        Returns:
            bool: True if the hash meets the difficulty, False otherwise
        """
        return block.hash.startswith("0" * self.difficulty)

    def is_chain_valid(self):
        """
        Validate the integrity of the blockchain.

        Returns:
            bool: True if the chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Check if current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                print(f"Block {current_block.index} has been tampered with!")
                return False

            # Check if current block points to the correct previous hash
            if current_block.previous_hash != previous_block.hash:
                print(
                    f"Block {current_block.index} points to an invalid previous hash!")
                return False

            # Check proof-of-work (for mined blocks beyond genesis)
            if i > 0 and not self.is_valid_nonce(current_block):
                print(
                    f"Block {current_block.index} has invalid proof-of-work!")
                return False

        return True

    def print_chain(self):
        """
        Print all blocks in the blockchain.
        """
        for block in self.chain:
            print(block)

    def tamper_with_chain(self, block_index, new_transaction):
        """
        Simulate tampering with a block's data (for demonstration purposes).

        Args:
            block_index (int): The index of the block to tamper with
            new_transaction (str): The new transaction to insert
        """
        if block_index < len(self.chain):
            self.chain[block_index].transactions.append(new_transaction)
            # Note: We don't recalculate the hash to demonstrate tampering
            print(
                f"Tampered with block {block_index} by adding a fake transaction!")
        else:
            print("Invalid block index for tampering!")


# Demonstration
if __name__ == "__main__":
    # Create a new blockchain
    my_blockchain = Blockchain()

    print("=== Initial Blockchain ===")
    my_blockchain.print_chain()

    # Add some transactions
    my_blockchain.add_transaction("Alice pays Bob 5 BTC")
    my_blockchain.add_transaction("Bob pays Charlie 3 BTC")

    # Mine the pending transactions
    my_blockchain.mine_pending_transactions()

    print("\n=== Blockchain after mining first block ===")
    my_blockchain.print_chain()

    # Add more transactions and mine again
    my_blockchain.add_transaction("Charlie pays Dave 1 BTC")
    my_blockchain.add_transaction("Dave pays Eve 0.5 BTC")
    my_blockchain.mine_pending_transactions()

    print("\n=== Blockchain after mining second block ===")
    my_blockchain.print_chain()

    # Validate the chain (should be valid)
    print("\n=== Blockchain Validation ===")
    if my_blockchain.is_chain_valid():
        print("Blockchain is valid!")
    else:
        print("Blockchain is invalid!")

    # Tamper with the chain (modify the first block after genesis)
    print("\n=== Tampering with the blockchain ===")
    my_blockchain.tamper_with_chain(1, "Hacker gives themselves 1000 BTC")

    # Validate again (should detect tampering)
    print("\n=== Blockchain Validation After Tampering ===")
    if my_blockchain.is_chain_valid():
        print("Blockchain is valid!")
    else:
        print("Blockchain is invalid!")
