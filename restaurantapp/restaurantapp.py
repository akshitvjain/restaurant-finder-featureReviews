from app import app

from gevent.wsgi import WSGIServer
http_server = WSGIServer(('', 5000), app)
http_server.serve_forever()

with open('feature_review_summary.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	for row in reader:
		print(row)

csvFile.close()
