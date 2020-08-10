from kivymd.app import MDApp
import time, re
from threading import Thread
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog

class Content(BoxLayout):
	pass

class EmptyApp(MDApp):
	
	dir = {}

	def searchAnd(self, folder):
	
		androidMatch = re.compile(rf"{self.dir['root']}\/Android(.*)?")
		matche = androidMatch.search(folder)
		return matche
		
	def delete(self):
		self.root.ids.lbl_text.text = ''
		self.root.ids.countdown.text = f"[b]0[/b] file clean"
		threadObj = Thread(target=self.check)
		threadObj.start()
		
	def check(self):
		self.count = 0
		self.dir['root'] = '/storage/emulated/0'
		self.emptyList = []
		self.countList = []
		self.update_check()
		

	def update_check(self):
		while True:
			for folder, subfolder, file in os.walk(self.dir['root']):
				self.root.ids.check.text = "Check: " + str(folder)
				if self.searchAnd(folder):
					continue
				if os.listdir(folder) == []:
					self.emptyList.append(folder + " is deleted...")
					self.count += 1
					self.emptyList = "\n".join(self.emptyList)
					self.root.ids.lbl_text.text = self.emptyList
					self.emptyList = self.emptyList.split("\n")
					self.root.ids.countdown.text = f"[b]{self.count}[/b] file clean"
					try:
						os.rmdir(folder)
						listOf = folder.split(os.sep)
						self.interval += len(listOf)
					except Exception as e:
						pass
			self.countList.append(self.count)
			if (len(self.countList) > 1) and (self.countList[-1] == self.countList[-2]):
				self.root.ids.countdown.text = f"Finally: [b]{self.count}[/b] file clean"
				break		
			elif self.count <= 0:
				self.root.ids.countdown.text = f"Finally: [b]{self.count}[/b] file clean"
				break
			
			
		
	def show(self):
		
		self.dialog = MDDialog(
			title="About",
			type="custom",
			content_cls=Content()
		)
		self.dialog.open()
	
	
if __name__ == "__main__":
	EmptyApp().run()