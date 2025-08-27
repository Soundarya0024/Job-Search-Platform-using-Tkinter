from tkinter import *
from tkinter import filedialog
import tkinter.messagebox as messagebox #notifications
import pymysql #sql package
import shutil
import os

#GUI window setup
root = Tk()
root.geometry("1200x600")        #window size Width X Height
root.title("Job Search Platform")   #Screen title
root.configure(bg="khaki4")     #Window Background colour

#sql Connection Details
def get_connection():
    return pymysql.connect(host="Localhost",user="root",password="Mysql@12345",database="job_db")

# --- ADMIN FUNCTIONALITY ---

# POST JOB

def insert_data():
    job_id = job_id_entry.get()
    job_name = job_name_entry.get()
    location = location_var.get()
    role = roles_var.get()
    description = job_description_entry.get()
    company = company_entry.get()

    if job_id and job_name and location and role and description and company:
        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute("INSERT INTO Admin_table VALUES (%s,%s,%s,%s,%s,%s)",
                        (int(job_id), job_name, location, role, description, company))
            con.commit()
            messagebox.showinfo("Success", "Job posted successfully")
            con.close()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "All fields required")

# SEARCH JOB (Admin side)
def search_data():
    job_id = job_id_entry.get()
    if not job_id:
        messagebox.showwarning("Alert", "Enter Job ID to search")
        return
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM Admin_table WHERE job_id=%s", (job_id,))
        row = cur.fetchone()
        if row:
            job_name_entry.delete(0, END)
            job_name_entry.insert(0, row[1])
            location_var.set(row[2])
            roles_var.set(row[3])
            job_description_entry.delete(0, END)
            job_description_entry.insert(0, row[4])
            company_entry.delete(0, END)
            company_entry.insert(0, row[5])
        else:
            messagebox.showinfo("Not found", "No job found")
        con.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- USER FUNCTIONALITY ---
resume_path = ""
def upload_resume():
    global resume_path
    file = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf"), ("DOC files", "*.docx")])
    if file:
        if not os.path.exists("resumes"):
            os.mkdir("resumes")
        dest = os.path.join("resumes", os.path.basename(file))
        shutil.copy(file, dest)
        resume_path = dest
        messagebox.showinfo("Uploaded", "Resume uploaded successfully")

# QUICK APPLY
def quick_apply():
    user_name = user_name_entry.get().strip()
    email_id = email_id_entry.get().strip()
    experience = experience_entry.get().strip()
    phone_no = phone_no_entry.get().strip()

    if user_name and email_id and experience and phone_no and resume_path:
        try:
            experience = int(experience)       # ✅ convert to int
            phone_no = int(phone_no)           # ✅ convert to int

            con = get_connection()
            cur = con.cursor()
            cur.execute("""
                INSERT INTO user_table (user_name, email_id, experience, phone_no, upload_resume)
                VALUES (%s, %s, %s, %s, %s)
            """, (user_name, email_id, experience, phone_no, resume_path))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Applied successfully")
        except ValueError:
            messagebox.showerror("Input Error", "Phone number and Experience must be numbers.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "All fields and Resume are required.")

# DELETE PROFILE

def delete_data():
    email = email_id_entry.get()
    if not email:
        messagebox.showwarning("Alert", "Enter Email to delete")
        return
    try:
        con = get_connection()
        cur = con.cursor()
        cur.execute("DELETE FROM user_table WHERE email_id=%s", (email,))
        con.commit()
        con.close()
        messagebox.showinfo("Deleted", "Profile deleted")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# UPDATE PROFILE

def update_data():
    user_name = user_name_entry.get()
    email_id = email_id_entry.get()
    experience = experience_entry.get()
    phone_no = phone_no_entry.get()

    if user_name and email_id and experience and phone_no:
        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute("UPDATE user_table SET user_name=%s, experience=%s, phone_no=%s WHERE email_id=%s",
                        (user_name, experience, phone_no, email_id))
            con.commit()
            con.close()
            messagebox.showinfo("Updated", "Profile updated")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Fill all", "Please fill all user details")

# ADD PROFILE

def add_profile():
    email_id = email_id_entry.get().strip()
    print("User entered email:", email_id)  # 🔍 Debug: show email entered

    if not email_id:
        messagebox.showwarning("Warning", "Enter Email ID to fetch profile")
        return

    try:
        con = get_connection()
        cur = con.cursor()

        # 🔍 Show what's in the table
        cur.execute("SELECT * FROM user_table")
        all_rows = cur.fetchall()
        print("All users in table:", all_rows)

        # 🔍 Now try the search
        cur.execute("SELECT user_name, experience, phone_no, upload_resume FROM user_table WHERE email_id = %s", (email_id,))
        result = cur.fetchone()
        print("Result from DB:", result)  # 🔍 Debug

        if result:
            user_name_entry.delete(0, END)
            user_name_entry.insert(0, result[0])

            experience_entry.delete(0, END)
            experience_entry.insert(0, result[1])

            phone_no_entry.delete(0, END)
            phone_no_entry.insert(0, result[2])

            messagebox.showinfo("Resume", f"Resume Path: {result[3]}")
        else:
            messagebox.showinfo("Not Found", "No profile found for this Email ID")

        con.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

#campanies button 

def show_company():
    job_id_val = job_id_entry.get().strip()

    if not job_id_val:
        messagebox.showwarning("Warning", "Please enter Job ID to view company details")
        return

    try:
        con = get_connection()
        cur = con.cursor()

        cur.execute("SELECT job_name, location, roles, job_description, company FROM Admin_table WHERE job_id = %s", (job_id_val,))
        result = cur.fetchone()

        if result:
            job_name_entry.delete(0, END)
            job_name_entry.insert(0, result[0])

            location_var.set(result[1])
            roles_var.set(result[2])

            job_description_entry.delete(0, END)
            job_description_entry.insert(0, result[3])

            company_entry.delete(0, END)
            company_entry.insert(0, result[4])

            messagebox.showinfo("Info", "Job details loaded successfully")
        else:
            messagebox.showinfo("Not Found", "No job found for this ID")

        con.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))


