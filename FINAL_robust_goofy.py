'''
/*
*Team Details:
*
*  Vishnu Priya Marripati - R.No. 20173090
*  Shubham Verma - R.No. 20172035
*/
'''


import datetime as dt
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Hash import SHA256

#private_key = RSA.generate(2048,prng)
#public_key = private_key.publickey()
#generate return RSA key object

class block:
	def __init__(self,id,sender,receiver,amount,transaction,spentflag,parent_block_id,signature):
		self.id = id
		self.dirty = 0
		self.amount = amount
		self.next = None
		self.prev = None
		self.sender = sender
		self.receiver = receiver
		self.parent_block_id = parent_block_id
		self.transaction = transaction
		self.spentflag = spentflag	 #0-not spent, 1-spent
		self.timestamp = dt.datetime.now().strftime("Created on %d %b,%y(%A) at %I:%M:%S %p")	#dt.date.today().weekday()
		self.signature = signature
		#also add minted variable to keep diff between goofy to goofy...
		#and goofy to anyone splitted having also goofy to goofy


class blockchain:
	def __init__(self):
		self.head=None
		self.id=0

	def blockid(self):
		self.id+=1
		return self.id

	def ischainempty(self):#return true/false
		return self.head == None

	def addblock(self,block_id,sender,receiver,amount,transaction,spentflag,parent_block_id,signature):
		#### if you have 0 bitcoin, you can't pay as you have spent all bitcoin ####
		if amount == 0:
			spentflag = 1
		temp=block(block_id,sender,receiver,amount,transaction,spentflag,parent_block_id,signature)
		############################

		h=self.head
		if h == None:
			self.head = temp
		else:
			while h.next != None:
				h=h.next
			h.next=temp

	def getlatestblock(self):
		t = self.head
		while t.next != None:
			t = t.next
		return t


	def getblock_by_id(self,vid):
		t = self.head
		while t != None:
#			print 'current_block_id',t.id
			if t.id == vid:
				return t
			t = t.next

	def isvalid(self,vid):
		if self.getblock_by_id(vid).dirty:
			return False
		else:
			return True

	def printchain(self):
		print 'chain\n['
		t=self.head
		while t != None:# '!=' is equivalent to 'is not'
			#using SHA256 for shortening long public and private keys and signature also...
			print '''
  {
     ID: ''',t.id,'''
     Is Valid: ''',self.isvalid(t.id),'''
     Sender(Public Key): ''',SHA256.new(t.sender.exportKey('PEM')).hexdigest(),'''
     Receiver(Public Key): ''',SHA256.new(t.receiver.exportKey('PEM')).hexdigest(),'''
     Parent: ''',t.parent_block_id,'''
     Amount: ''',t.amount,'''
     Transaction: ''',t.transaction,'''
     Timestamp: ''',t.timestamp,'''
     Spent: ''',t.spentflag,'''
     Signature:''',SHA256.new(str(t.signature)).hexdigest(),'''
  }
			'''
			t=t.next
		print ']'



