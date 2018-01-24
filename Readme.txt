=================
Goofy Coin system
=================

->Use of Hashing algorithms - SHA256

->Use of RSA to generate public/private keys for digital signatures

->Class Node: is implemented that contains the data structure required for a transaction
	-data structure used:
		.id 			 = unique id that is generated each time a block enters the goofy system
		.dirty 			 = flag to check whether any malicious act is done with the system like attempt to change the structure
		.amount 		 = amount transferred between sender and receiver in the particular transaction
		.next 			 = a pointer to the next block in the transaction
		.prev    		 = a pointer to the previous block from which this transaction is splitted (None for coinbased transactions)
		.sender			 = sender's public key (uniquely generated using RSA algo.)
		.receiver 		 = receiver's public key (uniquely generated using RSA algo.)
		.parent_block_id = id of the previous block to which prev pointer is pointing
		.transaction	 = a log that is written during the transfer of money between sender and receiver
		.spentflag	 	 = flag to check whether the money in the current block is spent or available for further transactions (0=unspent,1=spent)
		.timestamp		 = time at which the transaction is happened and block is added to the system
		.signature 		 = cryptographically generated hash used to authenticate the sender and thus the validity of the transaction


->Class Blockchain: contains various methods used for making a shared-append-only ledger and the starting Genesis block
		


------------------------------------------------------------------------
Various methods:-

1) Add user: to add a user to the Goofy coin system

2) Make coin: utility to help Goofy make coin

3) Do transaction: sender can send some Goofy coin to the receiver

4) Show Blockchain: to view the current blockchain of the Goofy system

5) Show users & bal: the intermediate function to display the users in the system and the total of all the balance they are having in chinks

6) Verify transaction: to verify if a particular transaction is valid or not

7) Change a block: to change a block with a particular id and we will notice that it will affect the blocks linked with it and blockchain becomes invalid

8) Is chain valid: to check whether the chain has been corrupted or not
-------------------------------------------------------------------------

------------------------------------
Input format:-
-Completely Menu Driven program
-Handled corner cases and rejections
------------------------------------