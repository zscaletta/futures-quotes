import requests


class Quotes:

    def __init__(self):
        self.loggedin = False
        # Start a session so we can have persistent cookies
        self.session = requests.Session()
        self.login_uname = ''
        self.login_pword = ''

    def set_login(self, username, password):
        self.login_uname = username
        self.login_pword = password

    def login(self):
        if self.login_uname and self.login_pword:
            # This is the form data that the page sends when logging in
            login_data = {
                'email': self.login_uname,
                'password': self.login_pword}
            # Authenticate
            url = 'http://www.barchart.com/login.php'
            r = self.session.post(url, data=login_data)
            if r:
                self.loggedin = True
        else:
            print('*********   Error: use "Quotes.set_login(username, password)" to configure Barchart login!')

    def get_futures(self, symbol):

        # 'Futures Product codes are the same as CBOE for the most part..
        # exceptions are included in 'symbs' dict so that keyword can be looked up instead of checking Barchart
        symbs = {'VIX': 'VI',
                 'VX': 'VI'}
        if symbol in symbs:
            symbol = symbs[symbol]

        downloadlink = 'http://www.barchart.com/export.php?symbols={0}Y0,{0}^F&fields=futures.contract,last,change,open,high,low,previous,volume,displaytime&mode=I&extension=.csv'.format(symbol)

        if self.loggedin:
            r = self.session.get(downloadlink)
            txt = r.text
            txt = txt.replace('\r\n', ',')
            txt = txt.replace(',,', ',')
            data = txt.split(",")
            data = data[2:]
            composite_list = [data[x:x+9] for x in range(0, len(data), 9)]
            final = []
            for line in composite_list:
                if len(line) > 2:
                    final.append(line)
            return final
        else:
            self.login()
            if self.loggedin:
                r = self.session.get(downloadlink)
                txt = r.text
                txt = txt.replace('\r\n', ',')
                txt = txt.replace(',,', ',')
                data = txt.split(",")
                ndata = []
                for item in data:
                    ndata.append(item[1:-1])
                data = ndata
                data = data[2:]
                composite_list = [data[x:x+9] for x in range(0, len(data), 9)]
                final = []
                for line in composite_list:
                    if len(line) > 2:
                        final.append(line)
                return final
