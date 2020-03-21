import requests

# Test 1: Verify Credentials: For Invalid Password should return 401
verify_credentials_response = requests.get('http://localhost:8000/players?page=2', auth=('admin', 'mybadpass'))
if verify_credentials_response.status_code != 401:
    print('Test 1: Verify Credentials,Status:Failed, Message: Invalid password can be entered, but expected 401 error')


# Test 2: Verify paging: for single page must return 50 items
page_size_response = requests.get('http://localhost:8000/players?page=2', auth=('admin', 'admin'))
num_of_items = len(page_size_response.json())
if num_of_items != 50:
    print('Test 2: Verify page size, Status:Failed, Message: max 49 elements are returned while expected 50 elements ')


# Test 3: Verify Paging Order: First Item on page #21 should be 20*50 = 1000
paging_order_response = requests.get('http://localhost:8000/players?page=21', auth=('admin', 'admin'))
if len(paging_order_response.json()) > 0 and paging_order_response.json()[0]["ID"] != 20 * 50:
    print(
        f'Test 3: Validate Paging Order, Status: Failed, Message: For the page 21, first element ID expected to be 1000, but actual was {paging_order_response.json()[0]["ID"]}')


# Test 4: Verify data integrity: the same request returns the same response json
first_response = requests.get('http://localhost:8000/players?page=1', auth=('admin', 'admin'))
second_response = requests.get('http://localhost:8000/players?page=1', auth=('admin', 'admin'))
if first_response.json() != second_response.json():
    print('Test 4: Verify data integrity, Status:Failed, Message: the same page request should return same items')

# Test 5: Verify data integrity: Items with Empty Name property
print("Test 5: Reproduce bug of items with Empty Names:")
for i in range(1,100):
    empty_names_response = requests.get('http://localhost:8000/players?page=1', auth=('admin', 'admin'))
    print(f'    iteration: {i}:', end =" ")
    for player in empty_names_response.json():
         if player["Name"] == "":
             print(player["ID"], end =" ")
    print()
    # TBD: Add validation - we should test that we does not have such elements

# Test 6: Load test: run 100K requests
print("Test 6: Run load test with 100K sequential requests:")
for i in range(1,100*1000):
    # TBD: Add timer
    load_test_response = requests.get('http://localhost:8000/players?page=1', auth=('admin', 'admin'))
    print(f'    iteration: {i}')
    # TBD: Validate all requests succeeded