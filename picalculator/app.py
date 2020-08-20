from flask import Flask
from flask import request

app = Flask(__name__)


def calcPi(limit: int):  # Generator function
    """
    Prints out the digits of PI
    until it reaches the given limit
    """

    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3

    decimal = limit
    counter = 0

    while counter != decimal + 1:
        if 4 * q + r - t < n * t:
            # yield digit
            yield n
            # insert period after first digit
            if counter == 0:
                yield '.'
            # end
            if decimal == counter:
                print('')
                break
            counter += 1
            nr = 10 * (r - n * t)
            n = ((10 * (3 * q + r)) // t) - 10 * n
            q *= 10
            r = nr
        else:
            nr = (2 * q + r) * l
            nn = (q * (7 * k) + 2 + (r * l)) // (t * l)
            q *= k
            t *= l
            l += 2
            k += 1
            n = nn
            r = nr


@app.route('/')
def home():
    digits = request.args.get('d')
    if digits is None:
        return 'BAD REQUEST:you should specify number of digits as `d` argument in GET method', 400
    try:
        digits = int(digits)
    except Exception as e:
        return "Exception:"+ str(e), 400

    return ''.join((str(c) for c in calcPi(digits)))


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)