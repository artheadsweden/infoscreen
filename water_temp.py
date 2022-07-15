import requests_html

def get_water_temp():
    session = requests_html.HTMLSession()

    data = session.get('https://www.gotlandsenergi.se/badapp/iframe')

    data.html.render()

    data = data.text.split('<td>Åminne</td>')
    data = data[1].split('</td>')
    data = data[0].strip()
    return data[4:]
