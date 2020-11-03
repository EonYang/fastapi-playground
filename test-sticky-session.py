import requests

'''
serve the app on k8s with more than 1 replicas.
call the endpoint to `set-cookie`
call the endpoint again, and assert that the response is from the same pod.
if it's not the same pod, there's issue with the sticky session.
'''
url = 'put the url here'
s = requests.Session()
res = s.get(url)
data = res.json()

print(res.headers.get('Set-Cookie'))

prev_pod_id = None
for i in range(100000):
    print(i)
    res = s.get(url)
    data = res.json()
    if prev_pod_id:
        assert data.get('pod_id') == prev_pod_id
        print('same pod id')
    else:
        prev_pod_id = data.get('pod_id')
