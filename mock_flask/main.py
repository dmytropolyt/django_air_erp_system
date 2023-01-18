from flask import Flask, request

app = Flask(__name__)


@app.route('/webhook/<int:pk>', methods=['POST'])
def webhook_receiver(pk):
    if request.method == 'POST':
        print(request.json)
        return 'Webhook received!'


if __name__ == '__main__':
    app.run(host='localhost', port=3000)