#Labels
Label(root,text="JOB SEARCH PLATFORM",font=("Times New Roman",20,'bold'),bg='lavender',fg='black').place(x=380,y=40)
#buttons ADMIN
Button(root,text="Companies",command=show_company,font=('Arial',16),bg='SteelBlue1',fg='black').place(x=55,y=120)
Button(root,text="PostJobs",command=insert_data,font=('Arial',16),bg='SteelBlue1',fg='black').place(x=250,y=120)
Button(root,text="Search",command=search_data,font=('Arial',16),bg='red4',fg='white').place(x=340,y=540)

#labels ADMIN
Label(text="CREATE_JOB",font=('Arial',16,'bold'),bg='lavender',fg='red').place(x=245,y=200)
Label(text="Job_id",font=('Arial',16),bg='lavender',fg='blue4').place(x=40,y=260)
#entry field
job_id_entry = Entry(root,font=('Arial',18),bg='lavender')
job_id_entry.place(x=200,y=260)

Label(text="Job_name",font=('Arial',16),bg='lavender',fg='blue4').place(x=40,y=320)
#entry field
job_name_entry = Entry(root,font=('Arial',18),bg='lavender')
job_name_entry.place(x=200,y=320)

Label(text="Location",font=('Arial',16),bg='lavender',fg='blue4').place(x=40,y=380)
location_var = StringVar()
location_dropdown = OptionMenu(root,location_var,"Coimbatore","Bangalore","Chennai","Hydrabad")
location_dropdown.config(font=('Arial',16),bg='white',fg='black')
location_dropdown.place(x=200,y=380)


Label(text="Roles",font=('Arial',16),bg='lavender',fg='blue4').place(x=365,y=380)

roles_var = StringVar()
roles_dropdown = OptionMenu(root,roles_var,"Python Developer","AI Engineer","Data Analyst","ML Engineer","Data Scientist")
roles_dropdown.config(font=('Arial',16),bg='white',fg='black')
roles_dropdown.place(x=460,y=380)

Label(text="Job_Description",font=('Arial',16),bg='lavender',fg='blue4').place(x=40,y=440)
#entry field
job_description_entry = Entry(root,font=('Arial',18),bg='lavender')
job_description_entry.place(x=200,y=440)

Label(text="Company",font=('Arial',16),bg='lavender',fg='blue4').place(x=40,y=490)
#entry field
company_entry = Entry(root,font=('Arial',18),bg='lavender')
company_entry.place(x=200,y=490)

#labels USER
Label(text="FIND YOUR DREAM JOB",font=('Arial',16,'bold'),bg='lavender',fg='red').place(x=760,y=200)
Label(text="User_Name",font=('Arial',16),bg='lavender',fg='blue4').place(x=720,y=260)
#entry field
user_name_entry = Entry(root,font=('Arial',18),bg='lavender')
user_name_entry.place(x=870,y=260)
Label(text="Email_id",font=('Arial',16),bg='lavender',fg='blue4').place(x=720,y=320)
#entry field
email_id_entry = Entry(root,font=('Arial',18),bg='lavender')
email_id_entry.place(x=870,y=320)
Label(text="Experience",font=('Arial',16),bg='lavender',fg='blue4').place(x=720,y=380)
#entry field
experience_entry = Entry(root,font=('Arial',18),bg='lavender')
experience_entry.place(x=870,y=380)
Label(text="Phone_No",font=('Arial',16),bg='lavender',fg='blue4').place(x=720,y=440)
#entry field
phone_no_entry = Entry(root,font=('Arial',18),bg='lavender')
phone_no_entry.place(x=870,y=440)

#Buttons USER
Button(root,text="Quick Apply",command=quick_apply,font=('Arial',16),bg='red4',fg='white').place(x=940,y=540)
Button(root,text="Delete",command=delete_data,font=('Arial',16),bg='red4',fg='white').place(x=1090,y=540)
Button(root,text="Add Profile",command=add_profile,font=('Arial',16),bg='SteelBlue1',fg='black').place(x=740,y=120)
Button(root,text="Upload Resume",command=upload_resume,font=('Arial',16),bg='SteelBlue1',fg='black').place(x=930,y=120)
Button(root,text="Update",command=update_data,font=('Arial',16),bg='red4',fg='white').place(x=820,y=540)
root.mainloop()

