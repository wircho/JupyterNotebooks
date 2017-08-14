from IPython.display import Image, display, clear_output, HTML
import ipywidgets as widgets
from tag_image_tools import Folder, Cat, all_categories, top, images, all_image_names
from tag_images_social_widget import KeyWidget

print("All categories: " + ", ".join(cat.name for cat in all_categories))

def input_category(q):
    value = input(q)
    for cat in all_categories:
        if cat.name == value: return cat
    return None

selected_category = input_category("Enter a category (case sensitive): ")
while selected_category is None:
    selected_category = input_category("Please enter a valid category (case sensitive): ")

clear_output()
display(HTML("You have selected <b>" + selected_category.name + "</b>"))
sample_base = "\\\\stelvio.net\\mtl\\Public\\Sensus\\sensus_samples\f\samples_"
display(HTML("Here are some examples of images in this category: <a target='_blank' href='file:" + sample_base + selected_category.name + "'>" + sample_base + selected_category.name + "</a>"))
# display(HTML("Below are examples of images from all other categories:"))
# for cat in all_categories:
#     if cat.name == selected_category.name: continue
#     display(HTML("<b>" + cat.name + ":</b> <a target='_blank' href='file:" + sample_base + cat.name + "'>" + sample_base + cat.name + "</a>"))
display(HTML("Press the 'Begin Tagging!' button above to continue."))


def image_should_show(image_name):
    if image_name in deleted_image_names: return True
    if selected_category.no.has(image_name) or selected_category.yes.has(image_name): return False
    if images.is_reserved(image_name): return False
    for cat in all_categories:
        if cat.name == selected_category.name: continue
        if cat.yes.has(image_name): return False
    return True

def image_set(image_name, value):
    if value:
        selected_category.no.remove(image_name)
        images.copy(image_name, selected_category.yes)
    else:
        selected_category.yes.remove(image_name)
        images.copy(image_name, selected_category.no)
        
#num_yes = selected_category.num_yes
#num_no = selected_category.num_no
num = len(all_image_names)

tag_map = {
    "1": True,
    "2": False
}

class TagInput:
    def __init__(self, key):
        self.key = key
        self.tag = tag_map[key] if (key in tag_map) else None
        self._isBack = key == "ArrowLeft"
        self._isForward = key == "ArrowRight"
        self._isExit = key == "Escape"
    def isBack(self):
        return self._isBack
    def isForward(self):
        return self._isForward
    def isExit(self):
        return self._isExit

deleted_image_names = {}
i = 0
warning = None
message = None
can_handle_tag_input = False

def handle_key(change):
    if change.new is None or change.new == "None": return
    print("received a key: " + change.new)
    handle_tag_input(TagInput(change.new))

def prepare_for_next_image():
    global can_handle_tag_input
    while still_preparing(): pass
    can_handle_tag_input = True
    
def handle_tag_input(tag_input):
    global can_handle_tag_input
    if not can_handle_tag_input: return
    can_handle_tag_input = False
    if not should_continue(tag_input): return
    prepare_for_next_image()
    
def still_preparing():
    global i, warning, message
    if i < 0: i = 0
    if i >= num: i = num - 1
    image_name = all_image_names[i]
    if i < num - 1 and not image_should_show(image_name):
        i += 1
        return True
    clear_output()
    images.reserve(image_name)
    num_yes = selected_category.yes.count()
    num_no = selected_category.no.count()
    display(HTML("<div style='font-size:28pt;'>Image " + str(i + 1) + "/" + str(num) + "&nbsp;&nbsp;&nbsp;<span style='color: grey;'>[<span style='color: green;'>" + str(num_yes) + "</span>]</span></div><br/>"))
    #display(HTML("<div>Current stats: " + str(num_yes) + " " + selected_category.name + "&nbsp;&nbsp;&nbsp;" + str(num_no) + " NOT " + selected_category.name + "</div>"))
    res = selected_category.result(image_name)
    if not(res is None): display(HTML("<div>Currently labeled as " + ("" if res is True else "NOT ") + selected_category.name + "</div><br/>"))
    if not(message is None):
        print(message)
        message = None
    if not(warning is None):
        display(HTML("<div style='color: red'><b>(!)</b> " + warning + "</div><br/>"))
        warning = None
    display(Image(images.slash(image_name), width = 500, height = 300))
    #print("[Counts: " + str(num_yes) + " " + selected_category.name + ", " + str(num_no) + " not " + selected_category.name + "]")
    display(HTML("<input type='text' placeholder='  [ 1 ] = " + selected_category.name + "    [ 2 ] = NOT " + selected_category.name + "' size='70' id='txt_field'/><script>window.inputElement = document.getElementById('txt_field'); window.inputElement.focus();</script>"))
    return False

def should_continue(tag_input):
    global i, warning, message, num #, num_yes, num_no
    image_name = all_image_names[i]
    images.unreserve(image_name)
    if tag_input.isBack():
        if i <= 0:
            warning = "You're at the first image."
            return True
        prev_image_name = all_image_names[i - 1]
        if not image_should_show(image_name): deleted_image_names[image_name] = True
        if not image_should_show(prev_image_name): deleted_image_names[prev_image_name] = True
        i -= 1
    elif tag_input.isForward():
        if image_name in deleted_image_names: del deleted_image_names[image_name]
        if image_should_show(image_name):
            warning = "Please label this image first."
            return True
        if i >= num - 1:
            clear_output()
            print("You're done! :) Bye!")
            return False
        i += 1
    elif tag_input.isExit():
        clear_output()
        print("Ok! :) Bye!")
        return False
    elif not(tag_input.tag is None):
        if image_name in deleted_image_names: del deleted_image_names[image_name]
        res = selected_category.result(image_name)
        if res is True: pass #num_yes -= 1
        if res is False: pass #num_no -= 1
        if tag_input.tag is True: pass #num_yes += 1
        if tag_input.tag is False: pass #num_no += 1
        image_set(image_name, tag_input.tag)
        if i >= num - 1:
            clear_output()
            print("You're done! :) Bye!")
            return False
        i += 1
    else:
        warning = "Wrong label (" + tag_input.key + "). Please try again."
    return True

display(HTML("<script src=\"tag_images_social_appearance.js\"></script>"))

key_widget = KeyWidget()
display(key_widget)
key_widget.observe(handle_key, names=["current_key"])

def pressed_btn(x):
    clear_output()
    print("Please wait. Things are currently happening in places...")
    btn.close()
    prepare_for_next_image()

btn = widgets.Button(description="Begin Tagging!", button_style="success")
btn.on_click(pressed_btn)
display(btn)