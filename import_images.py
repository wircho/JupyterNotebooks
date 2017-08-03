from tag_image_tools import Folder, Cat, all_categories, top, images, all_image_names
import pickel

NO = "NO"
YES = "YES"

class Import:
	def __init__(self, cat, val):
		self.cat = cat
		self.val = val
	def desc(self):
		return self.cat + "." + self.val

imports = []
done = False

def get_cat(message):
	global done
	name = input(message)
	if name == "finish!":
		done = True
		return None
	for cat in all_categories:
		if cat.name == name: return cat
	return None


def get_import():
	print("Current imports: " + str(list([i.desc() for i in imports])))
	cat = get_cat("Enter a category (type \"finish!\" if you're done): ")
	if done: return
	while cat is None:
		cat = get_cat("Enter a valid category (type \"finish!\" if you're done): ")
		if done: return

while not done:
	get_import()

info_path = input("Image info path (no .pkl): ") + ".pkl"
info = pickle.load(open(info_path, "rb"))

label_names = info["label_names"]

print("All labels: " + str(label_names))

selected_label = input("Select a label to import: ")

print("Gathering image names...")
names = info["names"]
labels = info["labels"]
selected_names = []
for i in range(0, len(names)):
	if labels[i] == selected_label: selected_names.append(names[i])

print("Gathered " + str(len(selected_names)) + " image names.")

for imp in imports:
	print("Copying images to " + imp.desc() + "...")
	folder = None
	if imp.val is YES:
		folder = imp.cat.yes
	elif imp.val is NO:
		folder = imp.cat.no
	if folder is None:
		print("Wrong import value!")
		continue
	for name in selected_names: images.copy(name, folder)
	print("Copied!")


