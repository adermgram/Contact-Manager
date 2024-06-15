from tkinter import *
from tkinter import messagebox, simpledialog
import json


# ---------------------------- ADD CONTACT ------------------------------- #
def add_contact():
    f_name = f_name_entry.get().title()
    l_name = l_name_entry.get().title()
    phone_no = phone_entry.get()
    email = email_entry.get().lower()

    new_data = {
        f_name: {
            "surname": l_name,
            "phone": phone_no,
            "email": email,
        }
    }
    if len(f_name) == 0 or len(phone_no) == 0:
        messagebox.showinfo(title="Oops", message="First name or phone number can't be empty.")
    else:
        save(new_data)
        messagebox.showinfo(title="Success", message="Added successfully")


# ---------------------------- SAVE CONTACT ------------------------------- #
def save(new_data):
    try:
        with open("data.json", "r") as data_file:
            # reading data
            old_data = json.load(data_file)

    except FileNotFoundError:
        with open("data.json", "w") as data_file:
            # saving new data
            json.dump(new_data, data_file, indent=4)

    else:
        # updating old data with new data
        old_data.update(new_data)

        with open("data.json", "w") as data_file:
            # saving updated data
            json.dump(old_data, data_file, indent=4)

    finally:
        clear_entry()


# ---------------------------- CLEAR ENTRY ------------------------------- #
def clear_entry():
    f_name_entry.delete(0, END)
    l_name_entry.delete(0, END)
    phone_entry.delete(0, END)
    email_entry.delete(0, END)


# ---------------------------- UPDATE FUNCTION ------------------------------- #


def update_data():
    query = simpledialog.askstring(title="Contact manager", prompt="Enter either first name, last name, mail or phone "
                                                                   "number"
                                                                   "to update")
    if query == '':
        messagebox.showinfo(title="Erro",
                            message="Please enter either first name, last name, phone number or email to update")
        return

    result = search_contacts(query)
    if result is not None:
        messagebox.showinfo(title="Contact found",
                            message="Please modify the entry you want to change from the home and click!! to add button")
        for name in result:
            first_name = name
        l_name = result[first_name]['surname']
        phone = result[first_name]['phone']
        email = result[first_name]['email']
        f_name_entry.insert(0, first_name)
        l_name_entry.insert(0, l_name)
        phone_entry.insert(0, phone)
        email_entry.insert(0, email)

        data_file = open("data.json")
        data = json.load(data_file)
        del data[first_name]
        data_file.close()

        data_file = open("data.json", "w")
        json.dump(data, data_file, indent=4)
        data_file.close()
    else:
        messagebox.showerror(message="Contact not found")


# ---------------------------- QUERY FUNCTION ------------------------------- #

def search_contacts(query):
    with open("data.json") as data_file:
        contacts = json.load(data_file)
    result = None
    for first_name, details in contacts.items():
        if query.lower() == first_name.lower() or query.lower() == details['surname'].lower() or query.lower() == \
                details['phone'] or query.lower() == details['email']:
            result = {first_name: details}
    return result


# ---------------------------- FIND CONTACT ------------------------------- #
def find_person():
    query = simpledialog.askstring(title="Contact manager", prompt="Enter either first name, last name, mail or phone "
                                                                   "number of the contact you want to search")

    if query == '':
        messagebox.showinfo(title="Error",
                            message="Please enter either first name, last name, phone number or email to search")
        return

    result = search_contacts(query)
    if result is not None:
        for name in result:
            first_name = name
        l_name = result[first_name]['surname']
        phone = result[first_name]['phone']
        email = result[first_name]['email']

        messagebox.showinfo(title=f"{first_name} details",
                            message=f"First Name: {first_name}\nLast Name: {l_name}\nPhone no: {phone}\nEmail: {email}")
    else:
        messagebox.showinfo(title="Error", message=f"No detail for {query} exist.")


# ---------------------------- DELETE CONTACT ------------------------------- #
def delete_contact():
    query = simpledialog.askstring(title="Contact manager", prompt="Enter either first name, last name, mail or phone "
                                                                   "number of the contact you want to delete")
    if query == '':
        messagebox.showinfo(title="Error",
                            message="Please enter either first name, last name, phone number or email to delete")
    else:
        result = search_contacts(query)
        if result is not None:
            for name in result:
                first_name = name
            l_name = result[first_name]['surname']
            phone = result[first_name]['phone']
            email = result[first_name]['email']
            is_ok = messagebox.askyesno(title="Contact manager", message=f"First name: {first_name}\n"
                                                                         f"Last name: {l_name}\n"
                                                                         f"Phone no: {phone}\n"
                                                                         f"Email: {email}\n\n"
                                                                         f"Are you sure you want to delete?")
            if is_ok:
                data_file = open("data.json")
                data = json.load(data_file)
                del data[first_name]
                data_file.close()

                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
        else:
            messagebox.showerror(title="Error", message="No data found")


# ---------------------------- INFO FUNCTION ------------------------------- #
def show_info():
    with open("information.txt") as info_file:
        information = info_file.read()
        messagebox.showinfo(title="Our Info", message=information)



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Contact Manager")
window.config(bg='sky blue')
window.config(padx=50, pady=50)

canvas = Canvas(height=512, width=512)
logo_img = PhotoImage(file="images/logo.png")
canvas.create_image(256, 256, image=logo_img)
canvas.config(bg='sky blue', highlightthickness=0)
canvas.grid(row=1, column=1)

# Labels
f_name_label = Label(text="First Name:", bg='sky blue', font=('Arial', 10, 'bold'))
f_name_label.grid(row=2, column=0)
l_name_label = Label(text="Last Name:", bg='sky blue', font=('Arial', 10, 'bold'))
l_name_label.grid(row=3, column=0)
phone_label = Label(text="Phone:", bg='sky blue', font=('Arial', 10, 'bold'))
phone_label.grid(row=4, column=0)
email_label = Label(text="Email:", bg='sky blue', font=('Arial', 10, 'bold'))
email_label.grid(row=5, column=0)

# Entries
f_name_entry = Entry(width=45)
f_name_entry.grid(row=2, column=1)
f_name_entry.focus()
l_name_entry = Entry(width=45)
l_name_entry.grid(row=3, column=1)
phone_entry = Entry(width=45)
phone_entry.grid(row=4, column=1)
email_entry = Entry(width=45)
email_entry.grid(row=5, column=1)

# Buttons
add_button = Button(text="Add", width=13, command=add_contact,
                    cursor='hand2', activebackground="#068FFF", bg="#DCF2F1")
add_button.grid(row=2, column=2)
search_button = Button(text="Search", width=13, command=find_person, bg="#DCF2F1", cursor="hand2",
                       activebackground="#068FFF")
search_button.grid(row=3, column=2)
update_button = Button(text="Update", width=13, command=update_data, bg="#DCF2F1", cursor="hand2",
                       activebackground="#068FFF")
update_button.grid(row=4, column=2)
delete_button = Button(text="Delete", width=13, command=delete_contact, bg="#DCF2F1", cursor="hand2",
                       activebackground="#068FFF")
delete_button.grid(row=5, column=2)

info_pic = PhotoImage(file="images/info.png")
info_button = Button(image=info_pic, bg='sky blue', command=show_info, cursor="hand2")
info_button.grid(row=0, column=2)
window.mainloop()