def main():

	def getkeys():
		prng = Random.new().read
		key = RSA.generate(2048,prng)
		private_key = key#.exportKey('PEM')
		public_key = key.publickey()#.exportKey('PEM')
		keys=[private_key,public_key]
		return keys

	def add_user():
		###### local reference ######
		name = raw_input('Enter username: ').lower()
		if name in users:
			print 'User already exists !'
			return
		users[name] = [getkeys(),0]
		#############################

	def show_users():
		###### local reference ######
		if not users:
			print 'No users are there in system !'
		else:
			for i in users:
				print i,' has ',users[i][1],' bitcoin in total'
		#############################

	def transact():
		sender = raw_input('Enter Sender: ').lower()
		receiver = raw_input('Enter Receiver:').lower()
		amt = int(raw_input('Enter amount: '))

		if sender not in users:
			print "User:",sender,"don't exist!"
			ch = raw_input('Add user(Y/N)?')
			if ch.lower() == 'y':
				add_user()
			return

		if receiver not in users:
			print "User:",receiver,"don't exist!"
			ch = raw_input('Add user(Y/N)?')
			if ch.lower() == 'y':
				add_user()
			return


		#### precheck balance then only go forward ####
		if users[sender][1] == 0:
			print sender,"have 0 balance !"
			return

		######## work on cryptography

		############################

		t = chain.head
		while t != None:
			#comparing pulbic keys of the two nodes
			if t.receiver == users[sender][0][1] and t.spentflag == 0 and amt <= t.amount:
				current_amt = t.amount
				t.spentflag = 1
				parent_block_id = t.id
				###### local reference ######
				users[sender][1] = users[sender][1]-amt
				users[receiver][1] = users[receiver][1]+amt
				#############################
				break
			else:
				t = t.next

			if t == None:
				print sender,' is trying to spend more than what they have !'
				return
		#############################



		#### we can add block before verifying the transaction by meeting certain conditions or during the time of adding block...

		transaction1 = sender+' paid '+str(amt)+' coins to '+receiver
		transaction2 = sender+' paid '+str(current_amt-amt)+' coins to '+sender

		id1 = chain.blockid()
		id2 = chain.blockid()
		data_for_signature1 = str(id1)+str(users[sender][0][1])+transaction1+str(amt)
		data_for_signature2 = str(id2)+str(users[sender][0][1])+transaction2+str(current_amt-amt)

		sign1 = calculate_signature(users[sender][0][0],data_for_signature1)
		sign2 = calculate_signature(users[sender][0][0],data_for_signature2)


		chain.addblock(id1,users[sender][0][1],users[receiver][0][1],amt,transaction1,0,parent_block_id,sign1)
		chain.getlatestblock().prev = chain.getblock_by_id(parent_block_id)

		chain.addblock(id2,users[sender][0][1],users[sender][0][1],current_amt-amt,transaction2,0,parent_block_id,sign2)
		chain.getlatestblock().prev = chain.getblock_by_id(parent_block_id)

	def display_chain():
		print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'
		chain.printchain()
		print '@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@'

	def make_coin():
		no = int(raw_input('Enter no. of coins: '))
		
		######## local reference #######
		users['goofy'][1]=users['goofy'][1]+no
		################################

		transaction = 'Goofy created '+str(no)+' more coins in the system!'

		#no need to add str(None) in data_for_signature here in make_coin
		id = chain.blockid()
		data_for_signature = str(id)+str(users['goofy'][0][1])+transaction+str(no)
		sign = calculate_signature(users['goofy'][0][0],data_for_signature)

		chain.addblock(id,users['goofy'][0][1],users['goofy'][0][1],no,transaction,0,None,sign)


	def calculate_signature(sender_private_key,data):
		digest = SHA256.new(data).hexdigest()#digest or hash same thing
		signature = sender_private_key.sign(digest,'')
		return signature


	def match_signature(sender_public_key,data,signature):
		digest = SHA256.new(data).hexdigest()
		return sender_public_key.verify(digest,signature)


	def verify():
		vid = int(raw_input('Enter the block id(to verify): '))
		found = chain.getblock_by_id(vid)
		if found == None:
			print "Block don't exist !"
			return
		# if found.prev == None:
		# 	print 'Transaction is valid !'
		# else:

		current_signature = found.signature
		current_transaction = found.transaction
		current_amt = found.amount
		current_sender = found.sender
		current_id = found.id

		while found.prev != None:
			# ########### finding sender name to get its private key from the local data structure(dictionary) ###########
			# for i in users:
			# 	if users[i][0][1] == found.sender:
			# 		sender_name = i
			# 		break
			# ###########################################

			data_for_signature = str(current_id)+str(current_sender)+current_transaction+str(current_amt)
			# sign = calculate_signature(users[sender_name][0][0],data_for_signature)

			if match_signature(current_sender,data_for_signature,current_signature):
				found = found.prev
			else:
				print 'Transaction is NOT VALID !'
				return
			current_signature = found.signature
			current_transaction = found.transaction
			current_amt = found.amount
			current_sender = found.sender
			current_id = found.id

		data_for_signature = str(current_id)+str(current_sender)+current_transaction+str(current_amt)
		if match_signature(current_sender,data_for_signature,current_signature):
			print 'Transaction is VALID !'
		else:
			print 'Transaction is NOT VALID !'

	def change_block():
		cb = int(raw_input('Enter block id to change: '))
		bk = chain.getblock_by_id(cb)
		bk.amount = 5000
		bk.dirty = 1


	def ischain_valid():
		t = chain.head
		if t == None:
			print 'Chain is empty, do some transactions first !'
			return
		while t != None:
			# checking if block is dirty or not, if it is then not valid
			if not chain.isvalid(t.id):
				print 'Chain is NOT VALID !'
				return
			t = t.next
		print 'Chian is VALID !'

	#name vs [[private_key,public_key],amount]
	users={
	'goofy':[getkeys(),0]
	}
	chain = blockchain()


	while(True):
		print '''
	|------- MENU --------|
	| 1.Add user          |
	| 2.Make coin         |
	| 3.Do transaction    |
	| 4.Show blockchain   |
	| 5.Show users & bal. |
	| 6.Verify transaction|
	| 7.Change a block    |
	| 8.Is chain valid?   |
	| 9.Exit              |
	|---------------------|'''
		try:
			ch=int(raw_input())
		except Exception:
			print 'Please enter choice no. !'
			continue
		myswitch={
		1:add_user,
		2:make_coin,
		3:transact,
		4:display_chain,
		5:show_users,
		6:verify,
		7:change_block,
		8:ischain_valid,
		9:exit
		}
		#handle wrong choice error
		try:
			myswitch.get(ch)()
		except Exception:
			print 'Invalid entry, Try again !'



if __name__ == '__main__':
	main()