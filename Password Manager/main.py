from kivymd.app import MDApp
from threading import Thread
import pickle, time
from kivymd.toast import toast
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from cryptography.fernet import Fernet
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty

class NavContent(BoxLayout):
	screen_drawer = ObjectProperty()
	nav_drawer = ObjectProperty()
	
	def go_home(self):
		self.screen_drawer.current = 'home'
		
class DialogContent(BoxLayout):
	pass
		
class PassApp(MDApp):
	name = ObjectProperty()
	password = ObjectProperty()
	flag = ObjectProperty()
	reference = ObjectProperty()
	icon_flag = ObjectProperty()
	Screen_drawer = ObjectProperty()
	ok_flag = False
	
	def on_start(self):
		threadObj = Thread(target=self.show_greet)
		threadObj.start()
		
	def show_greet(self):
		time.sleep(2)
		self.root.current = 'main'
		
	def check(self):
		if self.name.text and self.checkGateLock():
			self.reference.text = self.name.text
			self.screen_drawer.transition.direction = 'left'
			self.screen_drawer.current = 'view'
		elif not self.name.text:
			self.reference.text = "None"
			self.show_warning("Enter Account Name")
		elif not self.checkGateLock():
			self.reference.text = "None"
			self.show_warning("Incorrect password")
		else:
			self.reference.text = "None"
			self.show_warning("Something went wrong ppl")
		
	def show_hide(self):
		if self.flag.password:
			self.flag.password = False
			self.icon_flag.icon = "eye-off"
		else:
			self.flag.password = True
			self.icon_flag.icon = "eye"
			
	def passChecker(self, password):
		
		import re
		lowerCase = re.compile(r"[a-z]")
		upperCase = re.compile(r"[A-Z]")
		number = re.compile(r"\d")
	
		if len(password) < 6 or len(password) > 12:
			pass
		else:
			if not lowerCase.search(password):
				pass
			elif not upperCase.search(password):
				pass
			elif not number.search(password):
				pass
			else:
				return True
			
		return False
		
	def checkGateLock(self):
		self.password_check = self.password.text
		if self.passChecker(self.password_check) and self.fromGate(self.password_check):
			return True
		return False

	def fromGate(self, password):
		import os.path
		username = self.name.text
		if not os.path.exists('.gateLock.pkl'):
			self.show_warning("No account")
			return False
		with open('.gateLock.pkl', 'rb') as gateLock:
			saveAccnt = pickle.load(gateLock)
			for one_accnt in saveAccnt:
				if username in one_accnt:
					if password == self.decrypt(one_accnt[username]):
						return True
			return False
		
	def key_generate(self):
		key = Fernet.generate_key()
		with open(".secret.key", "wb") as key_file:
			key_file.write(key)
		
	def load_key(self):
		import os.path
		if not os.path.exists('.secret.key'):
			self.key_generate()
		return open('.secret.key', 'rb').read()
	
	def encrypt(self, plainText):
		key = self.load_key()
		f = Fernet(key)
		encrypted_text = f.encrypt(plainText.encode())
		return encrypted_text
	
	def decrypt(self, code):
		key = self.load_key()
		f = Fernet(key)
		decrypted_text = f.decrypt(code)
		return decrypted_text.decode()
		
	def create_new_account(self):
		password = self.password.text
		confirm_password = self.flag.text
		username = self.name.text
		accnt = self.readFile(".gateLock.pkl")
		if self.passChecker(password) and (password == confirm_password) and username:
			password = self.encrypt(password)
			if not accnt == []:
				for one_accnt in accnt:
					if username in one_accnt:
						self.show_warning("You have an account yet")
						return
				one_accnt = {}
				one_accnt[username] = password
				accnt.append(one_accnt)
			else:
				one_accnt = {}
				one_accnt[username] = password
				accnt.append(one_accnt)
			with open('.gateLock.pkl', 'wb') as gateLock:
				pickle.dump(accnt, gateLock)
				self.screen_drawer.current = 'home'
				
		elif not username:
			self.show_warning("Enter Account name")
				
		elif password != confirm_password:
			self.show_warning("Confirm password and New password is not same")
			
		elif not self.passChecker(password):
			self.show_warning("Incorrect password")
	
	def readFile(self, filename):
		import os.path
		if os.path.exists(filename):
			with open(filename, "rb") as file:
				accnt = pickle.load(file)
				return accnt		
		return []
		
	def writeFile(self, filename, passDict):
		with open(filename, "wb") as file:
			pickle.dump(passDict, file)
		
	def show_warning(self, text1):
		dialog = MDDialog(
			title ="Warning",
			text = text1
		)
		dialog.open()
		
	def setPass(self):
		username = self.name.text
		accnt_name = self.reference.text.capitalize()
		password = self.password.text
		if not accnt_name:
			self.show_warning("Enter Account Name")
			return
		if not password:
			self.show_warning("Enter Password")
			return
		PASSDICT = self.readFile('.saveFile.pkl')
		if PASSDICT != []:
			for one_accnt in PASSDICT:
				if username in one_accnt:
					if accnt_name in one_accnt[username]:
						self.show_warning("Account is available here")
						return
					one_accnt[username][accnt_name] = self.encrypt(password)
				elif username not in one_accnt:
					one_accnt[username] = {accnt_name: self.encrypt(password)}
		elif PASSDICT == []:
			one_accnt = {}
			one_accnt[username] = {accnt_name: self.encrypt(password)}
			PASSDICT.append(one_accnt)
		self.writeFile(".saveFile.pkl", PASSDICT)
		self.show_done()
	
	def showPass(self):
		username = self.name.text
		accnt_name = self.reference.text.capitalize()
		PASSDICT = self.readFile(".saveFile.pkl")
		if PASSDICT != []:
			for one_accnt in PASSDICT:
				if username in one_accnt:
					if accnt_name in one_accnt[username]:
						self.icon_flag.text = self.decrypt(one_accnt[username][accnt_name])
						return
					elif accnt_name not in one_accnt[username]:
						self.show_warning('No such account saved yet')
						return
				elif username not in one_accnt:
					self.show_warning('You have no account saved yet')
					return
		elif PASSDICT == []:
			self.show_warning('You have no account saved yet')
			return
			
	def changePass(self):
		username = self.name.text
		accnt_name = self.reference.text.capitalize()
		password = self.password.text
		if not accnt_name:
			self.show_warning("Enter Account Name")
			return
		if not password:
			self.show_warning("Enter Password")
			return
		PASSDICT = self.readFile('.saveFile.pkl')
		if PASSDICT != []:
			for one_accnt in PASSDICT:
				if username in one_accnt:
					if accnt_name in one_accnt[username]:
						one_accnt[username][accnt_name] = self.encrypt(password)
				elif username not in one_accnt:
					self.show_warning("No such account saved yet")
					return
		elif PASSDICT == []:
			self.show_warning("No such account saved yet")
			return
		self.writeFile(".saveFile.pkl", PASSDICT)
		self.show_done()
		
	def deletePass(self):
		username = self.name.text
		accnt_name = self.reference.text.capitalize()
		if not accnt_name:
			self.show_warning("Enter Account Name")
			return
		PASSDICT = self.readFile('.saveFile.pkl')
		if PASSDICT != []:
			for one_accnt in PASSDICT:
				if username in one_accnt:
					if accnt_name in one_accnt[username]:
						del one_accnt[username][accnt_name]
						self.dialog.dismiss()
					elif accnt_name not in one_accnt[username]:
						self.show_warning('No such account saved yet')
						return
				elif username not in one_accnt:
					self.show_warning("No such account saved yet")
					return
		elif PASSDICT == []:
			self.show_warning("No such account saved yet")
			return
		self.writeFile(".saveFile.pkl", PASSDICT)
		self.show_done()
		self.reference.text = ''
		
	def show_confirm(self):
		self.dialog = MDDialog(
			title="Confirmation",
			text="delete",
			auto_dismiss=False,
			buttons=[
				MDFlatButton(
					text="CANCEL",
					on_release= lambda x: self.dialog.dismiss(),
					text_color=self.theme_cls.primary_color
				),
				MDFlatButton(
					text="OK",
					on_release= lambda x: self.deletePass(),
					text_color=self.theme_cls.primary_color
				)
			]
		)
		self.dialog.open()
		
	def show_done(self):
		done = MDDialog(
			title="Done!",
			auto_dismiss=False,
			buttons=[
				MDIconButton(
					icon="checkbox-multiple-marked-circle-outline",
					on_release= lambda x: done.dismiss()
				)
			]
		)
		done.open()
		
	def show_toast(self):
		toast("Text was copied")
		
	def about_app(self):
		dialog = MDDialog(
			title="About",
			type="custom",
			content_cls=DialogContent()
		)
		dialog.open()



if __name__ == "__main__":
	PassApp().run()