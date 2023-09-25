from app import app
import newrelic.agent
newrelic.agent.initialize('newrelic.ini')
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
