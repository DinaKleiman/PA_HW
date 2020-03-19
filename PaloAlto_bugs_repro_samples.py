import requests

# Verify Credentials: For Invalid Password should return 401
verify_credentials_response = requests.get('http://localhost:8000/players?page=2', auth=('admin', 'mybadpass'))
if verify_credentials_response.status_code != 401:
    print('Test:Verify Credentials,Status:Failed, Message: Invalid password can be entered, but expected 401 error')


# Verify paging: for single page must return 50 items
page_size_response = requests.get('http://localhost:8000/players?page=2', auth=('admin', 'admin'))
num_of_items = len(page_size_response.json())
if num_of_items != 50:
    print('Test:Verify page size,Status:Failed, Message: max 49 elements are returned while expected 50 elements ')


# Verify Paging Order: First Item on page #21 should be 20*50 = 1000
paging_order_response = requests.get('http://localhost:8000/players?page=21', auth=('admin', 'admin'))
if len(paging_order_response.json()) > 0 and paging_order_response.json()[0]["ID"] != 20 * 50:
    print(
        f'Test: Validate Paging Order, Status: Failed, Message: For the page 21, first element ID expected to be 1000, but actual was {paging_order_response.json()[0]["ID"]}')



# Verify data integrity: the same request returns the same response json
first_response = requests.get('http://localhost:8000/players?page=1', auth=('admin', 'admin'))
second_response = requests.get('http://localhost:8000/players?page=1', auth=('admin', 'admin'))
if first_response.json() != second_response.json():
    print('est:Verify data integrity,Status:Failed, Message: the same request returns the same response json while expected the same data   ')
    #print (first_response.json(), second_response.json())
