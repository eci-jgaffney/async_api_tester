from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText


import aiohttp
import asyncio


def button_clicked():


    text_widget.delete(1.0, END)

    if validate_input() == False:
        return

    l_complete_url.config(text="", fg="black")


    api_url = cb_apis.get().strip()
    customer_code = e_customer_code.get().strip()
    endpoint = e_endpoint.get().strip()
    access_token = e_access_token.get().strip()
    iteration_count = int(e_iteration_count.get())

    text = "api: " + api_url + "\n"+ \
        "customer_code: " + customer_code + "\n"+ \
        "endpoint: " + endpoint + "\n"+ \
        "access token: " + access_token + "\n"+ \
        "num iterations: " + str(iteration_count) + "\n" \
        "------\n"

    complete_url = '%s/%s/%s' % (api_url, customer_code, endpoint)
    l_complete_url.config(text=complete_url)

    text_widget.insert(END, text)
    #
    # test
    # call api
    # insert results
    # validation

    run_async_test(iteration_count, complete_url, access_token)

# _num_iterations - number of times to call the API endpoint
# _full_url - the full url of the api endpoint
# _access_token - the API request's access token
def run_async_test(_num_iterations, _full_url, _access_token):

    _headers = {'Authorization': _access_token}

    async def main():
        async with aiohttp.ClientSession() as session:
            for _ in range(_num_iterations):
                async with session.get(_full_url, headers=_headers) as resp:
                    # print(resp.status)
                    # print(await resp.text())
                    text_widget.insert(END, str(resp.status) + "\n")
                    text_widget.insert(END, await resp.text() + "\n")

    #https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())


def validate_input():
    customer_code = e_customer_code.get().strip()
    endpoint = e_endpoint.get().strip()
    access_token = e_access_token.get().strip()
    iteration_count = e_iteration_count.get()

    l_complete_url.config(text="", fg="red")


    if customer_code == '':
        l_complete_url.config(text='Customer code cannot be blank')
        return False

    if endpoint == '':
        l_complete_url.config(text='Endpoint cannot be blank')
        return False

    if access_token == '':
        l_complete_url.config(text='Access token cannot be blank')
        return False

    if iteration_count == '':
        l_complete_url.config(text='Iteration count cannot be blank')
        return False

    if iteration_count.isdigit() == False:
        l_complete_url.config(text='Iteration count must be an integer.')
        return False

    return True



# ------------ Init ------------------

master = Tk()
master.title("Asynchronous API Caller")
master.geometry("975x470")
master.resizable(False, False)

# Dropdown menu options
options = [
    "https://development.ihmsweb.com/rest",
    "https://api.ecimarksystems.com/rest"
]

cb_apis = ttk.Combobox(
    state="readonly",
    values=options,
    width=40
)
cb_apis.grid(row=0, column=1, sticky=W)
cb_apis.current(0); #set the default value to the first option

Label(master, text="").grid(row=1); #spacer
Label(master, text='API').grid(row=0)
Label(master, text='Customer Code').grid(row=2)
Label(master, text='Endpoint').grid(row=3)
Label(master, text='Access Token').grid(row=4)
Label(master, text='Number of iterations').grid(row=5)

e_customer_code     = Entry(master, width=60)
e_customer_code.insert(0, "API")
e_endpoint          = Entry(master, width=60)
e_endpoint.insert(0, "companies/100")
e_access_token      = Entry(master, width=60)
e_iteration_count   = Entry(master, width=60)
e_iteration_count.insert(0, 10)

e_customer_code.grid(sticky=W, row=2, column=1)
e_endpoint.grid(sticky=W, row=3, column=1)
e_access_token.grid(sticky=W, row=4, column=1)
e_iteration_count.grid(sticky=W, row=5, column=1)

Label(master, text='Ex. BKR').grid(row=2, column=1, sticky=E)
Label(master, text='Ex. companies/100', anchor="w", justify=LEFT).grid(row=3, column=1, sticky=E)
Label(master, text='Ex. abc123-def456-ghi789', anchor="w", justify=LEFT).grid(row=4, column=1, sticky=E)
Label(master, text='Ex. 1 - 20', anchor="w", justify=LEFT).grid(row=5, column=1, sticky=E)
Label(master, text="").grid(row=6); #spacer



button = Button(master,
                   text="Submit",
                   command=button_clicked,
                   bg="lightgray",
                   fg="black")
button.grid(row=7, column=0)
l_complete_url = Label(master, text="")
l_complete_url.grid(row=7, column=1); #Shows complete url when button is clicked. Ex. https://development.ihmsweb.com/rest/DOR/companies/001

Label(master, text="").grid(row=8); #spacer

Label(master, text='API Response:').grid(row=9, column=0)


# Create a Scrollable Text widget
text_widget = ScrolledText(master, height=15, width=100, wrap="none")
text_widget.grid(row=9, column=1)



master.mainloop()


# api_url -> dropdown
# customer_code -> text
# endpoint -> text
# access_token -> text
# num iterations -> text
#
# api_url = 'https://development.ihmsweb.com/rest'
# customer_code = 'API'
# endpoint = 'companies/001'
# full_url = '%s/%s/%s' % (api_url, customer_code, endpoint)
# access_token = 'e32a3dc6-9665-47e1-9fd5-b9721aea453e'
# headers = {'Authorization': access_token}
# num_iterations = 10